import pandas as pd
import re
from datetime import datetime

import os
# Load the CSV file into a DataFrame
current_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(current_dir, '..', 'data/processed/', 'predictions.csv')
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

# Function to handle queries about daily average sales between dates
def promedio_ventas_diarias(product, fecha_inicio, fecha_fin):
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
    days_count = (fecha_fin - fecha_inicio).days + 1  # Incluyendo ambos extremos
    promedio_ventas = ventas_count / days_count
    return f"El promedio de ventas diarias de {product} entre {fecha_inicio.date()} y {fecha_fin.date()} es {promedio_ventas:.2f} unidades por día."

# Function to handle queries about daily average purchases between dates
def promedio_compras_diarias(product, fecha_inicio, fecha_fin):
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
    days_count = (fecha_fin - fecha_inicio).days + 1  # Incluyendo ambos extremos
    promedio_compras = compras_count / days_count
    return f"El promedio de compras diarias de {product} entre {fecha_inicio.date()} y {fecha_fin.date()} es {promedio_compras:.2f} unidades por día."

# Function to handle queries about the day with most sales
def dia_con_mas_ventas(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta')]
    
    if df_filtered.empty:
        return f"No hay datos de ventas para {product}."
    
    df_grouped = df_filtered.groupby('date').size()
    max_ventas_date = df_grouped.idxmax()
    max_ventas_count = df_grouped.max()
    return f"El día con más ventas de {product} fue {max_ventas_date.date()} con {max_ventas_count} unidades vendidas."

# Function to handle queries about the day with most purchases
def dia_con_mas_compras(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra')]
    
    if df_filtered.empty:
        return f"No hay datos de compras para {product}."
    
    df_grouped = df_filtered.groupby('date').size()
    max_compras_date = df_grouped.idxmax()
    max_compras_count = df_grouped.max()
    return f"El día con más compras de {product} fue {max_compras_date.date()} con {max_compras_count} unidades compradas."

# Function to handle queries about sales on a specific day
def ventas_por_dia(product, fecha):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha = pd.to_datetime(convert_date(fecha))

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta') & 
                     (df['date'] == fecha)]
    
    ventas_count = df_filtered.shape[0]
    return f"Se vendieron {ventas_count} unidades de {product} el {fecha.date()}."

# Function to handle queries about purchases on a specific day
def compras_por_dia(product, fecha):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha = pd.to_datetime(convert_date(fecha))

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra') & 
                     (df['date'] == fecha)]
    
    compras_count = df_filtered.shape[0]
    return f"Se compraron {compras_count} unidades de {product} el {fecha.date()}."

def mes_con_mas_ventas(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta')]
    
    if df_filtered.empty:
        return f"No hay datos de ventas para {product}."
    
    df_filtered['month'] = df_filtered['date'].dt.to_period('M')
    df_grouped = df_filtered.groupby('month').size()
    max_ventas_month = df_grouped.idxmax()
    max_ventas_count = df_grouped.max()
    return f"El mes con más ventas de {product} fue {max_ventas_month} con {max_ventas_count} unidades vendidas."

def mes_con_mas_compras(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra')]
    
    if df_filtered.empty:
        return f"No hay datos de compras para {product}."
    
    df_filtered['month'] = df_filtered['date'].dt.to_period('M')
    df_grouped = df_filtered.groupby('month').size()
    max_compras_month = df_grouped.idxmax()
    max_compras_count = df_grouped.max()
    return f"El mes con más compras de {product} fue {max_compras_month} con {max_compras_count} unidades compradas."

def ventas_por_mes(product, mes):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    try:
        mes_dt = pd.to_datetime(mes, format='%B %Y')
    except ValueError:
        return "Formato de mes no reconocido. Por favor, usa 'mes año', e.g., 'junio 2024'."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta') & 
                     (df['date'].dt.to_period('M') == mes_dt.to_period('M'))]
    
    ventas_count = df_filtered.shape[0]
    return f"Se vendieron {ventas_count} unidades de {product} en {mes_dt.strftime('%B %Y')}."

def compras_por_mes(product, mes):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    try:
        mes_dt = pd.to_datetime(mes, format='%B %Y')
    except ValueError:
        return "Formato de mes no reconocido. Por favor, usa 'mes año', e.g., 'junio 2024'."
    
    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra') & 
                     (df['date'].dt.to_period('M') == mes_dt.to_period('M'))]
    
    compras_count = df_filtered.shape[0]
    return f"Se compraron {compras_count} unidades de {product} en {mes_dt.strftime('%B %Y')}."


