import socket
import threading

# Función para manejar el recepción de mensajes
def handle_receive(client_socket, client_address):
    try:
        while True:
            # Recibir mensaje del cliente
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"{client_address} se desconectó.")
                break
            sender_name = get_name(client_address)
            
            # Verificar si es un mensaje de llamada
            if "llamado desde" in message:
                print(f"Llamada entrante de {sender_name}: {message}")
            else:
                print(f"{sender_name}: {message}")
    except ConnectionResetError:
        print(f"{client_address} se desconectó inesperadamente.")
    except OSError as e:
        if e.errno == 9:
            print("Error: Llegó un mensaje fuera de conexión.")
        else:
            print(f"Error al recibir mensaje de {client_address}: {e}")

    # Eliminar el socket desconectado de la lista de conexiones
    if client_address in connections:
        connections.pop(client_address)
        print(f"{client_address} se ha desconectado.")
    
    # Cerrar conexión con el cliente
    client_socket.close()


# Función para obtener el nombre asociado con una dirección IP
def get_name(client_address):
    if client_address in connections:
        return connections[client_address][1]
    return client_address[0]  # Si no se encuentra el nombre, devolver la dirección IP


# Función para conectar manualmente con un vecino
def connect_to_neighbor(host_ip, host_port):
    try:
        # Verificar si la dirección IP y puerto son los mismos que la IP local y el puerto local
        if host_ip == local_ip and host_port == PORT:
            print("No puedes conectar contigo mismo.")
            return
        
        # Verificar si la dirección IP ya está en la lista de conexiones activas
        for address, (_, name) in connections.items():
            if address[0] == host_ip:
                print(f"Ya estás conectado con {name} ({host_ip}). Rechazando la conexión.")
                return

        # Confirmación negativa para evitar autoconexión
        confirmation = input("¿Estás seguro de conectarte con este vecino? (S/N): ").lower()
        if confirmation != 's':
            print("Conexión cancelada.")
            return

        # Conectar con el vecino
        neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_socket.connect((host_ip, host_port))

        # Obtener el nombre asignado por el servidor
        client_name = neighbor_socket.recv(1024).decode()

        # Obtener el último número de la dirección IP para asignar el nombre
        last_ip_number = host_ip.split('.')[-1]
        client_name = f"Vecino_{last_ip_number}" if last_ip_number != '1' else "Vecino 1"

        # Iniciar el hilo para recibir mensajes del vecino
        receive_thread = threading.Thread(target=handle_receive, args=(neighbor_socket, (host_ip, host_port)))
        receive_thread.start()

        # Agregar el vecino a la lista de conexiones con su nombre
        connections[(host_ip, host_port)] = (neighbor_socket, client_name)

        print(f"Conectado con {client_name} ({host_ip}:{host_port})")
    except Exception as e:
        print("Error al conectar:", e)


# Función para mostrar las conexiones activas
def show_connections(local_ip):
    print("\nConexiones activas:")
    print(f"Tu dirección IP: {local_ip}")
    if not connections:
        print("No hay conexiones activas.")
    else:
        for i, (address, (socket, name)) in enumerate(connections.items()):
            print(f"{i+1}. {name} ({address[0]}:{address[1]})")


# Función para descubrir vecinos y conectar automáticamente
def discover_neighbors(local_ip, port=None):
    global neighbor_count  # Declarar la variable como global
    try:
        # Definir el puerto si no se proporciona manualmente
        if port is None:
            port = PORT

        # Definir el rango de direcciones IP a escanear (puedes ajustarlo según tu red)
        network_prefix = '.'.join(local_ip.split('.')[:3]) + '.'
        start_ip = 1
        end_ip = 254

        found_neighbors = []

        print("Escaneando vecinos en la red local...")
        for i in range(start_ip, end_ip + 1):
            ip = network_prefix + str(i)
            if ip != local_ip:
                # Intentar conectar con el vecino en el puerto específico
                neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                neighbor_socket.settimeout(0.5)  # Tiempo de espera reducido
                result = neighbor_socket.connect_ex((ip, port))
                if result == 0:
                    # Si la conexión es exitosa, agregar la IP a la lista de vecinos encontrados
                    found_neighbors.append(ip)
                    if (ip, port) not in connections:
                        # Conectar automáticamente con el vecino
                        auto_connect_to_neighbor(ip, port, str(ip.split('.')[-1]))  # Pasar el último número de la IP como nombre de vecino
                        neighbor_socket.close()  # Cerrar el socket después de conectar automáticamente
                else:
                    neighbor_socket.close()  # Cerrar el socket si la conexión falla
                    
            # Mostrar el progreso como un porcentaje
            progress = (i - start_ip + 1) / (end_ip - start_ip + 1) * 100
            print(f"Progreso: {progress:.1f}%", end='\r')

        print("\nVecinos encontrados:")
        for ip in found_neighbors:
            print(ip)

    except Exception as e:
        print("Error al descubrir vecinos:", e)



