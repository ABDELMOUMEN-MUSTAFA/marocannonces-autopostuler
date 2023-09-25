import urllib.parse
from request import Request
from auth import Auth
from menu import Menu

request = Request('https://www.marocannonces.com/maroc/offres-emploi-b309.html')
domaines = request.getDomaines('field_3')
fonctions = request.getFonctions('field_574')
niveaux = request.getNiveaux('field_570')
villes = request.getVilles('select-ville')

menu = Menu(domaines, fonctions, niveaux, villes)
queryString = menu.showMenu()

request_offers = Request(f"https://www.marocannonces.com/maroc/offres-emploi-b309.html?{urllib.parse.urlencode(queryString)}")
offers = request_offers.getOffers()
if not menu.showOffers(offers):
    input("==> Please press enter to stop the script <==")
    exit()

selectedOffers = menu.getSelectedOffers()

while True:
    # PUT YOUR USERNAME HERE 'hassan2456'
    username = input("- Nom d'utilisateur : ")
    while len(username) == 0:
        print(f"{Fore.RED} Veuillez entrer un nom d'utilisateur valid!")
        username = input("- Nom d'utilisateur : ")

    # PUT YOUR PASSWORD HERE 'dimabarca123'
    password = input("- Mot de passe : ")
    while len(password) == 0:
        print(f"{Fore.RED} Veuillez entrer un mot de passe valid!")
        password = input("- Mot de passe : ")

    auth = Auth(username, password, 'https://www.marocannonces.com/index.php?a=10&back=no')
    auth.firstFlight()
    if auth.login(selectedOffers):
        break

print("")
input("==> Please press enter to stop the script <==")
