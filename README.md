PEER-TO-PEER (P2P) COMMUNICATION SYSTEM IN PYTHON

Este es un sistema simple de comunicación peer-to-peer (P2P) implementado en Python que permite a los usuarios conectarse entre sí en una red local y comunicarse a través de mensajes.
Características principales:

    COMUNICACIÓN P2P: Los usuarios pueden conectarse entre sí directamente en una red local sin necesidad de un servidor centralizado.
    CONEXIONES MANUALES Y AUTOMÁTICAS: Los usuarios pueden conectarse manualmente ingresando la dirección IP y el puerto del vecino o realizar un escaneo automático para descubrir vecinos disponibles en la red local.
    MENSAJERÍA: Los usuarios pueden enviar mensajes a todos los vecinos conectados o seleccionar un usuario específico para enviar un mensaje.
    Gestión de conexiones activas: El sistema realiza un seguimiento de las conexiones activas y muestra una lista de los vecinos conectados en cualquier momento.

USO:

Para ejecutar el sistema, simplemente inicia el script Python-P2P.py en tu entorno de Python. El sistema mostrará un menú interactivo que te guiará a través de las diferentes opciones disponibles, como conectar a un vecino, enviar mensajes, mostrar conexiones activas y más.
Requisitos:

    Python 3.x
    Biblioteca estándar de Python

CONSTRUCCIÓN Y TECNOLOGÍAS UTILIZADAS

Este sistema de comunicación P2P está construido completamente en Python y hace uso de las siguientes funciones y bibliotecas:

    Sockets de Red: La comunicación entre pares se logra utilizando sockets de red TCP/IP, que permiten la transmisión de datos a través de una red local.

    Hilos (Threads): Se utilizan hilos de Python para manejar la comunicación concurrente con múltiples vecinos. Cada conexión activa se maneja en un hilo separado para garantizar la capacidad de respuesta del sistema.

    Biblioteca estándar de Python: El sistema hace uso extensivo de la biblioteca estándar de Python para manejar operaciones de red, entrada/salida de datos, manejo de excepciones y otros aspectos esenciales de la programación en red.

    Interfaz de Usuario Interactiva: El sistema presenta una interfaz de usuario interactiva basada en texto que permite a los usuarios seleccionar diferentes opciones a través de un menú.

    Descubrimiento Automático de Vecinos: Se implementa una función de escaneo automático de la red local para descubrir vecinos disponibles en la misma red. Esto se logra mediante el envío de solicitudes de conexión a rangos de direcciones IP predefinidos en la red local y la respuesta a las conexiones exitosas.

    Mensajería Directa entre Pares: Los usuarios pueden enviar mensajes directamente a otros vecinos conectados utilizando el sistema de mensajería implementado en el protocolo P2P.

Esta combinación de tecnologías y funciones permite la creación de un sistema de comunicación P2P simple pero efectivo en Python.

CONTRIBUCIONES:

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, no dudes en abrir un problema o enviar una solicitud de extracción. Cualquier mejora, corrección de errores o nuevas características serán apreciadas.

CONTRIBUIDORES DESTACADOS:
JHON JAIRO RENDON ZAVALA
SERGIO LUIS ARCILA QUICENO