# Función para conectar automáticamente con el vecino
def auto_connect_to_neighbor(neighbor_ip, neighbor_port, neighbor_count):
    try:
        # Verificar si la dirección IP ya está conectada
        for address, (_, name) in connections.items():
            if address[0] == neighbor_ip:
                print(f"La conexión con {neighbor_ip} ya existe. Rechazando la conexión.")
                return

        # Conectar automáticamente con el vecino
        neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_socket.connect((neighbor_ip, neighbor_port))

        # Asignar un nombre único al vecino como "Vecino 1", "Vecino 2", etc.
        neighbor_name = f"Vecino {neighbor_count}"

        # Enviar el nombre al vecino
        neighbor_socket.sendall(neighbor_name.encode())

        # Iniciar el hilo para recibir mensajes del vecino
        receive_thread = threading.Thread(target=handle_receive, args=(neighbor_socket, (neighbor_ip, neighbor_port)))
        receive_thread.start()

        # Agregar el vecino a la lista de conexiones con su nombre
        connections[(neighbor_ip, neighbor_port)] = (neighbor_socket, neighbor_name)

        print(f"Conectado automáticamente con {neighbor_name} ({neighbor_ip}:{neighbor_port})")
    except Exception as e:
        print("Error al conectar:", e)


        
    
# Función para llamar a un vecino por su número de IP
def call_neighbor_by_ip(local_ip):
    try:
        print("Vecinos disponibles para llamar:")
        for i, (address, (socket, name)) in enumerate(connections.items()):
            ip_number = address[0].split('.')[-1]  # Obtener el último número de la dirección IP
            print(f"{i+1}. Vecino_{ip_number} ({address[0]}:{address[1]})")

        try:
            user_ip_number = input("Ingrese el último número de IP del vecino al que desea llamar: ")
            for address, (socket, name) in connections.items():
                if address[0].split('.')[-1] == user_ip_number:
                    neighbor_address = address
                    break
            else:
                print("Número de IP de vecino no encontrado.")
                return

            # Obtener el socket del vecino al que se desea llamar
            neighbor_socket = connections[neighbor_address][0]

            # Enviar mensaje al vecino indicando que está siendo llamado
            calling_message = f"Estás siendo llamado desde {local_ip}"
            neighbor_socket.sendall(calling_message.encode())

            print(f"Llamando al vecino Vecino_{user_ip_number}...")

            # Solicitar al usuario el mensaje a enviar después de la notificación de llamada
            message = input("Ingrese el mensaje a enviar después de la llamada: ")
            # Enviar el mensaje al vecino
            neighbor_socket.sendall(message.encode())

        except Exception as e:
            print("Error al llamar al vecino:", e)
    except Exception as e:
        print("Error al llamar al vecino:", e)


