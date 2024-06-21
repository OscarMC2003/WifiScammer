from cryptography.fernet import Fernet

clave = open("clave.key", "rb").read()

def generar_clave():
    print("Generando clave...")
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def desencriptar_archivo(nombre_archivo, clave):
    print("Desencriptando archivo...")
    fernet = Fernet(clave)
    with open(nombre_archivo, "rb") as archivo_encriptado:
        datos_encriptados = archivo_encriptado.read()
    datos_desencriptados = fernet.decrypt(datos_encriptados)
    with open(nombre_archivo[:-10], "wb") as archivo_desencriptado:
        archivo_desencriptado.write(datos_desencriptados)

#generar_clave()
nombre_archivo = input("Por favor, ingrese el nombre del archivo: ")
desencriptar_archivo(nombre_archivo, clave)