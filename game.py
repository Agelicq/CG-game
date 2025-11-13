import pygame
import sys
# ¡Ya no importamos 'time'! Usaremos el reloj interno de Pygame.

# --- Inicialización de Pygame ---
pygame.init()

# --- Constantes Basadas en tu GDD ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Astro lost")

# Reloj para controlar los FPS
reloj = pygame.time.Clock()

# --- Colores ---
COLOR_FONDO_OSCURO = (5, 0, 20) 
COLOR_NEON_CIAN = (0, 255, 255)
COLOR_BLANCO = (230, 230, 250)

# --- Fuentes ---
try:
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_menu = pygame.font.Font(None, 50)
    fuente_pequena = pygame.font.Font(None, 30) # Fuente para el texto de "saltar"
except:
    print("Error al cargar fuentes. Usando fuente por defecto.")
    # (código de fuentes de respaldo)


# --- Función Auxiliar para dibujar texto ---
def dibujar_texto(texto, fuente, color, superficie, x, y):
    objeto_texto = fuente.render(texto, True, color)
    rect_texto = objeto_texto.get_rect()
    rect_texto.center = (x, y)
    superficie.blit(objeto_texto, rect_texto)

# --- Cargar la imagen de fondo para el menú ---
try:
    fondo_menu = pygame.image.load("historia_4.png").convert()
    # La escalamos para que coincida exactamente con la pantalla
    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))
except FileNotFoundError:
    print("Error: No se encontró la imagen de fondo. Usando color sólido.")
    # Si falla, crea un fondo negro para que el juego no se rompa
    fondo_menu = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    fondo_menu.fill(COLOR_FONDO_OSCURO)
    
# --- (NUEVA) Pantalla de Intro (Slideshow) ---
def pantalla_intro():
    """
    Muestra una secuencia de imágenes (slideshow) para contar la historia.
    Se puede saltar con Enter o Escape.
    """
    
    # 1. Lista de las imágenes de la historia
    # Asegúrate de que los nombres coincidan con tus archivos
    lista_imagenes_historia = [
        "historia_1.png",
        "historia_2.png",
        "historia_3.png",
        "historia_4.png",
        # Puedes añadir todas las que quieras
    ]
    
    # Duración de cada imagen en pantalla (en milisegundos)
    duracion_por_imagen = 3000 # 3 segundos

    for imagen_nombre in lista_imagenes_historia:
        # --- Cargar y preparar la imagen ---
        try:
            imagen = pygame.image.load(imagen_nombre).convert()
            # La escalamos a 800x600 por si acaso no tiene ese tamaño
            imagen = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen '{imagen_nombre}'. Saltando...")
            # Si no la encuentra, mostramos un fondo negro y seguimos
            imagen = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            imagen.fill((0, 0, 0))

        # --- Bucle por cada imagen (para que el juego no se congele) ---
        tiempo_inicio_imagen = pygame.time.get_ticks()
        running = True
        while running:
            tiempo_actual = pygame.time.get_ticks()

            # --- Manejo de Eventos (Permitir Salir o Saltar) ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    # Si presiona Enter o Escape, se salta TODA la intro
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                        print("Intro saltada por el usuario.")
                        return # Termina la función pantalla_intro() inmediatamente

            # --- Lógica de tiempo ---
            # Si ya pasaron los 3 segundos, salimos del bucle 'while'
            # y el 'for' cargará la siguiente imagen.
            if tiempo_actual - tiempo_inicio_imagen > duracion_por_imagen:
                running = False

            # --- Dibujar ---
            PANTALLA.blit(imagen, (0, 0)) # Muestra la imagen de la historia
            
            # Mensaje para saltar
            dibujar_texto("Presiona [Enter] para saltar", 
                          fuente_pequena, COLOR_BLANCO, PANTALLA, ANCHO_PANTALLA // 2, ALTO_PANTALLA - 30)
            
            pygame.display.update()
            reloj.tick(60)
            
    # Cuando el bucle 'for' termina, la función acaba y pasa al menú.


# --- (MISMA) Función Menú Principal ---
def menu_principal():
    """
    Bucle principal para el Menú Principal.
    (Esta función es la misma de antes, no hay cambios)
    """
    while True:
        PANTALLA.blit(fondo_menu, (0, 0))
        dibujar_texto("Menú Principal", fuente_titulo, COLOR_BLANCO, PANTALLA, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4)

        mx, my = pygame.mouse.get_pos()

        # --- Opciones del Menú ---
        boton_jugar = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 250, 200, 50)
        boton_puntajes = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 310, 200, 50)
        boton_ayuda = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 370, 200, 50)
        boton_creditos = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 430, 200, 50)
        boton_salir = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 490, 200, 50)

        # Resaltar botón
        color_jugar = COLOR_NEON_CIAN if boton_jugar.collidepoint((mx, my)) else COLOR_BLANCO
        color_puntajes = COLOR_NEON_CIAN if boton_puntajes.collidepoint((mx, my)) else COLOR_BLANCO
        color_ayuda = COLOR_NEON_CIAN if boton_ayuda.collidepoint((mx, my)) else COLOR_BLANCO
        color_creditos = COLOR_NEON_CIAN if boton_creditos.collidepoint((mx, my)) else COLOR_BLANCO
        color_salir = COLOR_NEON_CIAN if boton_salir.collidepoint((mx, my)) else COLOR_BLANCO

        # Dibujar los botones
        dibujar_texto("Jugar", fuente_menu, color_jugar, PANTALLA, ANCHO_PANTALLA // 2, 275)
        dibujar_texto("Puntajes", fuente_menu, color_puntajes, PANTALLA, ANCHO_PANTALLA // 2, 335)
        dibujar_texto("Ayuda", fuente_menu, color_ayuda, PANTALLA, ANCHO_PANTALLA // 2, 395)
        dibujar_texto("Créditos", fuente_menu, color_creditos, PANTALLA, ANCHO_PANTALLA // 2, 455)
        dibujar_texto("Salir", fuente_menu, color_salir, PANTALLA, ANCHO_PANTALLA // 2, 515)

        click = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    click = True

        # --- Acciones de los Botones ---
        if boton_jugar.collidepoint((mx, my)) and click:
            print("Iniciando Selección de Nivel...")
            # Aquí llamarías a la función seleccion_nivel()
                
        if boton_puntajes.collidepoint((mx, my)) and click:
            print("Mostrando Puntajes...") 

        if boton_ayuda.collidepoint((mx, my)) and click:
            print("Mostrando Ayuda...") 

        if boton_creditos.collidepoint((mx, my)) and click:
            print("Mostrando Créditos...") 

        if boton_salir.collidepoint((mx, my)) and click:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        reloj.tick(60)

# --- Ejecución del Juego ---
# 1. Primero se ejecuta el slideshow
pantalla_intro()
# 2. Cuando termina (o se salta), se ejecuta el menú
menu_principal()