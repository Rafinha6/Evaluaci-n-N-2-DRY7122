import requests
import json

TOKEN = '7a81a7d9-3b46-4e5d-af81-577c7b688d65'

def obtener_coordenadas(ciudad):
    url = f'https://graphhopper.com/api/1/geocode?q={ciudad}&key={TOKEN}'
    response = requests.get(url)
    data = response.json()
    if 'hits' in data and len(data['hits']) > 0:
        coordenadas = data['hits'][0]['point']
        return coordenadas['lat'], coordenadas['lng']
    else:
        raise Exception(f'No se encontraron coordenadas para la ciudad: {ciudad}')

def obtener_ruta(origen, destino):
    lat_origen, lon_origen = obtener_coordenadas(origen)
    lat_destino, lon_destino = obtener_coordenadas(destino)
    url = f'https://graphhopper.com/api/1/route?point={lat_origen},{lon_origen}&point={lat_destino},{lon_destino}&vehicle=car&locale=es&key={TOKEN}'
    response = requests.get(url)
    data = response.json()
    return data['paths'][0]

def calcular_combustible(distancia_km):
    consumo_por_km = 0.1
    return distancia_km * consumo_por_km

def main():
    while True:
        print("\nMenú de Opciones")
        print("1. Medir la distancia entre dos ciudades")
        print("2. Mostrar la duración del viaje")
        print("3. Mostrar el combustible requerido para el viaje")
        print("4. Imprimir la narrativa del viaje")
        print("5. Imprimir la ruta")
        print("q. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == 'q':
            break
        elif opcion in ['1', '2', '3', '4', '5']:
            origen = input("Ciudad de Origen: ")
            destino = input("Ciudad de Destino: ")
            
            try:
                ruta = obtener_ruta(origen, destino)
                distancia_km = ruta['distance'] / 1000.0
                duracion_segundos = ruta['time'] / 1000.0
                horas = int(duracion_segundos // 3600)
                minutos = int((duracion_segundos % 3600) // 60)
                segundos = int(duracion_segundos % 60)
                combustible = calcular_combustible(distancia_km)
                
                if opcion == '1':
                    print(f"Distancia entre {origen} y {destino}: {distancia_km:.2f} km")
                elif opcion == '2':
                    print(f"Duración del viaje: {horas} horas, {minutos} minutos, {segundos} segundos")
                elif opcion == '3':
                    print(f"Combustible requerido: {combustible:.2f} litros")
                elif opcion == '4':
                    print(f"Viaje de {origen} a {destino}:")
                    print(f"  Distancia: {distancia_km:.2f} km")
                    print(f"  Duración: {horas} horas, {minutos} minutos, {segundos} segundos")
                    print(f"  Combustible: {combustible:.2f} litros")
                elif opcion == '5':
                    print("Ruta:")
                    for instruccion in ruta['instructions']:
                        print(f"  {instruccion['text']}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Opción no válida, por favor seleccione nuevamente.")

if __name__ == "__main__":
    main()


