# Introducción al Procesamiento Digital de Imágenes (PDI)

Espacio para subir los trabajos prácticos de la materia 

# Ejecutar el proyecto 📋

## Paso 1. Activar entorno virtual 

### 1.1 Debe crear el entorno virtual usando virtualenv 

```bash
virtualenv env
```

### 1.2 Activar entorno
```bash
env\Scripts\activate
```

### 1.3 Instalar las librerias requeridas. Realizar este paso cada vez que se agregan librerias.
```bash
pip install -r requirements.txt
```
# Trabajo Practico N 1

Mostrar una imagen RGB en YIQ

# Trabajo Practico N 2

Realizar operaciones aritmeticas con 2 imagenes de igual tamaño. La interfaz cuenta con imagenes de ejemplos. En caso de querer seleccionar una imagen de su directorio puede descargar de la carpeta imagenes los archivos __image1.png__ y __image2.png__.

```bash
python TP2-OperacionesAritmeticas.py
```
![tp2-suma](https://res.cloudinary.com/dvxigug6q/image/upload/v1715258552/IPDI-2023/ttr1rfryr3v6ebidfhao.png)
# Trabajo Practico N 3

Realizar operaciones sobre el histograma de luminancias aplicando funciones de raiz cuadrada, exponencial o lineal a trozos sobre la imagen. La interfaz cuenta con la seleccion de una imagen para calcular su histograma segun diferentes contadores y tambien la imagen resultante aplicando los filtros disponibles.

```bash
python TP3-OperacionesLuminancia.py
```
![tp3-frecuencia](https://res.cloudinary.com/dvxigug6q/image/upload/v1715258808/IPDI-2023/ahgwzhypykibxebr7j6f.png)

# Trabajo Practico N 4

Cargar una imagen en tonos de gris, convirtiendo la misma a YIQ y manteniendo solo la banda de luminancia Y. Al resutado aplicar el filtrado por convolucion pasabajos, detectores de bordes y pasabanda.

```bash
python TP4-Convolucion.py
```
![tp4-convolucion](https://res.cloudinary.com/dvxigug6q/image/upload/v1715259028/IPDI-2023/dbz56esohbuz5b5zk0bk.png)

# Trabajo Practico N 5

Aplicar operaciones basicas de morfologia binaria a una imagen. Se incluye la capacidad de copiar la componente de la imagen procesada en la componente original, para poder aplicar dos o más filtrados en secuencia.

```bash
python TP5-Morfologia.py
```
![tp5-morfo](https://res.cloudinary.com/dvxigug6q/image/upload/v1715260746/IPDI-2023/l2rhjrxmnjxtabudde36.png)

# Ejercicio Ponds

Determina el área de los cuencos y arroyos que forman parte del agua acumulada en la playa. Para ello se aplicó ecualización de la imagen, segmentación con Método MeanShift, Binarización con Método de Otsu y detección de contornos con el algoritmo Teh-Chin Chain.

![ponds](https://res.cloudinary.com/dvxigug6q/image/upload/v1715261086/IPDI-2023/pd03rbmfynrdp8jes6oi.png)


# TPFinal - Diagnóstico Automático de Tuberculosis en Radiografías de Tórax aplicando Machine Learning

Determina una máscara para la segmentación de los pulmones aplicando ténicas de morfología, segmentación y binarización

![pulmones](https://res.cloudinary.com/dvxigug6q/image/upload/v1715261293/IPDI-2023/rqurcaixdn7uli8hsxtu.png)