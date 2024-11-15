import json

#TODO: dodati type hinting na sve funkcije!


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers: list, products:list, customers:list)->None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    # Omogućite unos kupca
    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers

    with open("customers.json", "r") as file:
        kupci = json.load(file)
    
    with open("products.json", "r") as file:
        proizvodi = json.load(file)

    with open("offers.json", "r") as file:
        ponude = json.load(file)

    odabir = input("Odaberite 1 ukoliko želite dodati kupca iz baze\nOdaberite 2 ukoliko želite dodati novog kupca\n")
    odabrani_kupac = 0
    if odabir == "1":
        postojeci_kupac = input("Odaberite vat_id postojećeg kupca: ")
        for kupac in kupci:
            if kupac["vat_id"] == postojeci_kupac:
                odabrani_kupac = kupac
    elif odabir == "2":
        unos_imena_kupca = input("Unesite ime kupca: ")
        unos_maila = input("Unesite Email adresu kupca: ")
        unos_VAT_ID = input("Unesite VAT ID: ")

        odabrani_kupac = {
            "name" : unos_imena_kupca,
            "email" : unos_maila,
            "vat_id" : unos_VAT_ID
        }
        kupci.append(odabrani_kupac)

        with open("customers.json", "w") as file:
            json.dump(kupci, file, indent=4)
        
    najveci_offer_numb = 0
    for ponuda in ponude:
        if ponuda["offer_number"] > najveci_offer_numb:
            najveci_offer_numb = ponuda["offer_number"]
        
    sljedeci_broj_ponude = najveci_offer_numb + 1

    datum = input("Unesite datum u formatu GGGG-MM-DD\n")

    stavke_ponude = []
    osnovica = 0
    while True:
        odabir_proizvoda = int(input("\n\nUnesite ID proizvoda: "))

        for proizvod in proizvodi:
            if proizvod["id"] == odabir_proizvoda:
                kolicina = int(input("Unesite količinu proizvoda: "))
                ukupna_cijena = kolicina * proizvod["price"]
                osnovica += ukupna_cijena
                proizvod_ponude = {
                    "product_id": proizvod["id"],
                    "product_name": proizvod["name"],
                    "description": proizvod["description"],
                    "price": proizvod["price"],
                    "quantity" : kolicina,
                    "item_total" : ukupna_cijena
                }
                stavke_ponude.append(proizvod_ponude)
                break
            
        dodavanje_drugog_proizvoda = input("Želite li dodati još jedan proizvod (DA/NE): ")
        if dodavanje_drugog_proizvoda.lower() == "ne".lower():
            break

    ponuda = {
        "offer_number" : sljedeci_broj_ponude,
        "customer" : odabrani_kupac["name"],
        "date" : datum,
        "items" : stavke_ponude,
        "sub_total" : osnovica,
        "tax": osnovica * 0.1,
        "total" : osnovica + osnovica * 0.1
    }
    ponude.append(ponuda)
    with open("offers.json", "w") as file:
        json.dump(ponude, file, indent=4)

    pass


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products: list)-> None:
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke

    with open("products.json", "r") as file:
        proizvodi = json.load(file)

    odabir = input("Upišite 1 za unos novog proizvoda \nUpišite 2 za izmjenu postojećeg proizvoda: ")
  
    if odabir == "1":
        unos_imena_proizvoda = input("Unesite ime proizvoda: ")
        unos_opisa_proizvoda = input("Unesite opis proizvoda: ")
        unos_cijene = float(input("Unesite cijenu proizvoda: "))
        najveci_id = 0
        for id in proizvodi:
            if id["id"] > najveci_id:
                najveci_id = id["id"]
        
        sljedeci_id = najveci_id + 1

        proizvod = {
            "id" : sljedeci_id,
            "name" : unos_imena_proizvoda,
            "description" : unos_opisa_proizvoda,
            "price" : unos_cijene
        }

        proizvodi.append(proizvod)
        
        with open("products.json", "w") as file:
            json.dump(proizvodi, file, indent=4)
    
    elif odabir == "2":
        for proizvod in proizvodi:
            print(f"\nID: {proizvod["id"]} Ime: {proizvod["name"]}, Opis: {proizvod["description"]}, Cijena: {proizvod["price"]}")

        odabir_proizvoda = int(input("\n\nUnesite ID proizvoda za izmjenu: "))
        proizvod_za_izmjenu = 0

        for proizvod in proizvodi:
            if proizvod["id"] == odabir_proizvoda:
                proizvod_za_izmjenu = proizvod
                break
        
        if proizvod_za_izmjenu:
            print(f"Odabrali ste proizvod: {proizvod_za_izmjenu}")

            proizvod_za_izmjenu["name"] = input("Novo ime proizvoda: ")
            proizvod_za_izmjenu["description"] = input("Novi opis proizvoda: ")
            proizvod_za_izmjenu["price"] = float(input("Nova cijena proizvoda: "))

            with open("products.json", "w") as file:
                json.dump(proizvodi, file, indent=4)
        
        else:
            print("\n\nNetočan unos IDa")

    pass


# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers: list)-> None:
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca

    with open("customers.json", "r") as file:
        kupci = json.load(file)

    odabir = input("Upišite 1 ukoliko želite dodati kupca \nUpišite 2 koliko želite pregled liste kupaca: ")
  
    if odabir == "1":
        unos_imena_kupca = input("Unesite ime kupca: ")
        unos_maila = input("Unesite Email adresu kupca: ")
        unos_VAT_ID = input("Unesite VAT ID: ")

        kupac = {
            "name" : unos_imena_kupca,
            "email" : unos_maila,
            "vat_id" : unos_VAT_ID
        }

        kupci.append(kupac)
        
        with open("customers.json", "w") as file:
            json.dump(kupci, file, indent=4)
    
    elif odabir == "2":
        for kupac in kupci:
            print(f"\nIme: {kupac["name"]}, Email: {kupac["email"]}, VAT ID: {kupac["vat_id"]}")

    pass


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers: list)-> None:
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora

    izbor = input("Za prikaz svih ponuda birajte 1\nZa prikaz ponuda po mjesecu birajte 2\nZa prikaz pojedinačne ponude birajte 3: ")
    if izbor == "1":
        for offer in offers:
            print_offer(offer)
    elif izbor == "2":
        izbor_mjeseca = input("Odaberite mjesec: ")
        for offer in offers:
            mjesec = offer["date"].split("-")[1]
            if izbor_mjeseca == mjesec:
                print_offer(offer)
    elif izbor == "3":
        broj_ponude = int(input("Unesite broj ponude za pregled: "))
        odabrana_ponuda = 0
        for offer in offers:
            if offer["offer_number"] == broj_ponude:
                odabrana_ponuda = offer
                break
        print_offer(offer)

    pass


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer: dict) -> None:
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()
