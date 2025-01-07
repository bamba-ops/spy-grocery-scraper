import re


def extract_number_from_string(s):
    """
    Extract the first number from a string.

    Args:
    - s (str): The string to extract the number from.

    Returns:
    - float: The extracted number, or None if no number is found.
    """
    match = re.search(r"\d+(\.\d+)?", s)
    if match:
        return float(match.group())
    return None


def handle_standardize_units(data):
    """
    Convertit les prix dans des unités standardisées (kg, L, unité).
    """
    for item in data:
        if "g" in item["unit"].lower():
            value_in_grams = extract_number_from_string(item["unit"])
            item["price"] = (item["price"] / value_in_grams) * 1000  # Convertir en kg
            item["unit"] = "kg"
        elif "ml" in item["unit"].lower():
            value_in_ml = extract_number_from_string(item["unit"])
            item["price"] = (item["price"] / value_in_ml) * 1000  # Convertir en ml
            item["unit"] = "L"
        elif item["unit"] == "kg" or item["unit"] == "L":
            pass  # Pas besoin de conversion
    return data


def handle_extract_unit_and_value(input_string):
    # Liste des unités de mesure communes
    units = ["g", "kg", "ml", "l", "cm", "m", "km", "oz", "lb", "x"]

    # Création d'une expression régulière pour détecter les valeurs suivies d'unités
    pattern = r"(\b\d+(?:\.\d+)?(?:\s*[xX\*]\s*\d+)?\s*(?:{}))".format("|".join(units))

    # Recherche dans la chaîne
    match = re.search(pattern, input_string, re.IGNORECASE)

    if match:
        # Extraction de la valeur et de l'unité
        result = match.group(0).strip()
        return result

    return ""  # Retourne une chaîne vide si aucune unité n'est trouvée


def handle_clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def wait_for_element(page, element_selector):
    try:
        page.wait_for_selector(
            element_selector, timeout=10000
        )  # Remplacez 'selector' par le sélecteur CSS spécifique
        print(f"L'élément avec le sélecteur '{element_selector}' a été trouvé.")
    except:
        print(
            f"L'élément avec le sélecteur '{element_selector}' n'a pas été trouvé après 10 secondes."
        )


def handle_banner(page):
    try:
        page.locator("text=Accepter").click(
            timeout=5000
        )  # Remplacez "Accepter" par le texte exact du bouton
    except:
        print("Aucune bannière de cookies ou modale détectée.")


def handle_dialog(dialog):
    print(f"Dialog message: {dialog.message}")
    dialog.accept()


def handle_extract_prices(data):
    """
    Extrait les prix et unités des données scrapées.
    """
    cleaned_data = []
    for item in data:
        # Matcher les prix avec unités (ex. "1,96 $/kg", "1,96 $/ kg", "1,96$/kg", "0,55 $ / 100 G.")
        match = re.search(r"(\d+,\d+)\s?\$\s?/\s?(\d+\s?\w+)?", item, re.IGNORECASE)
        if match:
            price = float(match.group(1).replace(",", "."))
            unit = match.group(2).strip() if match.group(2) else "unité"
            cleaned_data.append({"price": price, "unit": unit})
        elif "ch." in item:  # Prix fixes sans unité
            fixed_price = float(re.search(r"(\d+,\d+)", item).group().replace(",", "."))
            cleaned_data.append({"price": fixed_price, "unit": "unité"})
    return cleaned_data


def handle_standardize_units_metro(data):
    """
    Convertit les prix dans des unités standardisées (kg, L, unité).
    """
    for item in data:
        if item["unit"] == "100g":
            item["price"] *= 10  # Convertir en kg
            item["unit"] = "kg"
        elif item["unit"] == "100ml":
            item["price"] *= 10  # Convertir en litre
            item["unit"] = "L"
        elif item["unit"] == "kg" or item["unit"] == "L":
            pass  # Pas besoin de conversion
    return data


def handle_extract_prices_metro(data):
    """
    Extrait les prix et unités des données scrapées.
    """
    cleaned_data = []
    for item in data:
        # Matcher les prix avec unités (ex. "1,96 $ /kg") ou prix fixes ("ou 5,29 $ ch.")
        match = re.search(r"(\d+,\d+)\s\$\s?\/?(\w+)?", item)
        if match:
            price = float(match.group(1).replace(",", "."))
            unit = match.group(2) if match.group(2) else "unité"
            cleaned_data.append({"price": price, "unit": unit})
        elif "ch." in item:  # Prix fixes sans unité
            fixed_price = float(re.search(r"(\d+,\d+)", item).group().replace(",", "."))
            cleaned_data.append({"price": fixed_price, "unit": "unité"})
    return cleaned_data
