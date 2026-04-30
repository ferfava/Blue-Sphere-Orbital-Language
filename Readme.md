# Blue Sphere: Inteligencia de Señales Aplicada a la Gestión de Activos Aeroespaciales

## 🛰️ Visión General
**Blue Sphere** es un framework de auditoría técnica y monitoreo preventivo diseñado para la interceptación y análisis de telemetría satelital. El proyecto propone una metodología innovadora basada en la **sonificación** y el **procesamiento en el dominio de la frecuencia** para identificar anomalías en sistemas complejos donde los métodos de auditoría lineal tradicionales pueden resultar insuficientes.

## 🛠️ Objetivos del Proyecto
1. **Auditoría Forense Automática:** Implementar un motor de clasificación basado en la Transformada Rápida de Fourier (FFT) para etiquetar estados operativos en tiempo real.
2. **SIGINT (Signal Intelligence):** Interceptar y procesar flujos de datos provenientes de la red global de estaciones terrestres SatNOGS.
3. **Resiliencia de Datos:** Garantizar la continuidad del monitoreo mediante un sistema de *failover* inteligente que alterna entre captura en vivo y procesamiento de registros históricos ante fallos de red.
4. **Visualización de Diagnóstico:** Generar espectrogramas de alta precisión para la validación visual de firmas espectrales.

## 🧬 Metodología Técnica
El núcleo del sistema transforma la telemetría binaria (Hexadecimal) en señales acústicas, permitiendo detectar patrones rítmicos y variaciones de energía. 

- **Frecuencia de Muestreo (Sample Rate):** 22.05 kHz (Optimizado para eficiencia de recursos).
- **Algoritmo de Detección:** Análisis de picos de frecuencia dominante para la clasificación de frames (Health, Payload o Anomaly).
- **Integración API:** Conexión dinámica con bases de datos de misiones aeroespaciales.

## 📊 Resultados Recientes (Caso de Estudio: METEOR-M2)
Durante las pruebas de validación, **Blue Sphere** identificó con éxito:
- **Transmisiones Nominales:** Flujos estables de datos de carga útil.
- **Anomalías Críticas:** Desviaciones en la firma espectral en frames específicos (ej. Frame 03, 04), lo que permitió una identificación inmediata de eventos de interferencia o cambios de estado no programados.

## 📂 Estructura del Repositorio
- `src/`: Motores de procesamiento y lógica de auditoría.
- `data/`: Estructuras de datos para respaldo local.
- `output/`: Registro de evidencias (Audios y Espectrogramas).

---
*Este proyecto se desarrolla en el marco de investigación sobre nuevas tecnologías de gestión y auditoría en sistemas aeroespaciales.*
