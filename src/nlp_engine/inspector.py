import json

PATH = "data/raw/noaa15_raw.json"

def inspeccionar_extremo():
    try:
        with open(PATH, 'r') as f:
            data = json.load(f)
        
        print(f"Tipo de dato principal: {type(data)}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"📦 Primer elemento es de tipo: {type(data[0])}")
            print("--- CONTENIDO CRUDO DEL PRIMER ELEMENTO ---")
            # Esto nos va a mostrar la verdad:
            print(json.dumps(data[0], indent=2))
            print("-------------------------------------------")
        else:
            print(f"⚠️ El contenido no es una lista o está vacío: {data}")
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    inspeccionar_extremo()