# Function to handle queries about the most sold product
def producto_mas_vendido():
    df_filtered = df[df['action'] == 'venta']
    
    if df_filtered.empty:
        return "No hay datos de ventas disponibles."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    most_sold_product = product_counts.idxmax()
    most_sold_count = product_counts.max()
    
    for key, value in product_class_map.items():
        if value == most_sold_product:
            most_sold_product_name = key
    
    return f"El producto más vendido es {most_sold_product_name} con {most_sold_count} unidades vendidas."

# Function to handle queries about the least sold product
def producto_menos_vendido():
    df_filtered = df[df['action'] == 'venta']
    
    if df_filtered.empty:
        return "No hay datos de ventas disponibles."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    least_sold_product = product_counts.idxmin()
    least_sold_count = product_counts.min()
    
    for key, value in product_class_map.items():
        if value == least_sold_product:
            least_sold_product_name = key
    
    return f"El producto menos vendido es {least_sold_product_name} con {least_sold_count} unidades vendidas."

# Function to handle queries about the most purchased product
def producto_mas_comprado():
    df_filtered = df[df['action'] == 'compra']
    
    if df_filtered.empty:
        return "No hay datos de compras disponibles."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    most_bought_product = product_counts.idxmax()
    most_bought_count = product_counts.max()
    
    for key, value in product_class_map.items():
        if value == most_bought_product:
            most_bought_product_name = key
    
    return f"El producto más comprado es {most_bought_product_name} con {most_bought_count} unidades compradas."

# Function to handle queries about the least purchased product
def producto_menos_comprado():
    df_filtered = df[df['action'] == 'compra']
    
    if df_filtered.empty:
        return "No hay datos de compras disponibles."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    least_bought_product = product_counts.idxmin()
    least_bought_count = product_counts.min()
    
    for key, value in product_class_map.items():
        if value == least_bought_product:
            least_bought_product_name = key
    
    return f"El producto menos comprado es {least_bought_product_name} con {least_bought_count} unidades compradas."

# Function to handle queries about the most sold product between dates
def producto_mas_vendido_entre_fechas(fecha_inicio, fecha_fin):
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['action'] == 'venta') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]
    
    if df_filtered.empty:
        return "No hay datos de ventas disponibles en el rango de fechas especificado."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    most_sold_product = product_counts.idxmax()
    most_sold_count = product_counts.max()
    
    for key, value in product_class_map.items():
        if value == most_sold_product:
            most_sold_product_name = key
    
    return f"El producto más vendido entre {fecha_inicio.date()} y {fecha_fin.date()} es {most_sold_product_name} con {most_sold_count} unidades vendidas."

# Function to handle queries about the most purchased product between dates
def producto_mas_comprado_entre_fechas(fecha_inicio, fecha_fin):
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['action'] == 'compra') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]
    
    if df_filtered.empty:
        return "No hay datos de compras disponibles en el rango de fechas especificado."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    most_bought_product = product_counts.idxmax()
    most_bought_count = product_counts.max()
    
    for key, value in product_class_map.items():
        if value == most_bought_product:
            most_bought_product_name = key
    
    return f"El producto más comprado entre {fecha_inicio.date()} y {fecha_fin.date()} es {most_bought_product_name} con {most_bought_count} unidades compradas."

# Function to handle queries about the least sold product between dates
def producto_menos_vendido_entre_fechas(fecha_inicio, fecha_fin):
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['action'] == 'venta') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]
    
    if df_filtered.empty:
        return "No hay datos de ventas disponibles en el rango de fechas especificado."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    least_sold_product = product_counts.idxmin()
    least_sold_count = product_counts.min()
    
    for key, value in product_class_map.items():
        if value == least_sold_product:
            least_sold_product_name = key
    
    return f"El producto menos vendido entre {fecha_inicio.date()} y {fecha_fin.date()} es {least_sold_product_name} con {least_sold_count} unidades vendidas."

# Function to handle queries about the least purchased product between dates
def producto_menos_comprado_entre_fechas(fecha_inicio, fecha_fin):
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['action'] == 'compra') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]
    
    if df_filtered.empty:
        return "No hay datos de compras disponibles en el rango de fechas especificado."
    
    product_counts = df_filtered['predicted_class'].value_counts()
    least_bought_product = product_counts.idxmin()
    least_bought_count = product_counts.min()
    
    for key, value in product_class_map.items():
        if value == least_bought_product:
            least_bought_product_name = key
    
    return f"El producto menos comprado entre {fecha_inicio.date()} y {fecha_fin.date()} es {least_bought_product_name} con {least_bought_count} unidades compradas."

