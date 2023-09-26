import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)

class Menu:
    def __init__(self, domaines, fonctions, niveaux, villes):
        self.domaines = domaines
        self.fonctions = fonctions
        self.niveaux = niveaux
        self.villes = villes

    def __clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def showOffers(self, offers):
        self.offers = offers
        self.__clearScreen()
        print("")
        print(f"{Fore.RED}=" * 33  + "  LA LISTE DES DERNIÈRES OFFRES " + "=" * 33 + "\n")

        if not offers :
            print("- Il n'y a pas de résultats correspondants à votre recherche, Veuillez redémarrer le script et réessayer.\n");
            print(f"{Fore.RED}="  * 98)
            return False
        
        print(f"{Fore.RED}="  * 98)
        for offer in offers:
            space = "  " if offer['id'] < 10 else " "
            print(f" {Fore.BLUE}[{offer['id']}]{space}=> {Fore.WHITE}{offer['nom']} | {offer['date_publication']} | {offer['ville']}")
            print(f"{Fore.RED}="  * 98);

        return True

    def getSelectedOffers(self):
        offers = []
        selectedOffers = input("- Vous pouvez sélectionner des offres de cette manière (par exemple : 1,3,5,4...) ou vous pouvez toutes les sélectionner en tapant le mot 'all' : ")
        if selectedOffers == 'all':
            for offer in self.offers:
                offers.append({"nom" : offer['nom'], "postuler_url" : offer['postuler_url']})
        else:
            selectedOffers = selectedOffers.split(',')
            for offer in selectedOffers:
                offer = offer.strip()
                if not offer.isnumeric():
                    print(f"{Fore.RED}la valeur '{offer}' n'est pas valide!")
                    self.getSelectedOffers()

                index_offer = int(offer)
                if index_offer > len(self.offers) or index_offer <= 0:
                    print(f"{Fore.RED}la valeur '{offer}' n'est pas valide!")
                    self.getSelectedOffers()

                value_offer = self.offers[index_offer - 1]
                offers.append({"nom" : value_offer['nom'], "postuler_url" : value_offer['postuler_url']})

        self.__clearScreen()
        return offers

    def showDomaines(self):
        i = 0
        print("")
        print(f"{Fore.RED}=" * 33  + "  LA LISTE DES DOMAINES  " + "=" * 33 + "\n")
        for name in self.domaines:
            i = i + 1
            space = "  " if i < 10 else " "
            print(f" {Fore.BLUE}[{i}]{space}=> {Fore.WHITE}{name}")

        print("\n" + f"{Fore.RED}=" * 91)
        
        domaine_index = input("- S'il vous plaît, choisissez le numéro de votre domaine : ")
        while not domaine_index.isnumeric() or int(domaine_index) - 1 >= len(self.domaines) or int(domaine_index) - 1 < 0:
            print(f"{Fore.RED}Veuillez entrer un numéro de domaine valide!")
            domaine_index = input("- S'il vous plaît, choisissez le numéro de votre domaine : ")
        return self.domaines[int(domaine_index) - 1]
            
    def showFonctions(self):
        i = 0
        print("")
        print(f"{Fore.RED}=" * 33  + "  LA LISTE DES FONCTIONS  " + "=" * 33 + "\n")
        for name in self.fonctions:
            i = i + 1
            space = "  " if i < 10 else " "
            print(f" {Fore.BLUE}[{i}]{space}=> {Fore.WHITE}{name}")

        print( "\n" + f"{Fore.RED}=" * 91)
        
        fonction_index = input("- S'il vous plaît, choisissez le numéro de votre fonction : ")
        while not fonction_index.isnumeric() or int(fonction_index) - 1 >= len(self.fonctions) or int(fonction_index) - 1 < 0:
            print(f"{Fore.RED}Veuillez entrer un numéro de fonction valide!")
            fonction_index = input("- S'il vous plaît, choisissez le numéro de votre fonction : ")
        return self.fonctions[int(fonction_index) - 1]

    def showNiveaux(self):
        i = 0
        print("")
        print(f"{Fore.RED}=" * 33  + "  LA LISTE DES NIVEAUX  " + "=" * 33 + "\n")
        for name in self.niveaux:
            i = i + 1
            space = "  " if i < 10 else " "
            print(f" {Fore.BLUE}[{i}]{space}=> {Fore.WHITE}{name}")

        print( "\n" + f"{Fore.RED}=" * 91)
        
        niveau_index = input("- S'il vous plaît, choisissez le numéro de votre niveau : ")
        while not niveau_index.isnumeric() or int(niveau_index) - 1 >= len(self.niveaux) or int(niveau_index) - 1 < 0:
            print(f"{Fore.RED}Veuillez entrer un numéro de niveau valide!")
            niveau_index = input("- S'il vous plaît, choisissez le numéro de votre niveau : ")
        return self.niveaux[int(niveau_index) - 1]

    def showVilles(self):
        i = 0
        print("")
        print(f"{Fore.RED}=" * 33  + "  LA LISTE DES VILLES  " + "=" * 33 + "\n")
        for name, ville in self.villes.items():
            print(f" {Fore.BLUE}[{ville}]  => {Fore.WHITE}{name}")
            
        print( "\n" + f"{Fore.RED}=" * 91)
        
        ville_value = input("- S'il vous plaît, choisissez le numéro de votre ville : ")
        while ville_value not in self.villes.values():
            print(f"{Fore.RED}Veuillez entrer un numéro de ville valide!")
            ville_value = input("- S'il vous plaît, choisissez le numéro de votre ville : ")
        return ville_value

    def keywordsJob(self):
        print("")
        return input("- Mots-clés à rechercher (facultatif) : ")
    
    def showMenu(self):
        queryString = {
            'kw': '',
            'f_3' : '',
            'f_574': '',
            'f_570': '',
            'ville': ''
        }
        
        self.__clearScreen()
        queryString['f_3'] = self.showDomaines()
        self.__clearScreen()
        queryString['f_574'] = self.showFonctions()
        self.__clearScreen()
        queryString['f_570'] = self.showNiveaux()
        self.__clearScreen()
        queryString['ville'] = self.showVilles()
        self.__clearScreen()
        queryString['kw'] = self.keywordsJob()
        return queryString
