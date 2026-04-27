import cv2 as cv
# Falta que lea la extensión del archivo después de la contraseña y coger el "guardar como", 
# trimmear la extensión y guardarla con la extensión correcta

# Recibe el archivo a desencriptar con su extensión, el nombre del archivo sin la extensión y un array numérico con la contraseña
# Escribe el archivo desencriptado
def desencriptar(desde, hasta, contrasenia):
    # Leemos la imagen
    img = cv.imread("ENCRIPTING/" + desde)
    datos = []
    buffer = []

    extension_array = []
    leyendo_extension = False
    extension_long = 0
    extension_contador = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                byte = int(img[i][j][k]) # El byte que estamos leyendo

                if not leyendo_extension: # Leemos el contenido del archivo a formar
                    if buffer: # Si ya hay algo en el buffer, seguir añadiendo
                        buffer.append(byte)
                    elif byte == contrasenia[0]: # Si byte coincide con el inicio de la contraseña, empezamos a llenar el buffer
                        buffer = [byte]
                    else: # Si no, son datos normales
                        datos.append(byte)

                    if len(buffer) == len(contrasenia): # Comprobación del buffer
                        if buffer == contrasenia: # Si se encuentra la contraseña, se ha terminado de leer los datos y se empieza con la extensión
                            leyendo_extension = True
                        else: # Si no, se añaden el buffer a los datos, se vacía y se sigue leyendo
                            datos.extend(buffer)
                            buffer = []

                elif leyendo_extension: # Empezamos a leer la extension
                    if extension_contador == 0: extension_long = byte # Si no hemos leído la longitud de la extensión, la guardamos
                    elif extension_contador < extension_long+1: # Seguimos leyendo
                        extension_array.append(byte)
                    elif extension_contador == extension_long+1: # Hemos acabo de leer la extensión
                        extension = bytes(extension_array).decode("latin-1")
                        # Fin de los datos
                        with open("ENCRIPTING/" + hasta + "." + extension, "wb") as f:
                            f.write(bytearray(datos))
                        print("Contraseña correcta. Archivo desencriptado guardado como \"%s\"." % (hasta + "." + extension))
                        return
                    extension_contador += 1

    print("Contraseña incorrecta. No se pudo desencriptar el archivo.")

def contrasenia():
    while True:
        password = input("Introduce la contraseña: ")
        try:
            array_numeros = list(password.encode("latin-1"))
            return array_numeros
        except UnicodeEncodeError:
            print("Error: La contraseña contiene caracteres que no caben en el rango 0-255 (como emojis).")

# Crea un archivo para el resultado y devuelve su nombre sin la extensión  
def archivo():
    while True:
        # nombre_archivo_completo = input("Nombre del archivo desencriptado: ")
        nombre_archivo_completo = "decrypt"
        nombre_archivo_split = nombre_archivo_completo if len(nombre_archivo_completo.split(".")) == 1 else nombre_archivo_completo.split(".")[-2]

        try:
            with open('ENCRIPTING/' + nombre_archivo_completo, "wb"): return nombre_archivo_split
        except Exception as e:
            print(f"Error con el nombre del archivo: {e}")

# Comprueba que pueda abrir el archivo a desencriptar y devuelve su nombre con extensión
def archivo_encript():
    try:
        with open("ENCRIPTING/encript.png", "rb"): return "encript.png"
    except FileNotFoundError:
        end = input("Error: El archivo \"encript.png\" no existe en ENCRIPTING/encript.png.\nEl programa se cerrará.\nPresiona Enter para salir...")
        exit(1)

def main():
    desencriptar(archivo_encript(), archivo(), contrasenia())
    end = input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()