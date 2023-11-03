import math

import hashlib

def cifrar_transposicion(mensaje, clave):
    key = len(clave)
    textoCifrado = [''] * key
    for col in range(key):
        apuntador = col
        while apuntador < len(mensaje):
            textoCifrado[col] += mensaje[apuntador]
            apuntador += key
    return ''.join(textoCifrado)

def descifrar_transposicion(mensaje_cifrado, clave):
    key = len(clave)
    numCols = math.ceil(len(mensaje_cifrado) / key)
    numFil = key
    numVacios = (numCols * numFil) - len(mensaje_cifrado)
    textoDescifrado = [""] * numCols
    col = 0; fila = 0;

    for symbol in mensaje_cifrado:
        textoDescifrado[col] += symbol
        col += 1

        if (col == numCols) or (col == numCols - 1) and (fila >= numFil - numVacios):
            col = 0
            fila += 1

    return "".join(textoDescifrado)
    
    
def hash_mensaje(mensaje):
    mensaje_bytes = mensaje.encode('utf-8')

    sha256 = hashlib.sha256()

    sha256.update(mensaje_bytes)

    hash_hexadecimal = sha256.hexdigest()

    return hash_hexadecimal

    
def firmar_mensaje(mensaje_hash_hex, clave_privada):
    mensaje_hash = int(mensaje_hash_hex, 16)

    firma = mensaje_hash * clave_privada
    return firma

"""
mensaje = "Et adipisci ut et nihil. Et itaque totam nam et fugit quibusdam nihil iusto odio. Non voluptatibus error et iusto."
clave = "9887670048572"
mensaje_cif = cifrar_transposicion(mensaje, clave)
mensaje_des = descifrar_transposicion(mensaje_cif, clave)
print("Mensaje Cifrado: ", mensaje_cif)
print("Mensaje descifrado:", mensaje_des)

"""