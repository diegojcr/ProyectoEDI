import B_Tree

bada = B_Tree.BTree(t=1000)

def login():
    B_Tree.BTree.cargarJson()
    print("-------BIENVENIDO-------")
    print("-------INICIO DE SESION-----")
    usuario = input("Ingrese el nombre del reclutador: ")
    contra = usuario + "123"
    contraseñaI = input("Ingrese la contraseña: ")
    


def menuPrincipal():
    continuar = True
    while(continuar):
        opcionCorrecta = False
        while(not opcionCorrecta):
            print("--- MENU PRINCIPAL ---")
            print("1. Listar candidatos")
            print("2. Leer cartas en archivo")
            print("3. Buscar candidato por DPI")
            print("4. Buscar candidato por Nombre")
            print("5. Eliminar candidato por DPI")
            print("6. Eliminar candidato por Nombre")
            print("7. Leer archivo JSONL")
            print("8. Salir del programa")
            print("-----------------------")
            opcion = int(input("Seleccione una opción: "))

            if opcion < 1 or opcion > 8:
                print("Opción incorrecta, ingrese nuevamente...")
            elif opcion == 8:
                continuar = False
                break
            else:
                opcionCorrecta = True
                ejecutarOpcion(opcion)

def ejecutarOpcion(opcion):
    if opcion == 1:
        B_Tree.BTree.listar()
    elif opcion == 2:
        B_Tree.BTree.leerCartas()
    elif opcion == 3:
        dpi = input("Ingrese el dpi del candidato a buscar:")
        B_Tree.BTree.buscarC(dpi)
        op = input("Le gustaría ver slas conversaciones almacenadas?: ")
        if op == "Si" or op == "si":
            B_Tree.BTree.verCartas(dpi)
    elif opcion == 4:
        nombre = input("Ingrese el nombre del candidato a buscar:")
        B_Tree.BTree.buscarCporNombre(nombre)
    elif opcion == 5:
        dpi = input("Ingrese el dpi del candidato a eliminar:")
        bada.eliminarC(dpi)
    elif opcion == 6:
        name = input("Ingrese el nombre del candidato a eliminar:")
        B_Tree.BTree.elimincarCporNombre(name)
    elif opcion == 7:
        B_Tree.BTree.cargarJson()



menuPrincipal()