import B_Tree
import json
import Keys
import Controller

bada = B_Tree.BTree(t=1000)
data_list = []
def login():
    
    with open('C:/Users/Diego/Desktop/input.json', 'r') as jsonl_file:
        for line in jsonl_file:
            # Insertar datos
            if line.startswith("INSERT;"):
                json_data = line[len("INSERT;"):]

                try:
                    data = json.loads(json_data)
                    data_list.append(data)
                except json.JSONDecodeError:
                    print("Error al decodificar JSON en la línea:", line)

            # Eliminar datos
            elif line.startswith("DELETE;"):
                json_data = line[len("DELETE;"):]
                
                try:
                    data = json.loads(json_data)
                    dpi = data.get("dpi")
                    for item in data_list:
                        if item.get("dpi") == dpi:
                            data_list.remove(item)
                except json.JSONDecodeError:
                    print("Error al decodificar JSON en la línea:", line)

            # Modificar datos
            elif line.startswith("PATCH;"):
                json_data = line[len("PATCH;"):]

                try:
                    data = json.loads(json_data)
                    dpi = data.get("dpi")
                    for i, item in enumerate(data_list):
                        if item.get("dpi") == dpi:
                            data_list[i].update(data)

                except json.JSONDecodeError:
                    print("Error al decodificar JSON en la línea:", line)

    print("-------BIENVENIDO-------")
    print("-------INICIO DE SESION-----")
    usuario = input("Ingrese el nombre del reclutador: ")
    p, q = Keys.generar_primos_aleatorios()
    clave_publica, clave_privada = Keys.generate_keypair(p,q)
    for item in data_list:
        if item.get("recluiter") == usuario:
            contra = usuario + "123"
            contraCifrada = Controller.encriptar(clave_privada, contra, p, q)
            contraseñaI = input("Ingrese la contraseña: ")
            contraDescifrada = Controller.desencriptar(clave_publica,contraCifrada,p,q)
            while(contraseñaI != contraDescifrada):
                contraseñaI = input("La contraseña no es correcta. Intentelo nuevamente: ")
            
            menuPrincipal(usuario)
            break
    



def menuPrincipal(usuario):
    continuar = True
    while(continuar):
        opcionCorrecta = False
        while(not opcionCorrecta):
            print("--- MENU PRINCIPAL ---")
            print("1. Listar candidatos")
            print("2. Leer conversaciones en archivo")
            print("3. Buscar candidato por DPI")
            print("4. Leer cartas de recomendacion en archivo")
            print("5. Eliminar candidato por DPI")
            print("6. Eliminar candidato por Nombre")
            print("7. Leer archivo JSONL del reclutador")
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
                if opcion == 1:
                    B_Tree.BTree.listar()
                elif opcion == 2:
                    B_Tree.BTree.leerConv()
                elif opcion == 3:
                    dpi = input("Ingrese el dpi del candidato a buscar:")
                    B_Tree.BTree.buscarC(dpi)
                    op = input("Le gustaría ver slas conversaciones almacenadas?: ")
                    if op == "Si" or op == "si":
                        B_Tree.BTree.verCartas(dpi)
                elif opcion == 4:
                    B_Tree.BTree.leerCartas()
                elif opcion == 5:
                    dpi = input("Ingrese el dpi del candidato a eliminar:")
                    bada.eliminarC(dpi)
                elif opcion == 6:
                    name = input("Ingrese el nombre del candidato a eliminar:")
                    B_Tree.BTree.elimincarCporNombre(name)
                elif opcion == 7:
                    B_Tree.BTree.cargarPersonalizado(data_list, usuario)
                    print("se han ingresado los datos")




login()
