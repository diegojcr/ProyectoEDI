import json
import Controller
import os
import glob
import re
import Keys


class BTreeNode(object):
  
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.c = []
        self.data = []
        
    def __str__(self):
        if self.leaf:
            return "Leaf BTreeNode with {0} keys\n\tK:{1}\n\tData:{2}\n".format(len(self.keys), self.keys, self.data)
        else:
            return "Internal BTreeNode with {0} keys, {1} children\n\tK:{2}\n\n".format(len(self.keys), len(self.c), self.keys)


class BTree(object):
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        self.t = t
    
    def search(self, k, x=None):
        
        if isinstance(x, BTreeNode):
            i = 0
            while i < len(x.keys):  # look for index of k
                if k == x.keys[i]:
                    return (x, i)
                i += 1
            
            if x.leaf:  # no match in keys, and is leaf ==> no match exists
                return None
            else:  # search children
                return self.search(k, x.c[i])
        else:  # no node provided, search root of tree
            return self.search(k, self.root)
    
    def searchByName(self, name, x=None):
        if x is None:
            x = self.root

        i = 0
        while i < len(x.keys):
            if name == x.data[i]['name']:
                return (x,i)
            i += 1
        
        if x.leaf:
            return None
        else:
            return self.searchByName(name, x.c[i])
    
    
    def insert(self, k, data):
        r = self.root
        if len(r.keys) == (2 * self.t) - 1:  # keys are full, so we must split
            s = BTreeNode()
            self.root = s
            s.c.insert(0, r)  # former root is now 0th child of new root s
            self._split_child(s, 0)
            self._insert_nonfull(s, k, data)
        else:
            self._insert_nonfull(r, k, data)
    
    def _insert_nonfull(self, x, k, data):
        i = len(x.keys) - 1
        if x.leaf:
            # insert a key
            x.keys.append(0)
            x.data.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                x.data[i + 1] = x.data[i]
                i -= 1
            x.keys[i + 1] = k
            x.data[i + 1] = data
        else:
            # insert a child
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.c[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.c[i], k, data)
    
    def _split_child(self, x, i):
        t = self.t
        y = x.c[i]
        z = BTreeNode(leaf=y.leaf)
        
        # slide all children of x to the right and insert z at i+1.
        x.c.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        x.data.insert(i, y.data[t - 1])
        
        # keys of z are t to 2t - 1,
        # y is then 0 to t-2
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        
        z.data = y.data[t:(2 * t - 1)]
        y.data = y.data[0:(t - 1)]
        
        # children of z are t to 2t els of y.c
        if not y.leaf:
            z.c = y.c[t:(2 * t)]
            y.c = y.c[0:(t - 1)]
    
    

    def list_clients(self):
        clients = []
        self._inorder_traversal(self.root, clients)
        return clients

    def _inorder_traversal(self, node, clients):
        if node:
            if not node.leaf:
                for i in range(len(node.c)):
                    self._inorder_traversal(node.c[i], clients)
            for i in range(len(node.keys)):
                clients.append(node.data[i])



    #diccionario_ascii = ["NUL","SOH","STX","ETX","EOT","ENQ","ACK","BEL","BS","HT","LF","VT","FF","CR","SO","SI","DLE","DC1","DC2","DC3","DC4","NAK","SYN","ETB","CAN","EM","SUB","ESC","FS","GS","RS","US"," ","!","'","#","$","%","&","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","¿","Á","É","Í","Ó","Ú","Ä","Ë","Ï","Ö","Ü","Ñ","ñ","/","¡","á","é","í","ó","ú"]

    def cargarJson():

        # Cargar datos desde un archivo JSONL
        with open('C:/Users/Diego/Desktop/input4.json', 'r') as jsonl_file:
            for line in jsonl_file:
                #insert data 
                if line.startswith("INSERT;"):
                    json_data = line[len("INSERT;"):]

                    try:
                        data = json.loads(json_data)
                              
                        name = data["name"]
                        dpi = data["dpi"]
                        date_birth = data["datebirth"]
                        address = data["address"]
                        companies = []
                        companies = data["companies"]
                        
                        b_tree.insert(dpi, data)
                        
                    except json.JSONDecodeError:

                        print("Error al decodificar JSON en la línea:", line)
                #delete data
                elif line.startswith("DELETE;"):
                    json_data = line[len("DELETE;"):]
                
                    try:
                        data = json.loads(json_data)

                        name = data["name"]
                        dpi = data["dpi"]
                        b_tree.eliminarC(dpi)

                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea: ", line)

                #Modify data
                elif line.startswith("PATCH;"):
                    json_data = line[len("PATCH;"):]

                    try:
                        data = json.loads(json_data)
                        
                        
                        if "companies" in data:
                            name = data["name"]
                            dpi = data["dpi"]
                            date_birth = data["datebirth"]
                            address = data["address"]
                            companies = []
                            companies = data["companies"]
                            
                            newData = {
                                "name": name,
                                "dpi": dpi,
                                "datebirth" : date_birth,
                                "address": address,
                                "companies": companies
                            }
                            b_tree.actualizarC(dpi,newData)

                    except json.JSONDecodeError:

                        print("Error al decodificar JSON en la línea:", line)


    def leerCartas():
        # Ruta de la carpeta que deseas recorrer
        carpeta = 'C:/Users/Diego/Desktop/inputs'

        # Extensión de los archivos que quieres procesar (en este caso, archivos de texto .txt)
        extension = '*.txt'

        # Usar glob para obtener una lista de archivos en la carpeta con la extensión deseada
        archivos = glob.glob(os.path.join(carpeta, extension))

        regex = r'CONV-(\d+)-\d+\.txt'

        # Recorrer la lista de archivos y realizar alguna acción en cada uno
        for archivo in archivos:
            nombre_archivo = os.path.basename(archivo)
            match = re.search(regex, nombre_archivo)
            dpiObtenido = match.group(1)
            result = b_tree.search(dpiObtenido)
            cliente = result[0].data[result[1]]
            name = cliente["name"]
            dpi = cliente["dpi"]
            date_birth = cliente["datebirth"]
            address = cliente["address"]
            companies = []
            companies = cliente["companies"]
            conversaciones = []
            conversaciones = cliente.get("conversaciones",[])
            conversaciones.append(nombre_archivo)
            newData = {
                "name" : name,
                "dpi" : dpi,
                "datebirth" : date_birth,
                "address" : address,
                "companies" : companies,
                "conversaciones" : conversaciones
            }
            b_tree.actualizarC(dpiObtenido, newData)
            """
            with open(archivo, 'r') as file:
                # Realiza alguna acción con el archivo de texto, por ejemplo, imprimir su contenido
                contenido = file.read()
                cifrado = Controller.cifrar_transposicion(contenido,dpiObtenido)
                print(f'Nombre del archivo: {nombre_archivo}')
                print(f'Contenido del archivo {archivo}:\n{cifrado}')
            """    
    
    

    
    
    def listar():
        # Listar todos los clientes
        all_clients = b_tree.list_clients()
        for client in all_clients:
            print(client)



    def buscarC(dpi):
        # Buscar un cliente
        result = b_tree.search(dpi)
        if result:
            cliente = result[0].data[result[1]]
            companies = []
            
            
            print(f"Cliente encontrado: {cliente['name']} (DPI: {dpi})")
            print("Información del Cliente:")
            print(f"Nombre: {cliente['name']}")
            print(f"Fecha de Nacimiento: {cliente['datebirth']}")
            print(f"Dirección: {cliente['address']}")
            print(f"Empresas: {cliente['companies']}")
            print(f"Conversaciones: {cliente['conversaciones']}")

        else:
            print(f"Cliente con dpi {dpi} no encontrado.")
    
    def verCartas(dpi):
        carpeta = 'C:/Users/Diego/Desktop/inputs'

        regex = re.compile(r'CONV-{}-\d+\.txt'.format(dpi))

        archivos = glob.glob(os.path.join(carpeta, '*.txt'))

        for archivo in archivos:
            
            nombre_archivo = os.path.basename(archivo)
            if regex.match(nombre_archivo):
                opc = input("Se mostrarán las conversaciones: ")
                print(f'-------------FIRMA DIGITAL------------')
                print(f'Conversación para cliente con dpi: {dpi}: {nombre_archivo}')
                with open(archivo, 'r') as file:
                    contenido = file.read()
                    men_hash_firma = Controller.hash_mensaje(contenido)
                    p, q = Keys.generar_primos_aleatorios()
                    clave_publica, clave_privada = Keys.generate_keypair(p,q)
                    firma = Controller.firmar_mensaje(men_hash_firma,clave_privada)
                    print(f'\n{firma}')
                    print(f'-------------CONVERSACION CIFRADA------------')
                    cifrado = Controller.cifrar_transposicion(contenido,dpi)
                    print(f'Contenido del archivo {archivo}:\n{cifrado}')
                    opc = input("Desea ver esta carta descifrada?: ")
                    if(opc == "Si" or opc == "si"):
                        descifrada = Controller.descifrar_transposicion(cifrado,dpi)
                        print(f'-------------CONVERSACION DESCIFRADA------------')
                        print(f'Contenido del archivo {archivo}:\n{descifrada}')
                        men_hash_descifrado = Controller.hash_mensaje(descifrada)
                        if(men_hash_firma == men_hash_descifrado):
                            print(f'---------------------')
                            print(f'La firma es válida!!')
                            print(f'---------------------')
                        else:
                            print(f'---------------------')
                            print(f'La firma no es válida. El documento ha sido modificado')
                            print(f'---------------------')
                """
                print(f'-------------CONVERSACION CIFRADA------------')
                print(f'Encontrada carta para cliente con dpi: {dpi}: {nombre_archivo}')
                # Leer y mostrar el contenido del archivo
                with open(archivo, 'r') as file:
                    contenido = file.read()
                    cifrado = Controller.cifrar_transposicion(contenido,dpi)
                    print(f'Contenido del archivo {archivo}:\n{cifrado}')
                    opc = input("Desea ver esta carta descifrada?: ")
                    if(opc == "Si" or opc == "si"):
                        descifrada = Controller.descifrar_transposicion(cifrado,dpi)
                        print(f'-------------CONVERSACION DESCIFRADA------------')
                        print(f'Contenido del archivo {archivo}:\n{descifrada}')
                        men_hash = Controller.hash_mensaje(descifrada)
                        print(f'Mensaje con Hash {archivo}:\n{men_hash}')
                """



    def buscarCporNombre(name):
        #Buscar un cliente
        result = b_tree.searchByName(name)
        if result:
            cliente = result[0].data[result[1]]
            print(f"Cliente encontrado: {cliente['name']} (DPI: {cliente['dpi']})")
            print("Información del Cliente:")
            print(f"Nombre: {cliente['name']}")
            print(f"DPI: {cliente['dpi']}")
            print(f"Fecha de Nacimiento: {cliente['datebirth']}")
            print(f"País de Residencia: {cliente['address']}")
        else:
            print(f"Cliente con nombre {name} no encontrado.")


    def elimincarCporNombre(name):
        result = b_tree.searchByName(name)
        if result:
            nodo = result[0]
            indice = result[1]

            del nodo.keys[indice]
            del nodo.data[indice]

            print(f"Candidato con nombre {name} eliminado con exito.")
        else:
            print(f"Candidato con nombre {name} no encontrado")

    def eliminarC(self, dpi):
        result = b_tree.search(dpi)
        if result:
            nodo = result[0]
            indice = result[1]
        
            # Eliminar la clave y los datos asociados
            del nodo.keys[indice]
            del nodo.data[indice]
        
        
        
            print(f"Candidato con DPI {dpi} eliminado con éxito.")
        else:
            print(f"Candidato con DPI {dpi} no encontrado.")

    
    def actualizarC(self, dpi, nuevos_datos):
        result = b_tree.search(dpi)
        if result:
            nodo = result[0]
            indice = result[1]
        
            # Actualizar los datos asociados al cliente con los nuevos datos proporcionados
            nodo.data[indice] = nuevos_datos
        
            
        
            print(f"Cliente con DPI {dpi} actualizado con éxito.")
        else:
            print(f"Cliente con DPI {dpi} no encontrado.")





b_tree = BTree(t=1000)