import B_Tree

bada = B_Tree.BTree(t=2)

def menuPrincipal():
    continuar = True
    while(continuar):
        opcionCorrecta = False
        while(not opcionCorrecta):
            print("--- MENU PRINCIPAL ---")
            print("1. Listar candidatos")
            print("2. Escribir datos en un archivo JSON")
            print("3. Buscar candidato")
            print("4. Actualizar candidato")
            print("5. Eliminar candidato")
            print("6. Leer archivo JSONL")
            print("7. Salir del programa")
            print("-----------------------")
            opcion = int(input("Seleccione una opción: "))

            if opcion < 1 or opcion > 7:
                print("Opción incorrecta, ingrese nuevamente...")
            elif opcion == 7:
                continuar = False
                break
            else:
                opcionCorrecta = True
                ejecutarOpcion(opcion)

def ejecutarOpcion(opcion):
    if opcion == 1:
        B_Tree.BTree.listar()
    elif opcion == 2:
        B_Tree.BTree.escribirArchivo()
    elif opcion == 3:
        dpi = int(input("Ingrese el dpi del candidato a buscar:"))
        B_Tree.BTree.buscarC(dpi)
    elif opcion == 4:
        actualizarCandidato()
    elif opcion == 5:
        dpi = int(input("Ingrese el dpi del candidato a eliminar:"))
        B_Tree.BTree.eliminarC(dpi)
    elif opcion == 6:
        B_Tree.BTree.cargarJson()

def listarCandidatos():
    print("cerote")

def insertarCandidato():
    print("---Insertar un nuevo candidato---")
    nombre = input("Ingrese el nombre: ")
    dpi = int(input("Ingrese el dpi: "))
    fecha_nac = input("Ingrese la fecha de nacimiento: ")
    direccion = input("Ingrese la dirección: ")
    cand = candidatos(nombre,dpi,fecha_nac,direccion)
    
    Arbol.insertar(cand)
def buscarCandidato():
    print("Buscar")

def actualizarCandidato():
    print("actualizar")

def eliminarCandidato():
    print("eliminar")

menuPrincipal()