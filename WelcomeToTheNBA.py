import csv
import unicodedata
import matplotlib.pyplot as plt
import numpy as np
import json

file_path = "basket_players.csv"
output_file_path = "jugadors_basket.csv"

INCHES_TO_CMS = 2.54
POUNDS_TO_KGS = 0.45

def main():
    generar_nou_csv()
    obtenir_dades_csv()
    convertir_a_json()


def generar_nou_csv():
    csv_data = read_csv()
    show_csv_content(csv_data)
    csv_data = modify_header(csv_data)
    csv_data = translate_positions(csv_data)
    csv_data = convert_units(csv_data)
    csv_data = round_ages(csv_data)
    write_csv(csv_data)

def read_csv():
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            csv_data = list(csv_reader)
    except FileNotFoundError:
        print(f"L'arxiu '{file_path}' no existeix.")
        csv_data = []
    return csv_data

def show_csv_content(csv_data):
    for i, fila in enumerate(csv_data):
            print(f"Fila {i}: {fila}")

def modify_header(csv_data):
    try:
        if csv_data:
            header = csv_data[0]
            translations = {
                "Name": "Nom",
                "Team": "Equip",
                "Position": "Posició",
                "Heigth": "Altura",
                "Weigth": "Pes",
                "Age": "Edat"
            }
            header_translated = [translations.get(col, col) for col in header]
            csv_data[0] = header_translated
    except Exception as e:
        print(f"Error al modificar la capçalera: {e}")

    return csv_data

def translate_positions(csv_data):
    try:
        if csv_data:
            for i, fila in enumerate(csv_data[1:]):
                position = fila[2]
                position_translations = {
                    "Point Guard": "Base",
                    "Shooting Guard": "Escorta",
                    "Small Forward": "Aler",
                    "Power Forward": "Ala-pivot",
                    "Center": "Pivot"
                }
                translated_position = position_translations.get(position, position)
                csv_data[i+1][2] = translated_position
    except Exception as e:
        print(f"Error al traduir les posicions: {e}")

    return csv_data

def convert_units(csv_data):
    try:
        for i, row in enumerate(csv_data):
            if i > 0: 
                height_inch = float(row[3])
                height_cm = height_inch * INCHES_TO_CMS
                height_cm = round(height_cm, 2)
                row[3] = str(height_cm)

                weight_pound = float(row[4])
                weight_kg = weight_pound * POUNDS_TO_KGS
                weight_kg = round(weight_kg, 2)
                row[4] = str(weight_kg)
    except Exception as e:
        print(f"Error al convertir les unitats: {e}")

    return csv_data

def round_ages(csv_data):
    try:

        for i, row in enumerate(csv_data):
            if i > 0:  
                age = float(row[5])
                age = round(age)
                row[5] = str(age)
    except Exception as e: 
        print(f"Error al arrodonir les edats: {e}")

    return csv_data

def write_csv(csv_data):
    try:
        with open(output_file_path, mode='w', newline='', encoding='ascii') as file:
            csv_writer = csv.writer(file, delimiter='^')
            for row in csv_data:
                row = [unicodedata.normalize('NFD', cell).encode('ascii', 'ignore').decode('ascii') for cell in row]
                csv_writer.writerow(row)
    except Exception as e:
        print(f"Error al escriure el fitxer: {e}")

def obtenir_dades_csv():
    data = carregar_fitxer_csv_nou()
    obtenir_jugador_mes_pes(data)
    obtenir_jugador_mes_baix(data)
    diagrama_alcades(data)
    mitjana_dades(data)
    recompte_posicions(data)
    distribucio_edats(data)
    grafica_subplots(data)

def carregar_fitxer_csv_nou():
    try:
        data = np.genfromtxt(output_file_path, delimiter='^', dtype=str, encoding='utf-8')
    except Exception as e: 
        print(f"Error al carregar el fitxer: {e}")
        data = []

    return data

def obtenir_jugador_mes_pes(data):
    try:
        pes_max = np.max(data[1:, 4].astype(float))
        jugador_pes_max = data[np.where(data[1:, 4].astype(float) == pes_max)[0][0] + 1, 0]
        print(f"Jugador amb més pes: {jugador_pes_max}")
    except Exception as e: 
        print(f"Error al obtenir el jugador amb més pes: {e}")

