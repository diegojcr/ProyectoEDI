import json

class BTreeNode(object):
    """A B-Tree Node.
    
    attributes
    =====================
    leaf : boolean, determines whether this node is a leaf.
    keys : list, a list of keys internal to this node
    c : list, a list of children of this node
    data: list, a list of data associated with the keys (e.g., candidate information)
    """
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
        """Search the B-Tree for the key k.
        
        args
        =====================
        k : Key to search for
        x : (optional) Node at which to begin search. Can be None, in which case the entire tree is searched.
        
        """
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
    
    def delete(self, k):
        if self.root is not None:
            if self.search(k):
                self._delete(self.root, k)
    
    def _delete(self, x, k):
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            # Key k is in node x in position i
            if x.leaf:
                # Case 1: If the key k is in node x and x is a leaf, delete the key k from x.
                x.keys.pop(i)
                x.data.pop(i)
            else:
                # Case 2: If the key k is in node x and x is an internal node, do the following.
                # a) If the child y that precedes k in node x has at least t keys, then find the
                # predecessor k0 of k in the sub-tree rooted at y. Recursively delete k0, and
                # replace k by k0 in x. (We can find k0 and delete it in a single downward pass.)
                if len(x.c[i].keys) >= self.t:
                    predecessor_key, predecessor_data = self._find_predecessor(x.c[i])
                    x.keys[i] = predecessor_key
                    x.data[i] = predecessor_data
                    self._delete(x.c[i], predecessor_key)
                # b) If y has fewer than t keys but at least t-1 keys, execute symmetrically. We
                # then recurse on the appropriate child.
                elif len(x.c[i + 1].keys) >= self.t:
                    successor_key, successor_data = self._find_successor(x.c[i + 1])
                    x.keys[i] = successor_key
                    x.data[i] = successor_data
                    self._delete(x.c[i + 1], successor_key)
                # c) If both y and z have t-1 keys, merge k and all of z into y, so that x loses both k
                # and the pointer to z, and y now contains 2t - 1 keys. Then free z and recursively delete k
                # from y.
                else:
                    self._merge_children(x, i)
                    self._delete(x.c[i], k)
        else:
            if x.leaf:
                # The key k is not present in the tree.
                print(f"Key {k} not found in the tree.")
            else:
                # Determine the child where k should be located.
                if i == len(x.keys):
                    i -= 1
                if len(x.c[i].keys) < self.t:
                    self._fill_child(x, i)
                # Recurse on the appropriate child.
                if i < len(x.keys) and k > x.keys[i]:
                    i += 1
                self._delete(x.c[i], k)

    def _find_predecessor(self, x):
        """Find the predecessor of the key k in the sub-tree rooted at x."""
        while not x.leaf:
            x = x.c[-1]
        return x.keys[-1], x.data[-1]

    def _find_successor(self, x):
        """Find the successor of the key k in the sub-tree rooted at x."""
        while not x.leaf:
            x = x.c[0]
        return x.keys[0], x.data[0]

    def _merge_children(self, x, i):
        """Merge child i and i+1 of node x."""
        child_i = x.c[i]
        child_i1 = x.c[i + 1]
        child_i.keys.append(x.keys[i])
        child_i.data.append(x.data[i])
        child_i.keys.extend(child_i1.keys)
        child_i.data.extend(child_i1.data)
        child_i.c.extend(child_i1.c)
        x.keys.pop(i)
        x.data.pop(i)
        x.c.pop(i + 1)

    def _fill_child(self, x, i):
        """Fill up child x.c[i] with keys from its siblings or perform a merge."""
        if i > 0 and len(x.c[i - 1].keys) >= self.t:
            self._borrow_from_prev(x, i)
        elif i < len(x.keys) and len(x.c[i + 1].keys) >= self.t:
            self._borrow_from_next(x, i)
        elif i < len(x.keys):
            self._merge_children(x, i)
        else:
            self._merge_children(x, i - 1)

    def _borrow_from_prev(self, x, i):
        """Borrow a key and data from the previous child for child x.c[i]."""
        child_i = x.c[i]
        child_prev = x.c[i - 1]
        child_i.keys.insert(0, x.keys[i - 1])
        child_i.data.insert(0, x.data[i - 1])
        if not child_i.leaf:
            child_i.c.insert(0, child_prev.c.pop())
        x.keys[i - 1] = child_prev.keys.pop()
        x.data[i - 1] = child_prev.data.pop()

    def _borrow_from_next(self, x, i):
        """Borrow a key and data from the next child for child x.c[i]."""
        child_i = x.c[i]
        child_next = x.c[i + 1]
        child_i.keys.append(x.keys[i])
        child_i.data.append(x.data[i])
        if not child_i.leaf:
            child_i.c.append(child_next.c.pop(0))
        x.keys[i] = child_next.keys.pop(0)
        x.data[i] = child_next.data.pop(0)

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



    def cargarJson():
        # Cargar datos desde un archivo JSONL (reemplaza 'data.jsonl' con tu archivo)
        with open('C:/Users/Diego/Desktop/datos.json', 'r') as jsonl_file:
            for line in jsonl_file:
                #insert data 
                if line.startswith("INSERT;"):
                    json_data = line[len("INSERT;"):]

                    try:
                        data = json.loads(json_data)
                                
                        name = data["name"]
                        dpi = data["dpi"]
                        date_birth = data["dateBirth"]
                        address = data["address"]

                        b_tree.insert(dpi, data)
                    except json.JSONDecodeError:

                        print("Error al decodificar JSON en la línea:", line)
                #delete data
                if line.startswith("DELETE;"):
                    json_data = line[len("DELETE;"):]
                
                    try:
                        data = json.loads(json_data)

                        name = data["name"]
                        dpi = data["dpi"]
                        b_tree.delete(dpi)

                    except json.JSONDecodeError:
                        print("Error al decodificar JSON en la línea: ", line)

                #Modify data
                if line.startswith("PATCH;"):
                    json_data = line[len("PATCH;"):]

                    try:
                        data = json.loads(json_data)
                        
                        
                        if "dataBirth" in data:
                            name = data["name"]
                            dpi = data["dpi"]
                            date_birth = data["dateBirth"]
                            newData = {
                                "name": name,
                                "dpi":dpi,
                                "dateBirth":date_birth
                            }
                            b_tree.actualizarC(dpi,newData)
                        elif "address" in data:
                            name = data["name"]
                            dpi = data["dpi"]
                            address = data["address"]
                            newData = {
                                "name": name,
                                "dpi": dpi,
                                "address":address
                            }
                            b_tree.actualizarC(dpi, newData)

                    except json.JSONDecodeError:

                        print("Error al decodificar JSON en la línea:", line)



    def listar():
        # Listar todos los clientes
        all_clients = b_tree.list_clients()
        for client in all_clients:
            print(client)



    def buscarC(dpi):
        # Buscar y eliminar un cliente (reemplaza 'numero_de_cliente' con el número del cliente que desees)
        result = b_tree.search(dpi)
        if result:
            cliente = result[0].data[result[1]]
            print(f"Cliente encontrado: {cliente['name']} (DPI: {dpi})")
            print("Información del Cliente:")
            print(f"Nombre: {cliente['name']}")
            print(f"DPI: {dpi}")
            print(f"Fecha de Nacimiento: {cliente['dateBirth']}")
            print(f"País de Residencia: {cliente['address']}")
        else:
            print(f"Cliente con dpi {dpi} no encontrado.")


    def eliminarC(dpi):
        result = b_tree.search(dpi)
        if result:
            nodo = result[0]
            indice = result[1]
        
            # Eliminar la clave y los datos asociados
            del nodo.keys[indice]
            del nodo.data[indice]
        
        # Realizar cualquier reorganización necesaria para mantener la estructura del árbol B
        
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
        
            # Realizar cualquier reorganización necesaria para mantener la estructura del árbol B
        
            print(f"Cliente con DPI {dpi} actualizado con éxito.")
        else:
            print(f"Cliente con DPI {dpi} no encontrado.")

    def escribirArchivo():
        all_clients = b_tree.list_clients()
        nombre_archivo = "C:/Users/Diego/Desktop/candidatos.json"

        with open(nombre_archivo, 'w') as archivo_json:
            json.dump(all_clients, archivo_json)


# Ejemplo de uso:
# Crear un árbol B con un grado mínimo t (por ejemplo, t=2)
b_tree = BTree(t=1000)