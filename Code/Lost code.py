import pygame
import os

pygame.init()

# Configuración de la pantalla y fuente
pantalla = pygame.display.set_mode((608, 608))

# Función para cargar imágenes de forma segura
def cargar_imagen(ruta, dimensiones):
    try:
        return pygame.transform.scale(pygame.image.load(ruta), dimensiones)
    except FileNotFoundError:
        print(f"Error: No se pudo cargar la imagen en {ruta}")
        pygame.quit()
        exit()

# Cargar imágenes
imagenes = {
    0: cargar_imagen(os.path.join("Images", "tierra.png"), (608, 608)),
    1: cargar_imagen(os.path.join("Images", "celda.png"), (608, 608)),
    2: cargar_imagen(os.path.join("Images", "vozmisteriosa.png"), (608, 608)),
    3: cargar_imagen(os.path.join("Images", "vozmisteriosa.png"), (608, 608)),
    4: cargar_imagen(os.path.join("Images", "3 options.png"), (608, 608)),
    5: cargar_imagen(os.path.join("Images", "cuevaexpo.png"), (608, 608)),
}

# Cargar fuente
try:
    font = pygame.font.Font(os.path.join("Fonts", "font.ttf"), 36)
except FileNotFoundError:
    print("Error: No se encontró el archivo de fuente. Verifica la ruta.")
    pygame.quit()
    exit()

# Textos para cada estado
textos = {
    0: [
        "En una tierra olvidada por el tiempo,",
        "donde la magia fluye en forma de símbolos",
        "arcanos, despiertas en una celda oscura",
        "con un extraña marca en la palma.",
    ],
    1: [
        "Despiertas en una celda húmeda,",
        "rodeado de oscuridad...",
    ],
    2: [
        "¿Cuál es tu nombre, joven aprendiz?",
    ],
    4: [
        "Elige sabiamente que harás:",
        "1. Explorar la cueva.",
        "2. Salir a investigar el bosque.",
        "3. Gritar y pedir ayuda.",
    ],
    5: [
        "Explorando la cueva...",
        "Al final de la cueva notas un artefacto ",
        "brillante, decides acercarte a ver",
    ],
}

# Estado inicial
estado = 0  # 0: tierra, 1: celda, 2: vozmisteriosa, 4: opciones
nombre = ""  # Variable para almacenar el nombre ingresado
opcion_seleccionada = 0  # Índice de la opción seleccionada

# Función para mostrar texto
def mostrar_texto(lineas, y_offset=10, color=(155, 155, 155), opcion_activa=None):
    for i, linea in enumerate(lineas):
        if opcion_activa is not None and i == opcion_activa + 1:  # Resaltar opciones seleccionables
            texto = font.render(linea, True, (255, 255, 255))  # Texto blanco para la opción activa
        else:
            texto = font.render(linea, True, color)
        pantalla.blit(texto, (10, y_offset))
        y_offset += 40

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if estado == 2:  # Capturar el nombre directamente
                if event.key == pygame.K_RETURN:  # Finalizar la entrada al presionar Enter
                    estado += 1  # Avanzar al siguiente estado
                elif event.key == pygame.K_BACKSPACE:  # Borrar el último carácter
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode  # Agregar el carácter presionado
            elif estado == 4:  # Navegar y seleccionar opciones
                if event.key == pygame.K_UP:  # Mover hacia arriba
                    opcion_seleccionada = (opcion_seleccionada - 1) % 3
                elif event.key == pygame.K_DOWN:  # Mover hacia abajo
                    opcion_seleccionada = (opcion_seleccionada + 1) % 3
                elif event.key == pygame.K_RETURN:  # Confirmar la opción
                    if opcion_seleccionada == 0:
                        print("Explorando la cueva...")
                        estado = 5
                    elif opcion_seleccionada == 1:
                        print("Saliendo a explorar el bosque...")
                        running = False  # Terminar el juego
                    elif opcion_seleccionada == 2:
                        print("Gritando y pidiendo ayuda...")
                        running = False  # Terminar el juego
            elif event.key == pygame.K_RETURN:  # Avanzar entre estados
                if estado < 4:
                    estado += 1

    # Mostrar la imagen correspondiente según el estado
    pantalla.blit(imagenes[estado], (0, 0))

    # Mostrar las opciones con la opción seleccionada resaltada
    if estado in textos:
        if estado == 4:
            mostrar_texto(textos[4], y_offset=10, opcion_activa=opcion_seleccionada)
        else:
            mostrar_texto(textos[estado])
            
    if estado == 2:  # Mostrar el nombre que el usuario está escribiendo
        texto_nombre = font.render(nombre, True, (155, 155, 155))  # Texto gris
        pantalla.blit(texto_nombre, (10, 40))
    elif estado == 3:  # Mostrar el saludo final
        saludo = f"{nombre}...tu viaje apenas comienza..."
        texto_saludo = font.render(saludo, True, (155, 155, 155))  # Texto gris
        pantalla.blit(texto_saludo, (10, 10))
    pygame.display.flip()

pygame.quit()