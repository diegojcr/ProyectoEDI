import math
import Keys
import hashlib
from io import StringIO

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


def encriptar(privada, contra, p, q):
    key = privada
    n = p * q
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
            
    numberRepr = [ord(char) for char in contra]
    cipher = [pow(ord(char),key,n) for char in contra]
    
    #Return the array of bytes
    return cipher

def desencriptar(publica, encriptado, p, q):
    key = publica
    n = p * q
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    numberRepr = [pow(char, key, n) for char in encriptado]
    plain = [chr(pow(char, key, n)) for char in encriptado]

    
    #Return the array of bytes as a string
    return ''.join(plain)


def comprimir(no_comprimido):
        """"""

        # Construir el diccionario.
        tamaño_diccionario = 1000
        diccionario = dict((chr(i), chr(i)) for i in range(tamaño_diccionario))

        w = ""
        resultado = []
        for c in no_comprimido:
            wc = w + c
            if wc in diccionario:
                w = wc
            else:
                resultado.append(diccionario[w])
                # Agregar wc al diccionario.
                diccionario[wc] = tamaño_diccionario
                tamaño_diccionario += 1
                w = c

        # Salida del código para w.
        if w:
            resultado.append(diccionario[w])
        return resultado


def descomprimir(comprimido):
    tamaño_diccionario = 1000
    diccionario = dict((chr(i), chr(i)) for i in range(tamaño_diccionario))

    resultado = StringIO()
    w = comprimido.pop(0)
    resultado.write(w)
    for k in comprimido:
        if k in diccionario:
            entrada = diccionario[k]
        elif k == tamaño_diccionario:
            entrada = w + w[0]
        else:
            raise ValueError('No se puede descomprimir: %s' % k)
        resultado.write(entrada)

        diccionario[tamaño_diccionario] = w + entrada[0]
        tamaño_diccionario += 1

        w = entrada
    return resultado.getvalue()






"""
mensaje = "Et adipisci ut et nihil. Et itaque totam nam et fugit quibusdam nihil iusto odio. Non voluptatibus error et iusto."
p, q = Keys.generar_primos_aleatorios()
clave_publica, clave_privada = Keys.generate_keypair(p,q)
clave = "9887670048572"
mensaje_cif = encriptar(clave_privada, mensaje, p, q)
mensaje_des = desencriptar(clave_publica, mensaje_cif, p, q)
print("Mensaje Cifrado: ", mensaje_cif)
print("Mensaje descifrado:", mensaje_des)
"""