def obtenir_jugador_mes_baix(data):
    try:
        altura_min = np.min(data[1:, 3].astype(float))
        jugador_altura_min = data[np.where(data[1:, 3].astype(float) == altura_min)[0][0] + 1, 0]
        print(f"Jugador més baix: {jugador_altura_min}")
    except Exception as e: 
        print(f"Error al obtenir el jugador més baix: {e}")

def diagrama_alcades(data):
    try:
        altures = data[1:, 3].astype(float)
        plt.bar(range(len(altures)), altures)
        plt.xlabel("Jugador")
        plt.ylabel("Alçada (cm)")
        plt.title("Alçades dels jugadors")
        plt.show()
    except Exception as e: 
        print(f"Error al mostrar el diagrama de les alçades: {e}")

def mitjana_dades(data):
    try:
        equips = np.unique(data[1:, 1])
        pesos = []
        alturas = []
        for equip in equips:
            indices = np.where(data[1:, 1] == equip)[0]
            pesos.append(np.mean(data[indices + 1, 4].astype(float)))  
            alturas.append(np.mean(data[indices + 1, 3].astype(float)))  

        plt.bar(range(len(equips)), pesos, label="Pes (kg)")
        plt.bar(range(len(equips)), alturas, bottom=pesos, label="Alçada (cm)")  
        plt.xticks(range(len(equips)), equips)
        plt.xlabel("Equip")
        plt.ylabel("Valor")
        plt.title("Mitjana de pes i alçada de jugador per equip")
        plt.legend()
        plt.show()
    except Exception as e: 
        print(f"Error al mostrar la mitjana de dades: {e}")

def recompte_posicions(data):
    try:
        posicions = np.unique(data[1:, 2])
        recompte = []
        for posicio in posicions:
            indices = np.where(data[1:, 2] == posicio)[0]
            recompte.append(len(indices))

        plt.pie(recompte, labels=posicions, autopct='%1.1f%%')
        plt.title("Recompte de jugadors per posició")
        plt.show()
    except Exception as e: 
        print(f"Error al mostrar el recompte de posicions: {e}")

def distribucio_edats(data):
    try:
        edats = data[1:, 5].astype(float)
        plt.hist(edats, bins=10, edgecolor='black')
        plt.xlabel("Edat")
        plt.ylabel("Nombre de jugadors")
        plt.title("Distribució de les edats dels jugadors")
        plt.show()
    except Exception as e:  
        print(f"Error al mostrar la distribució de les edats: {e}")

def grafica_subplots(data):
    try:
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        # Alçades de los jugadors
        alturas = data[1:, 3].astype(float)
        axs[0, 0].bar(range(len(alturas)), alturas)
        axs[0, 0].set_title("Alçades de los jugadors")

        # Mitjana de pes i alçada de jugador per equip
        equipos = np.unique(data[1:, 1])
        pesos = []
        alturas = []
        for equipo in equipos:
            indices = np.where(data[1:, 1] == equipo)[0]
            pesos.append(np.mean(data[indices + 1, 4].astype(float)))  
            alturas.append(np.mean(data[indices + 1, 3].astype(float)))  
        axs[0, 1].bar(range(len(equipos)), pesos, label="Pes (kg)")
        axs[0, 1].bar(range(len(equipos)), alturas, bottom=pesos, label="Alçada (cm)")  
        axs[0, 1].set_title("Mitjana de pes i alçada de jugador per equip")
        axs[0, 1].legend()
        # Recompte de jugadors per posició
        posicions = np.unique(data[1:, 2])
        recompte = []
        for posicio in posicions:
            indices = np.where(data[1:, 2] == posicio)[0]
            recompte.append(len(indices))
        axs[1, 0].pie(recompte, labels=posicions, autopct='%1.1f%%')
        axs[1, 0].set_title("Recompte de jugadors per posició")

        # Distribució de jugadors per edat
        edats = data[1:, 5].astype(float)
        axs[1, 1].hist(edats, bins=10, edgecolor='black')
        axs[1, 1].set_title("Distribució de jugadors per edat")

        plt.tight_layout()
        plt.show()
    except Exception as e: 
        print(f"Error al mostrar la gràfica de subplots: {e}")

def convertir_a_json():
    with open(output_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='^')
        next(reader)
        data = []
        for row in reader:
            jugador = {
                "nom": row[0],
                "equip": row[1],
                "posicio": row[2],
                "altura": row[3],
                "pes": row[4],
                "edat": row[5]
            }
            data.append(jugador)

    # Convertir a JSON
    with open('jugadors_basket.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()