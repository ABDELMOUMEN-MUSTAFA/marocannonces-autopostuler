from bs4 import BeautifulSoup
import requests as req
import colorama
from colorama import Fore, Back

class Request:
    def __init__(self, base_url):
        self.__loading()
        self.base_url = base_url
        self.page = req.get(base_url)
        self.page.encoding = "utf-8"
        self.bs = BeautifulSoup(self.page.text, 'html.parser')
        self.offers = []
        self.countNotFoundOffers = 0

    def __loading(self):
        print(f"{Fore.YELLOW}CHARGEMENT...")

    def __addOffer(self, offerID, nom, ville, date_publication, postuler_url):
        offer = {}
        offer["id"] = offerID
        offer["nom"] = nom
        offer["ville"] = ville
        offer["date_publication"] = date_publication
        offer["postuler_url"] = postuler_url
        self.offers.append(offer)

    def __getPostulerUrl(self, urlOffer):
        request = self.__class__(urlOffer)
        page = request.page
        # if this offer is not exists return false otherwise return postuler url
        if page.status_code != 200 or not request.bs.find(class_='btn-reply'):
            self.countNotFoundOffers = self.countNotFoundOffers + 1
            return False

        return 'https://www.marocannonces.com/' + request.bs.find(class_='btn-reply').get('href')

    def getOffers(self):
        offerID = 0
        pages = self.__getPagination()
        for page in pages:
            request = self.__class__(self.base_url + '&pge=' + page)
            offersItems = request.bs.find(class_='cars-list')
            # if there is not offer return empty list
            if not offersItems:
                return self.offers
            
            for offerItem in offersItems.find_all('li'):
                # This is not an offer maybe it's an advertising
                if not offerItem.find('h3'):
                    print(f"{Fore.MAGENTA}- Publicité !!!")
                    continue

                # check if this offer still available
                postuler_url = self.__getPostulerUrl('https://www.marocannonces.com/' + offerItem.find('a').get('href'))
                if not postuler_url:
                    print(f"{Fore.RED}- L'offre nommée '{offerItem.find('h3').contents[0].strip()}' est introuvable.")
                    continue
        
                offerID = offerID + 1
                time = offerItem.find(class_='date').find('span').contents[0].strip()
                date = offerItem.find(class_='date').find(class_="date").contents[0].strip()
                date_publication = f"{date} - {time}"
                self.__addOffer(offerID, offerItem.find('h3').contents[0].strip(), offerItem.find(class_='location').contents[0], date_publication, postuler_url)
                print(f"{Fore.GREEN}- Recevoir une offre appelée '{offerItem.find('h3').contents[0].strip()}'")
            
            if offerID >= 50 or self.countNotFoundOffers > 40:
                break
                    
        return self.offers

    def __getPagination(self):
        pages = []
        paginations = self.bs.find(class_='paging')
        if not paginations:
            return []

        for page in paginations.find_all('li'):
            ancreTag = page.find('a')
            if not ancreTag:
                pages.append(page.find('strong').contents[0])
                continue
            
            innerText = page.find('a').contents[0]
            if innerText == 'Précédent' or innerText == 'Suivant':
                continue
            
            pages.append(innerText)

        return pages

    def __getFilters(self, id):
        filters = self.bs.find(id=id).find_all('option')
        filters.pop(0)
        return filters
    
    def getDomaines(self, id):
        domaines = []
        domaineOptions = self.__getFilters(id)
        for i in range(len(domaineOptions)):
            domaines.append(domaineOptions[i].get('value'))
        return domaines

    def getFonctions(self, id):
        fonctions = []
        fonctionOptions = self.__getFilters(id)
        for i in range(len(fonctionOptions)):
            fonctions.append(fonctionOptions[i].get('value'))
        return fonctions

    def getNiveaux(self, id):
        niveaux = []
        niveauOptions = self.__getFilters(id)
        for i in range(len(niveauOptions)):
            niveaux.append(niveauOptions[i].get('value'))
        return niveaux

    def getVilles(self, id):
        villes = {}
        villeOptions = self.__getFilters(id)
        for i in range(len(villeOptions)):
            villes[villeOptions[i].contents[0]] = villeOptions[i].get('value')
        return villes
