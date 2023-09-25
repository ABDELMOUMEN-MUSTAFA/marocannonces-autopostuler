from bs4 import BeautifulSoup
import requests as req
import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)

class Auth:
    def __init__(self, username, password, url):
        self.payload = {
            'b[username]': username, 
            'b[password]': password, 
            'c': 'a*is*4'
        }
        self.login_url = url

    def firstFlight(self):
        page = req.post(self.login_url, data=self.payload)
        cookies = {}
        for cookie in page.cookies:
            cookies[cookie.name] = cookie.value
                
        self.cookies = cookies

    def login(self, offers):
        with req.session() as s:
            page = s.post(self.login_url, data=self.payload, cookies=self.cookies)
            if page.status_code == 200:
                bs = BeautifulSoup(page.text, 'html.parser')
                if bs.find('title').contents[0].strip() == 'Mon compte | marocannonces.com':
                    print(f"{Fore.GREEN}==============> Connecté à votre compte avec succès ! <==============")
                    payload = self.__getPayload(offers[0]['postuler_url'], s)
                    self.__postuler(offers, s, payload)
                    print(f"{Fore.GREEN}==============> Déconnecté de votre compte avec succès ! <==============")
                    return True
                else:
                    print(f"{Fore.RED}==============> Login ou mot de passe incorrect !!! <==============")
                    return False
            else:
                print(f"{Fore.RED}==============> Something went wrong (server error) !!! <==============")

    def __postuler(self, offers, s, payload):
        for offer in offers:
            page = s.post(offer['postuler_url'], data=payload, cookies=self.cookies)
            if page.status_code == 200:
                print(f"{Fore.GREEN}- Vous avez postulé à l'offre appelée '{offer['nom']}' avec succès.")
            else:
                print(f"{Fore.RED}- Une erreur se produit lorsque vous essayez de postuler à l'offre nommée '{offer['nom']}'.")

    def __getPayload(self, url, s):
        payload = {}
        page = s.get(url, cookies=self.cookies)
        bs = BeautifulSoup(page.text, 'html.parser')
        form = bs.find('form', id="seller_form_top")
        payload['c[senders_name]'] = form.find('input', id="c_senders_name").get('value')
        payload['c[senders_phone]'] = form.find('input', id="c_senders_phone").get('value')
        payload['c[senders_comments]'] = self.__getLettreMotivatin(form)
        payload['c[senders_secteur]'] = form.find('select', id="secteur_cv").find('option', selected="selected").get('value')
        payload['domaine_id'] = form.find('input', id="domaine_id").get('value')
        payload['c[senders_domaine]'] = bs.find('select', id="domaine_cv").find('option', selected="selected").get('value')
        payload['c[senders_studylevel]'] = form.find('select', id="c_senders_studylevel").find('option', selected="selected").get('value')
        payload['c[senders_experience]'] = form.find('select', id="c_senders_experience").find('option', selected="selected").get('value')
        payload['c[senders_city]'] = form.find('select', id="c_senders_city").find('option', selected="selected").get('value')
        payload['action'] = "upload"
        return payload

    def __getLettreMotivatin(self, form):
        letterMotivationInScript = form.find_all('script')[3].string
        start_marker = 'jQuery( "#c_senders_comments" ).html("'
        end_marker = '");'
        start_index = letterMotivationInScript.find(start_marker)
        end_index = letterMotivationInScript.find(end_marker, start_index)
        letterMotivation = letterMotivationInScript[start_index + len(start_marker):end_index]
        return letterMotivation