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
    Extrait les prix (ex: "1,43 $ /100g") et ignore les prix du type "4,39 $ ch.".
    """
    cleaned_data = []
    for item in data:
        # On recherche un format du type "(\d+,\d+) $ /(\w+)" (ex.: "1,43 $ /100g")
        # Note le slash '/' obligatoire pour filtrer les "ch."
        match = re.search(r"(\d+,\d+)\s*\$\s*/(\w+)", item)
        if match:
            price_str = match.group(1)  # "1,43"
            unit_str = match.group(2)  # "100g"
            price = float(price_str.replace(",", "."))
            cleaned_data.append({"price": price, "unit": unit_str})
        # Sinon, on ignore tout ce qui ne correspond pas
        # (notamment ceux qui contiennent "ch.")
    return cleaned_data


def remove_ch_prices(line: str) -> str:
    """
    Retire tout segment du type "<prix> $ ch." s'il n'y a pas de slash ensuite.
    Ex. "4,39 $ ch." -> supprimé.
    On laisse intact le reste, comme "1,43 $ /100g".
    """
    return re.sub(r"\d+,\d+\s*\$\s*ch\.", "", line, flags=re.IGNORECASE)


def separate_price_units(line: str) -> str:
    """
    Insère un espace entre l'unité (kg, lb, g, ml, etc.)
    et un prix collé qui suit immédiatement.
    Ex: "1,52 $ /kg0,69 $ /lb." -> "1,52 $ /kg 0,69 $ /lb."
    """
    pattern = r"(kg|lb|g|ml|[0-9]+g|[0-9]+ml)(\d+,\d+)"
    return re.sub(pattern, r"\1 \2", line)


def handle_extract_prices_metro_2(data):
    """
    Extrait toutes les occurrences de "<prix> $ /<unité>"
    - Ignore '... $ ch.' (pas de slash)
    - Ignore toutes les occurrences contenant 'lb'
    """
    pattern = re.compile(r"(\d+,\d+)\s*\$\s*/(\w+)\.?", re.IGNORECASE)
    cleaned_data = []
    for line in data:
        # 1) Supprimer "XX,XX $ ch."
        line = remove_ch_prices(line)
        # 2) Séparer "kg0,69" => "kg 0,69"
        line = separate_price_units(line)

        # 3) Extraire les prix
        matches = pattern.findall(line)
        for price_str, unit_str in matches:
            # Si l'unité est "lb", on skip
            if "lb" in unit_str.lower():
                continue

            price = float(price_str.replace(",", "."))
            cleaned_data.append({"price": price, "unit": unit_str})
    return cleaned_data


def handle_standardize_units_2(data):
    """
    Convertit les prix dans des unités standardisées (kg, L, etc.)
    Exemples :
      - "100g" -> on convertit le prix en $/kg
      - "100ml" -> on convertit le prix en $/L
    """
    for item in data:
        unit_lower = item["unit"].lower()
        print(item)

        # 3) Cas "g" => on convertit en "kg"
        if "g" in unit_lower and unit_lower != "kg":
            # ex.: "g", "G"
            # On suppose que c'est 1g => convertir en 1 kg => * 1000
            item["price"] = (item["price"] * 1000) / 100
            item["unit"] = "kg"

        # 4) Cas "kg" => on laisse tel quel
        # Rien à faire

        # 5) Cas "ml" => on convertit en "L"
        if "ml" in unit_lower and unit_lower != "l":
            # On suppose que c'est 1 ml => * 1000 = 1 L
            item["price"] = (item["price"] * 1000) / 100
            item["unit"] = "L"

        if "lb" in unit_lower:
            # 1 lb ~ 0.45359237 kg
            del item["price"]
            del item["unit"]

        # 6) Cas "l" => laisser comme "L"
        if unit_lower == "l":
            # Rien à faire
            item["unit"] = "L"

    return data
