import pygame
import sys
import time

# --- Inicialización de Pygame ---
pygame.init()

# --- Constantes Basadas en tu GDD ---

# Resolución de pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Astro lost") #

# Reloj para controlar los FPS
reloj = pygame.time.Clock()

# --- Definición de Colores (Basado en la temática) ---
# GDD menciona "nebulosa púrpura" y "fondo espacial oscuro"
COLOR_FONDO_OSCURO = (5, 0, 20) 
# GDD menciona "luces de neón cian"
COLOR_NEON_CIAN = (0, 255, 255)
# GDD menciona "blanco glacial"
COLOR_BLANCO = (230, 230, 250)

# --- Fuentes (Simulando "Pixel Art Retro") ---
# Usamos una fuente monoespaciada simple. 
# Idealmente, aquí cargarías una fuente .ttf de pixel art
try:
    fuente_titulo = pygame.font.Font(None, 74) # Fuente para el título
    fuente_menu = pygame.font.Font(None, 50)  # Fuente para opciones de menú
except:
    print("Error al cargar fuentes. Usando fuente por defecto.")
    fuente_titulo = pygame.font.SysFont('Consolas', 74)
    fuente_menu = pygame.font.SysFont('Consolas', 50)


# --- Función Auxiliar para dibujar texto ---
def dibujar_texto(texto, fuente, color, superficie, x, y):
    """
    Función para renderizar texto en la pantalla.
    Centra el texto en las coordenadas (x, y).
    """
    objeto_texto = fuente.render(texto, True, color)
    rect_texto = objeto_texto.get_rect()
    rect_texto.center = (x, y)
    superficie.blit(objeto_texto, rect_texto)


# --- Pantalla de Intro ---
def pantalla_intro():
    """
    Muestra la pantalla de Intro con el logo.

    Ahora la intro dura 3 segundos *o* se puede saltar con clic izquierdo del ratón
    o pulsando cualquier tecla. También dibuja un texto "Haz clic para continuar".
    """
    tiempo_inicio = time.time()
    duracion = 3.0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Permitir saltar la intro con clic izquierdo o cualquier tecla
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                return  # vuelve al menú
            if evento.type == pygame.KEYDOWN:
                return

        # Si han pasado más de 'duracion' segundos, salir automáticamente
        if time.time() - tiempo_inicio >= duracion:
            return

        # Ambientación: "scroll lento de estrellas", "nebulosa púrpura"
        # (Por ahora, solo un fondo estático)
        PANTALLA.fill(COLOR_FONDO_OSCURO)
        
        # "Presenta el logotipo de Astro-Lost"
        dibujar_texto("Astro lost", fuente_titulo, COLOR_BLANCO, PANTALLA, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 30)
        pygame.display.update()
        reloj.tick(60)

# --- Menú Principal ---
def menu_principal():
    """
    Bucle principal para el Menú Principal.
    Maneja la selección de opciones.
    """
    while True:
        # "fondo espacial oscuro"
        PANTALLA.fill(COLOR_FONDO_OSCURO) 
        
        dibujar_texto("Menú Principal", fuente_titulo, COLOR_BLANCO, PANTALLA, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4)

        # --- Obtener posición del mouse ---
        mx, my = pygame.mouse.get_pos()

        # --- Opciones del Menú ---
        # "Botones con un marcado estilo Pixel Art Retro y luces de neón cian"
        # (Creamos rectángulos invisibles para la colisión del clic)
        
        boton_jugar = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 250, 200, 50)
        boton_puntajes = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 310, 200, 50)
        boton_ayuda = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 370, 200, 50)
        boton_creditos = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 430, 200, 50)
        boton_salir = pygame.Rect(ANCHO_PANTALLA // 2 - 100, 490, 200, 50)

        # Resaltar botón si el mouse está encima (simulando "luces de neón")
        color_jugar = COLOR_NEON_CIAN if boton_jugar.collidepoint((mx, my)) else COLOR_BLANCO
        color_puntajes = COLOR_NEON_CIAN if boton_puntajes.collidepoint((mx, my)) else COLOR_BLANCO
        color_ayuda = COLOR_NEON_CIAN if boton_ayuda.collidepoint((mx, my)) else COLOR_BLANCO
        color_creditos = COLOR_NEON_CIAN if boton_creditos.collidepoint((mx, my)) else COLOR_BLANCO
        color_salir = COLOR_NEON_CIAN if boton_salir.collidepoint((mx, my)) else COLOR_BLANCO

        # Dibujar los botones (como texto)
        dibujar_texto("Jugar", fuente_menu, color_jugar, PANTALLA, ANCHO_PANTALLA // 2, 275) #
        dibujar_texto("Puntajes", fuente_menu, color_puntajes, PANTALLA, ANCHO_PANTALLA // 2, 335) #
        dibujar_texto("Ayuda", fuente_menu, color_ayuda, PANTALLA, ANCHO_PANTALLA // 2, 395) #
        dibujar_texto("Créditos", fuente_menu, color_creditos, PANTALLA, ANCHO_PANTALLA // 2, 455) #
        dibujar_texto("Salir", fuente_menu, color_salir, PANTALLA, ANCHO_PANTALLA // 2, 515) #

        # --- Manejo de Eventos (Clics) ---
        click = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    click = True

        # --- Acciones de los Botones ---
        if boton_jugar.collidepoint((mx, my)):
            if click:
                # "Jugar" dirige primero a la [Selección de Nivel]
                print("Iniciando Selección de Nivel...")
                # Aquí llamarías a la función seleccion_nivel()
                
        if boton_puntajes.collidepoint((mx, my)):
            if click:
                print("Mostrando Puntajes...") #
                # Aquí llamarías a la función mostrar_puntajes()

        if boton_ayuda.collidepoint((mx, my)):
            if click:
                print("Mostrando Ayuda...") #
                # Aquí llamarías a la función mostrar_ayuda()

        if boton_creditos.collidepoint((mx, my)):
            if click:
                print("Mostrando Créditos...") #
                # Aquí llamarías a la función mostrar_creditos()

        if boton_salir.collidepoint((mx, my)):
            if click:
                # GDD: "Debe mostrar una ventana emergente sencilla... [Sí] / [No]"
                # (Por ahora, solo salimos directamente)
                pygame.quit()
                sys.exit()


        pygame.display.update()
        reloj.tick(60)

# --- Ejecución del Juego ---
pantalla_intro()
menu_principal()