# Function to handle queries about returns between dates
def devoluciones_entre_fechas(product, fecha_inicio, fecha_fin):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'devolucion') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    devoluciones_count = df_filtered.shape[0]
    return f"Se devolvieron {devoluciones_count} unidades de {product} entre {fecha_inicio.date()} y {fecha_fin.date()}."

# Function to handle queries about total returns
def devoluciones_totales(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'devolucion')]

    devoluciones_totales_count = df_filtered.shape[0]
    return f"Se han devuelto {devoluciones_totales_count} unidades de {product} en total."

# Function to handle queries about current inventory
def inventario_actual(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    ventas_count = df[(df['predicted_class'] == product_class) & 
                      (df['action'] == 'venta')].shape[0]
    compras_count = df[(df['predicted_class'] == product_class) & 
                       (df['action'] == 'compra')].shape[0]
    inventario = compras_count - ventas_count
    return f"El inventario actual de {product} es de {inventario} unidades."

# Function to handle queries about sales this week
def ventas_esta_semana(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_fin = pd.to_datetime(datetime.now().date())
    fecha_inicio = fecha_fin - pd.DateOffset(days=7)

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    ventas_count = df_filtered.shape[0]
    return f"Se vendieron {ventas_count} unidades de {product} esta semana."

# Function to handle queries about purchases this week
def compras_esta_semana(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_fin = pd.to_datetime(datetime.now().date())
    fecha_inicio = fecha_fin - pd.DateOffset(days=7)

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    compras_count = df_filtered.shape[0]
    return f"Se compraron {compras_count} unidades de {product} esta semana."

# Function to handle queries about sales this month
def ventas_este_mes(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_fin = pd.to_datetime(datetime.now().date())
    fecha_inicio = fecha_fin - pd.DateOffset(days=30)

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'venta') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    ventas_count = df_filtered.shape[0]
    return f"Se vendieron {ventas_count} unidades de {product} este mes."

# Function to handle queries about purchases this month
def compras_este_mes(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    fecha_fin = pd.to_datetime(datetime.now().date())
    fecha_inicio = fecha_fin - pd.DateOffset(days=30)

    df_filtered = df[(df['predicted_class'] == product_class) & 
                     (df['action'] == 'compra') & 
                     (df['date'] >= fecha_inicio) & 
                     (df['date'] <= fecha_fin)]

    compras_count = df_filtered.shape[0]
    return f"Se compraron {compras_count} unidades de {product} este mes."

# Function to handle queries about average price of a product
def precio_promedio(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[df['predicted_class'] == product_class]
    
    if 'price' not in df.columns or df_filtered['price'].isnull().all():
        return f"No hay datos de precios disponibles para {product}."
    
    average_price = df_filtered['price'].mean()
    return f"El precio promedio de {product} es {average_price:.2f} unidades monetarias."

# Function to handle queries about maximum price of a product
def precio_maximo(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[df['predicted_class'] == product_class]
    
    if 'price' not in df.columns or df_filtered['price'].isnull().all():
        return f"No hay datos de precios disponibles para {product}."
    
    max_price = df_filtered['price'].max()
    return f"El precio máximo de {product} es {max_price:.2f} unidades monetarias."

# Function to handle queries about minimum price of a product
def precio_minimo(product):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."
    
    df_filtered = df[df['predicted_class'] == product_class]
    
    if 'price' not in df.columns or df_filtered['price'].isnull().all():
        return f"No hay datos de precios disponibles para {product}."
    
    min_price = df_filtered['price'].min()
    return f"El precio mínimo de {product} es {min_price:.2f} unidades monetarias."

# Function to handle queries about inventory between dates
def inventario_entre_fechas(product, fecha_inicio, fecha_fin):
    product_class = product_class_map.get(product.lower())
    if not product_class:
        return f"Producto '{product}' no reconocido."

    fecha_inicio = pd.to_datetime(convert_date(fecha_inicio))
    fecha_fin = pd.to_datetime(convert_date(fecha_fin))

    ventas_count = df[(df['predicted_class'] == product_class) & 
                      (df['action'] == 'venta') & 
                      (df['date'] >= fecha_inicio) & 
                      (df['date'] <= fecha_fin)].shape[0]
    compras_count = df[(df['predicted_class'] == product_class) & 
                       (df['action'] == 'compra') & 
                       (df['date'] >= fecha_inicio) & 
                       (df['date'] <= fecha_fin)].shape[0]
    inventario = compras_count - ventas_count
    return f"El inventario de {product} entre {fecha_inicio.date()} y {fecha_fin.date()} es de {inventario} unidades."

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
        (r"cuántas (\w+) se han comprado", compras_totales),
        (r"cuál es el promedio de ventas diarias de (\w+) del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", promedio_ventas_diarias),
        (r"cuál es el total de (\w+) vendidas hasta ahora", ventas_totales),
        (r"cuál es el total de (\w+) compradas hasta ahora", compras_totales),
        (r"cuál fue el día con más ventas de (\w+)", dia_con_mas_ventas),
        (r"cuál fue el día con más compras de (\w+)", dia_con_mas_compras),
        (r"cuántas (\w+) se vendieron en (\d{1,2} de [a-z]+)", ventas_por_dia),
        (r"cuántas (\w+) se compraron en (\d{1,2} de [a-z]+)", compras_por_dia),
        (r"cuál es el producto más vendido", producto_mas_vendido),
        (r"cuál es el producto menos vendido", producto_menos_vendido),
        (r"cuál es el producto más comprado", producto_mas_comprado),
        (r"cuál es el producto menos comprado", producto_menos_comprado),
        (r"cuál es el promedio de compras diarias de (\w+) del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", promedio_compras_diarias),
        (r"cuál es el total de ventas de (\w+) en (\d{1,2} de [a-z]+)", ventas_por_dia),
        (r"cuál es el total de compras de (\w+) en (\d{1,2} de [a-z]+)", compras_por_dia),
        (r"cuál fue el mes con más ventas de (\w+)", mes_con_mas_ventas),
        (r"cuál fue el mes con más compras de (\w+)", mes_con_mas_compras),
        (r"cuántos (\w+) se vendieron en (\w+)", ventas_por_mes),
        (r"cuántas (\w+) se vendieron en (\w+)", ventas_por_mes),
        (r"cuántos (\w+) se compraron en (\w+)", compras_por_mes),
        (r"cuántas (\w+) se compraron en (\w+)", compras_por_mes),
        (r"cuál es el producto más vendido entre (\d{1,2} de [a-z]+) y (\d{1,2} de [a-z]+)", producto_mas_vendido_entre_fechas),
        (r"cuál es el producto más comprado entre (\d{1,2} de [a-z]+) y (\d{1,2} de [a-z]+)", producto_mas_comprado_entre_fechas),
        (r"cuál es el producto menos vendido entre (\d{1,2} de [a-z]+) y (\d{1,2} de [a-z]+)", producto_menos_vendido_entre_fechas),
        (r"cuál es el producto menos comprado entre (\d{1,2} de [a-z]+) y (\d{1,2} de [a-z]+)", producto_menos_comprado_entre_fechas),
        (r"cuántos (\w+) se devolvieron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", devoluciones_entre_fechas),
        (r"cuántas (\w+) se devolvieron del (\d{1,2} de [a-z]+) al (\d{1,2} de [a-z]+)", devoluciones_entre_fechas),
        (r"cuántos (\w+) se han devuelto", devoluciones_totales),
        (r"cuántas (\w+) se han devuelto", devoluciones_totales),
        (r"cuántos (\w+) hay en inventario", inventario_actual),
        (r"cuántas (\w+) hay en inventario", inventario_actual),
        (r"cuántos (\w+) se vendieron esta semana", ventas_esta_semana),
        (r"cuántas (\w+) se vendieron esta semana", ventas_esta_semana),
        (r"cuántos (\w+) se compraron esta semana", compras_esta_semana),
        (r"cuántas (\w+) se compraron esta semana", compras_esta_semana),
        (r"cuántos (\w+) se vendieron este mes", ventas_este_mes),
        (r"cuántas (\w+) se vendieron este mes", ventas_este_mes),
        (r"cuántos (\w+) se compraron este mes", compras_este_mes),
        (r"cuántas (\w+) se compraron este mes", compras_este_mes),
        (r"cuál es el precio promedio de (\w+)", precio_promedio),
        (r"cuál fue el precio máximo de (\w+)", precio_maximo),
        (r"cuál fue el precio mínimo de (\w+)", precio_minimo),
        (r"cuál es el inventario de (\w+) entre (\d{1,2} de [a-z]+) y (\d{1,2} de [a-z]+)", inventario_entre_fechas)
    ]

    # Check if the input matches any of the patterns
    for pattern, func in patterns:
        match = re.match(pattern, user_input)
        if match:
            params = match.groups()
            return func(*params)
    
    return "Lo siento, no entendí eso. Por favor, haz una pregunta relacionada con los datos de ventas o saluda."

def simulate_conversation():
    inputs = [
        "hola",
        "cuál fue el mes con más ventas de refrigeradores",
        "cuál fue el mes con más compras de televisores",
        "cuántos microondas se vendieron en junio 2024",
        "cuántas secadoras se compraron en mayo 2024",
        "cuántos refrigeradores se devolvieron del 1 de enero al 31 de enero",
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
