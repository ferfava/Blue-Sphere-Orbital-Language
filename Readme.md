Project Blue Sphere: Orbital Data Analytics & NLP
Módulo de investigación para la tesis: Echo-Spatial

Descripción
Project Blue Sphere es una iniciativa técnica centrada en el análisis de telemetría satelital mediante técnicas de Procesamiento de Lenguaje Natural (PLN). El proyecto propone un cambio de paradigma: tratar los flujos de datos orbitales no como simples números, sino como un corpus lingüístico con gramática y semántica propias.

A través de este enfoque, se desarrolla la "Arqueología Sonora de Datos" (Echo-Spatial), permitiendo la interpretación de estados físicos de satélites (como el LightSail-2) mediante una sonificación paramétrica y auditada.

Tecnologías Utilizadas
Procesamiento de Datos: Python (NumPy, SciPy).

Fuentes de Información: Red SatNOGS (Telemetría cruda en tiempo real).

Visualización y Auditoría: Matplotlib para validación de patrones.

Ingeniería de Sonido: Síntesis de ondas para representación semántica de sensores.

Estructura del Repositorio
src/ingestion/: Módulos para la captura de datos desde APIs satelitales.

src/nlp_engine/: Núcleo de procesamiento donde se realiza la tokenización de frames y la sonificación de los datos.

data/raw/: Almacenamiento de frames hexadecimales originales.

data/processed/: Salidas de auditoría, logs de frecuencia y archivos de audio generados.

Cómo ejecutar el proyecto
Instalar las dependencias: pip install -r requirements.txt

Ejecutar la ingesta: python src/ingestion/ingestion.py

Generar la sonificación: python src/nlp_engine/sonificador_deconstructor.py
