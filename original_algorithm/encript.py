#pip install opencv-python
import cv2 as cv 
import numpy as np

def encriptar(desde, hasta, final):
    # Leemos archivo
    with open(desde, "rb") as f: data = f.read()

    # Extension
    extension_archivo = extension(desde)
    array_extension = []
    if extension_archivo != None:
        array_extension = list(extension_archivo.encode("latin-1"))
    extension_lenght = len(array_extension)


    # Tamaños
    tam_bytes = len(array_extension) + len(data) + len(final) # n bytes que va a contener la imagen
    n_pixels = int(np.ceil(tam_bytes / 3))
    lado = int(np.ceil(np.sqrt(n_pixels)))

    img_bytes = []
    for i in range(len(data)): img_bytes.append(data[i]) # Datos del archivo
    img_bytes += final + [extension_lenght] + array_extension # Aniade contrasenia, num de chars de la extension, y la extension sin punto
    
    # Img es una matriz de lado x lado x 3
    img = np.zeros((lado, lado, 3), dtype=np.uint8) # Rojo: [0, 0, 0], Verde: [0, 0, 1], Azul: [0, 0, 2]

    # Rellenamos la imagen con los bytes del archivo
    c = 0
    for i in range(lado):
        for j in range(lado):
            for k in range(3):
                if c < len(img_bytes):
                    img[i][j][k] = img_bytes[c]
                    c += 1
                else:
                    img[i][j][k] = np.random.randint(0, 256)

    # Creamos una imagen con nuestra matriz
    cv.imwrite(hasta, img)
    print("Archivo encriptado guardado como \"encripted.png\"")


# Devuelve la extension sin el punto, o "" si no la tiene
def extension(nombre_archivo):
    if "." in nombre_archivo:
        return nombre_archivo.split(".")[-1]
    else:
        return ""

# Pregunta por la contraseña, comprueba que sea de >=3 caracteres y que sean validos
# Devuelve un array de ints
# Podría convertir la contraseña en un hash o algo parecido, así no se adivinará por casualidad // TODO
def contrasenia():
    while True:
        password = input("Introduce tu contraseña: ")
        try:
            array_numeros = list(password.encode("latin-1"))
            if len(array_numeros) < 3:
                print("La contraseña debe tener al menos 3 caracteres.")
                continue
            return array_numeros
        except UnicodeEncodeError:
            print("Error: La contraseña contiene caracteres que no caben en el rango 0-255 (como emojis).")

# Bucla intentando abrir un archivo. Cuando lo consigue, devuelve el nombre del archivo (solo nombre.extension)
def archivo():
    while True:
        ruta = input("Archivo a encriptar: ")
        
        try:
            with open(ruta, "rb"): return ruta
        except FileNotFoundError:
            print("Error: El archivo no existe. Por favor, introduce un nombre de archivo válido.")

def main():
    encriptar(archivo(), "encripted.png", contrasenia())
    end = input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()