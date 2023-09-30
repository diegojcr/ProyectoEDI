#diccionario_ascii = ["NUL","SOH","STX","ETX","EOT","ENQ","ACK","BEL","BS","HT","LF","VT","FF","CR","SO","SI","DLE","DC1","DC2","DC3","DC4","NAK","SYN","ETB","CAN","EM","SUB","ESC","FS","GS","RS","US"," ","!","'","#","$","%","&","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","¿","Á","É","Í","Ó","Ú","Ä","Ë","Ï","Ö","Ü","Ñ","ñ","/","¡","á","é","í","ó","ú"]
def comprimir(frase, diccionario):
    w = ""
    b = 0
    salida = []
    while(b<len(frase)):
        k = frase[b]
        wk = w +k
        if(wk in diccionario):
            w = wk
            b = b+1
        else:
            indice = diccionario.index(w)
            salida.append(indice)
            diccionario.append(wk)
            w=k
            b = b+1 
    indice = diccionario.index(w)
    salida.append(indice)
    return salida

def descomprimir(salida,diccionario):
    res = []
    i = 0
    cod_viejo = salida[i]
    caracter = diccionario[cod_viejo]
    res.append(caracter)
    i+=1
    while (i < len(salida)):
        cod_nuevo = salida[i]
        if(cod_nuevo not in diccionario):
            cadena = diccionario[cod_nuevo]
            res.append(cadena)
            caracter = cadena[0]
            diccionario.append(diccionario[cod_viejo] + caracter)
            cod_viejo = cod_nuevo
            i+=1
        else:
            cadena = diccionario[cod_viejo]
            cadena = cadena + caracter
            i+=1
    return res

""""

import os
os.chdir('C:/Users/Diego/Desktop')

libro = open('pruebalzw.txt')

frase = []
texto = libro.read()
for i in texto:
    frase.append(i)

a = comprimir(frase,diccionario_ascii)

b = descomprimir(a,diccionario_ascii)

print(a)
print(b)
"""