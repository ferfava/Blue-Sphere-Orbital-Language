import json
import os

INPUT_PATH = "data/raw/noaa15_raw.json"
OUTPUT_PATH = "data/processed/orbital_corpus.txt"

def generar_corpus():
    try:
        with open(INPUT_PATH, 'r') as f:
            data = json.load(f)
        
        frames = []
        for paquete in data:
            frame = paquete.get('frame')
            if frame:
                # Opcional: Podés separar cada byte con un espacio 
                # para que parezcan "palabras" para la IA
                palabras = " ".join([frame[i:i+2] for i in range(0, len(frame), 2)])
                frames.append(palabras)
        
        os.makedirs('data/processed', exist_ok=True)
        with open(OUTPUT_PATH, 'w') as f:
            f.write("\n".join(frames))
            
        print(f"✅ Corpus generado exitosamente en {OUTPUT_PATH}")
        print(f"📄 Se procesaron {len(frames)} oraciones satelitales.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generar_corpus()