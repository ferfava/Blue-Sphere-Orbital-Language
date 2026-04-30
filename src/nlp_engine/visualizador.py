import json
import matplotlib.pyplot as plt
import os

PATH = 'data/raw/noaa15_raw.json'

def validar_datos():
    if not os.path.exists(PATH):
        print("❌ No encuentro el archivo de datos. Corré el ingestion.py primero.")
        return

    with open(PATH, 'r') as f:
        data = json.load(f)
    
    # Tomamos el primer paquete (frame)
    frame_hex = data[0]['frame']
    
    # Convertimos cada par hexadecimal a un número decimal (0-255)
    # Estos son los valores que "suenan" en tu audio
    valores = [int(frame_hex[i:i+2], 16) for i in range(0, len(frame_hex), 2)]
    
    # Creamos el gráfico
    plt.figure(figsize=(12, 5))
    plt.plot(valores, color='#0078d4', linewidth=2, marker='o', markersize=4)
    
    # Anotaciones para tu defensa de tesis
    plt.axvspan(0, 10, color='red', alpha=0.1, label='Cabecera (ID/Protocolo)')
    plt.axvspan(10, 40, color='green', alpha=0.1, label='Telemetría (Batería/Sensores)')
    
    plt.title('Análisis de Estructura Orbital: LightSail-2', fontsize=14)
    plt.xlabel('Posición del Byte (Tiempo)', fontsize=12)
    plt.ylabel('Valor Decimal (Frecuencia)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    print("📊 Generando visualización... Debería abrirse una ventana nueva.")
    plt.show()

if __name__ == "__main__":
    validar_datos()