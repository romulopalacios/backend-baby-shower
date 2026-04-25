import csv
import json

import os
# Leemos el CSV descargado de Google Sheets
csv_path = os.path.join(os.path.dirname(__file__), 'invitados.csv')
json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'data', 'invitados.json')
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(csv_path, mode='r', encoding='utf-8') as file:
    # DictReader convierte automáticamente la primera fila en las claves del JSON
    csv_reader = csv.DictReader(file)
    invitados = list(csv_reader)

# Lo exportamos como el JSON que consumirá el frontend
with open(json_path, mode='w', encoding='utf-8') as json_file:
    json.dump(invitados, json_file, indent=4, ensure_ascii=False)