# Función para manejar el menú
def menu(local_ip):
    while True:
        print("\n=== Menú ===")
        print("1. Conectar a un vecino (escribir 'conectar')")
        print("2. Enviar mensaje (escribir 'enviar')")
        print("3. Enviar mensaje a un usuario específico (escribir 'mensaje')")
        print("4. Mostrar las conexiones activas (escribir 'conexiones')")
        print("5. Escaneo de descubrimiento IP (escribir 'escaneo')")
        print("6. Asignar nombre a una conexión (escribir 'nombre')")
        print("7. Llamar a un vecino (escribir 'llamar')")
        print("8. Desconectar (escribir 'desconectar')")
        print("9. Salir del menú (escribir 'salir')")

        choice = input("Seleccione una opción: ").lower()  # Convertir a minúsculas para facilitar la comparación

        if choice in ['1', 'conectar']:
            # Pedir al usuario la dirección IP y el puerto del vecino
            neighbor_ip = input("Ingresa la dirección IP del vecino: ")
            neighbor_port = int(input("Ingresa el puerto del vecino: "))
            connect_to_neighbor(neighbor_ip, neighbor_port)
            pass
        
        elif choice in ['2', 'enviar']:
            # Pedir al usuario el mensaje a enviar
            message = input("Ingrese el mensaje a enviar: ")
            # Enviar el mensaje a todos los vecinos conectados
            for _, (neighbor_socket, _) in connections.items():
                neighbor_socket.sendall(message.encode())
            pass   
        elif choice in ['3', 'mensaje']:
            # Pedir al usuario el índice del usuario al que enviar el mensaje
            print("Usuarios conectados:")
            for i, (address, (socket, name)) in enumerate(connections.items()):
                print(f"{i+1}. {name} ({address[0]}:{address[1]})")
            try:
                user_index = int(input("Ingrese el número de usuario al que desea enviar el mensaje: ")) - 1
                message = input("Ingrese el mensaje a enviar: ")
                connections[list(connections.keys())[user_index]][0].sendall(message.encode())
            except (IndexError, ValueError):
                print("Índice inválido.")
            pass
            
        elif choice in ['4', 'conexiones']:
            show_connections(local_ip)
            pass
        
        elif choice in ['5', 'escaneo']:
            port_option = input("¿Quieres asignar un puerto manualmente? (S/N): ").upper()
            if port_option == 'S':
                port = int(input("Ingresa el puerto: "))
            else:
                port = PORT
            discover_neighbors(local_ip, port)
            pass
        
        elif choice in ['6', 'nombre']:
            # Asignar nombre a una conexión
            print("Conexiones activas:")
            for i, address in enumerate(connections.keys()):
                print(f"{i+1}. {address[0]}:{address[1]}")
            try:
                user_index = int(input("Ingrese el número de conexión a la que desea asignar un nombre: ")) - 1
                name = input("Ingrese el nombre para la conexión: ")
                address = list(connections.keys())[user_index]
                connections[address] = (connections[address][0], name)
                print(f"Nombre '{name}' asignado a la conexión {address[0]}:{address[1]}.")
            except (IndexError, ValueError):
                print("Índice inválido.")
            pass
            
        elif choice in ['7', 'llamar']:
         call_neighbor_by_ip(local_ip)
         pass

        
        elif choice in ['8', 'desconectar']:
            # Desconectar todos los vecinos
            for _, (neighbor_socket, _) in connections.items():
                neighbor_socket.close()
            connections.clear()
            print("Desconectado de todos los vecinos.")
            pass
        
        elif choice in ['9', 'salir']:
            print("Saliendo del menú...")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")
        
         # Espera confirmación para volver a mostrar el menú
        print("             ")
        input("Presione Enter para continuar o escriba 'menu' para mostrar el menú nuevamente: ")

# Puerto para la conexión
PORT = 9999

if __name__ == "__main__":
    # Diccionario para almacenar las conexiones activas
    connections = {}

    # Solicitar al usuario su dirección IP local
    local_ip = input("Ingrese su dirección IP local: ")

    # Crear servidor para aceptar conexiones entrantes
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))  # Utilizar la IP local automáticamente asignada
    server.listen()

    print(f"Esperando conexiones entrantes en el puerto {PORT}...")

    # Iniciar hilo para el menú
    menu_thread = threading.Thread(target=menu, args=(local_ip,))
    menu_thread.start()

# Aceptar conexiones entrantes
while True:
    client_socket, client_address = server.accept()
    print(f"Conexión entrante de {client_address}")

    # Obtener el último número de la dirección IP del cliente para asignar el nombre
    last_ip_number = client_address[0].split('.')[-1]
    client_name = f"Vecino_{last_ip_number}" if last_ip_number != '1' else "Vecino 1"

    # Enviar el nombre al cliente
    client_socket.sendall(client_name.encode())

    # Agregar la conexión entrante al diccionario de conexiones
    connections[client_address] = (client_socket, client_name)

    # Iniciar hilo para recibir mensajes
    receive_thread = threading.Thread(target=handle_receive, args=(client_socket, client_address))
    receive_thread.start()
