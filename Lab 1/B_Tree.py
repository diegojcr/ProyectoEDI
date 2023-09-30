import json
import Controller
diccionario_ascii = ["NUL","SOH","STX","ETX","EOT","ENQ","ACK","BEL","BS","HT","LF","VT","FF","CR","SO","SI","DLE","DC1","DC2","DC3","DC4","NAK","SYN","ETB","CAN","EM","SUB","ESC","FS","GS","RS","US"," ","!","'","#","$","%","&","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","¿","Á","É","Í","Ó","Ú","Ä","Ë","Ï","Ö","Ü","Ñ","ñ","/","¡","á","é","í","ó","ú"]

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
        with open('C:/Users/Diego/Desktop/input.json', 'r') as jsonl_file:
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
                        #companies = data["companies"]
                        if "companies" in data:
                            indice = 0
                            empresas_cod = []
                            for company in data["companies"]:
                                companies.append(dpi+" "+company)
                                frase = Controller.comprimir(companies[indice],diccionario_ascii)
                                empresas_cod.append(frase)
                                indice = indice+1
                        
                        newData = {
                            "name": name,
                            "dpi": dpi,
                            "date_birth" : date_birth,
                            "address": address,
                            "companies": empresas_cod
                        }
                        b_tree.insert(dpi, newData)
                        
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
                            #companies = data["companies"]
                            if "companies" in data:
                                indice = 0
                                empresas_cod = []
                                for company in data["companies"]:
                                    companies.append(dpi+" "+company)
                                    frase = Controller.comprimir(companies[indice],diccionario_ascii)
                                    empresas_cod.append(frase)
                                    indice = indice+1
                            
                            newData = {
                                "name": name,
                                "dpi": dpi,
                                "date_birth" : date_birth,
                                "address": address,
                                "companies": empresas_cod
                            }
                            b_tree.actualizarC(dpi,newData)

                    except json.JSONDecodeError:

                        print("Error al decodificar JSON en la línea:", line)



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
            #companies = data["companies"]
            if "companies" in cliente:
                indice = 0
                frase = []
                for company in cliente["companies"]:
                    companies.append(company)
                    frase.append(Controller.descomprimir(companies[indice],diccionario_ascii))
                    indice = indice+1
            
            print(f"Cliente encontrado: {cliente['name']} (DPI: {dpi})")
            print("Información del Cliente:")
            print(f"Nombre: {cliente['name']}")
            print(f"Fecha de Nacimiento: {cliente['date_birth']}")
            print(f"Dirección: {cliente['address']}")
            print(f"Empresas: {frase}")

        else:
            print(f"Cliente con dpi {dpi} no encontrado.")
    
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

    def escribirArchivo():
        all_clients = b_tree.list_clients()
        nombre_archivo = "C:/Users/Diego/Desktop/imprimir.json"

        with open(nombre_archivo, 'w') as archivo_json:
            json.dump(all_clients, archivo_json)



b_tree = BTree(t=1000)