import pandas as pd
import re
from datetime import datetime

# Load the CSV file into a DataFrame
csv_file_path = r'C:\Users\xcrss\OneDrive - Universidad Tecnológica de Panamá\C 2\C\Code\Samsung\Proyecto_Tokyo\Tokyo_repo\csv\predictions.csv'
df = pd.read_csv(csv_file_path)
df['date'] = pd.to_datetime(df['date'])

# Mapping from product names in Spanish to class names in the CSV
product_class_map = {
    'lavadoras': 'SAM-LAV',
    'microondas': 'SAM-MIC',
    'refrigeradores': 'SAM-REF',
    'secadoras': 'SAM-SEC',
    'televisores': 'SAM-TV'
}

# Function to convert Spanish date format to "YYYY-MM-DD"
def convert_date(date_str):
    months = {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12'
    }
    day, month = date_str.split(' de ')
    month_number = months[month.lower()]
    return f"2024-{month_number}-{int(day):02d}"

# Function to handle queries about sales between dates
def ventas_entre_fechas(product, fecha_inicio, fecha_fin):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    ventas_count = df_filtered.shape[0]
    return f"Se vendieron {ventas_count} unidades de {product} entre {fecha_inicio.date()} y {fecha_fin.date()}."

# Function to handle queries about purchases between dates
def compras_entre_fechas(product, fecha_inicio, fecha_fin):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    compras_count = df_filtered.shape[0]
    return f"Se compraron {compras_count} unidades de {product} entre {fecha_inicio.date()} y {fecha_fin.date()}."

# Function to handle queries about total sales
def ventas_totales(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta')]

    ventas_totales_count = df_filtered.shape[0]
    return f"Se han vendido {ventas_totales_count} unidades de {product} en total."

# Function to handle queries about total purchases
def compras_totales(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra')]

    compras_totales_count = df_filtered.shape[0]
    return f"Se han comprado {compras_totales_count} unidades de {product} en total."

# Function to process user input and generate responses
def process_input(user_input):
    # Normalize input
    user_input = user_input.lower()

    # Check for greetings and farewells
    if user_input in ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'qué tal']:
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    if user_input in ['adiós', 'salir', 'hasta luego', 'nos vemos']:
        return "¡Adiós! ¡Que tengas un buen día!"

    # Regex patterns to match different types of queries
    patterns = [
        (r"cuántos (\w+) se vendieron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", ventas_entre_fechas),
        (r"cuántas (\w+) se vendieron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", ventas_entre_fechas),
        (r"cuántos (\w+) se compraron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", compras_entre_fechas),
        (r"cuántas (\w+) se compraron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", compras_entre_fechas),
        (r"cuántos (\w+) se han vendido", ventas_totales),
        (r"cuántas (\w+) se han vendido", ventas_totales),
        (r"cuántos (\w+) se han comprado", compras_totales),
        (r"cuántas (\w+) se han comprado", compras_totales)
    ]

    # Check if the input matches any of the patterns
    for pattern, func in patterns:
        match = re.match(pattern, user_input)
        if match:
            params = match.groups()
            return func(*params)
    
    return "Lo siento, no entendí eso. Por favor, haz una pregunta relacionada con los datos de ventas o saluda."

# Simulated conversation for testing
def simulate_conversation():
    inputs = [
        "hola",
        "cuántos refrigeradores se vendieron del 10 de junio al 20 de junio",
        "cuántos microondas se han comprado",
        "cuántas lavadoras se compraron del 15 de junio al 20 de junio",
        "adiós"
    ]
    
    print("¡Bienvenido al Chatbot de Consultas de Ventas!")
    print("Escribe 'salir' o 'adiós' para terminar el chat.")
    
    for user_input in inputs:
        print(f"Tú: {user_input}")
        response = process_input(user_input)
        print(f"Chatbot: {response}")
        if user_input.lower() in ['salir', 'adiós']:
            break

# Run the simulated conversation
if __name__ == "__main__":
    simulate_conversation()
