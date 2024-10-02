import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue - Juego de Deducción")

# Cargar la imagen del tablero
try:
    board_image = pygame.image.load('clue.jpg')
except pygame.error as e:
    print(f"No se pudo cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

# Definir los rectángulos de las habitaciones
rooms = {
    "Study": pygame.Rect(18, 2, 100, 100),
    "Hall": pygame.Rect(221, 19, 100, 100),
    "Lounge": pygame.Rect(408, 20, 100, 100),
    "Library": pygame.Rect(20, 150, 100, 100),
    "Billiard Room": pygame.Rect(18, 282, 100, 100),
    "Dining Room": pygame.Rect(403, 226, 100, 100),
    "Ballroom": pygame.Rect(231, 421, 100, 100),
    "Kitchen": pygame.Rect(430, 452, 100, 100),
    "Conservatory": pygame.Rect(24, 449, 100, 100),
}

# Lista de sospechosos y armas
suspects = ["Mr. Green", "Professor Plum", "Miss Scarlet", "Colonel Mustard", "Mrs. Peacock", "Mrs. White"]
weapons = ["Knife", "Candlestick", "Revolver", "Rope", "Lead Pipe"]
locations = list(rooms.keys())

# Generar un caso aleatorio
case = {
    "suspect": random.choice(suspects),
    "weapon": random.choice(weapons),
    "location": random.choice(locations)
}

# Establecer la fuente para el texto
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Definir las posiciones de los rectángulos de los sospechosos y armas
suspect_rects = {}
weapon_rects = {}
y_offset = 100

# Crear rectángulos para los sospechosos
for suspect in suspects:
    suspect_rects[suspect] = pygame.Rect(WIDTH - 250, y_offset, 230, 40)
    y_offset += 50

# Alinear armas a la misma altura en el eje Y
y_offset_weapons = 100  # Reiniciar el offset para las armas
x_offset_weapons = WIDTH - 500  # Ajustar para que estén más a la izquierda

# Crear rectángulos para las armas
for weapon in weapons:
    weapon_rects[weapon] = pygame.Rect(x_offset_weapons, y_offset_weapons, 230, 40)
    y_offset_weapons += 50

# Variables para guardar la selección del jugador
selected_suspect = None
selected_weapon = None
selected_room = None

# Función para crear el menú de inicio
def show_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fondo negro

        # Título del juego
        title_text = font.render("Clue - Juego de Deducción", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Explicación del juego
        explanation = [
            "Este es un juego de deducción inspirado en Clue.",
            "Tu objetivo es descubrir quién es el asesino, qué arma fue utilizada y en qué lugar ocurrió el crimen.",
            "Haz clic en los sospechosos, armas y lugares para hacer tus selecciones.",
            "Luego, presiona 'Enter' para hacer una suposición.",
            "También puedes resolver automáticamente presionando 'Resolver'."
        ]

        # Dibujar las líneas de explicación
        for i, line in enumerate(explanation):
            explanation_text = small_font.render(line, True, (255, 255, 255))
            screen.blit(explanation_text, (WIDTH // 2 - explanation_text.get_width() // 2, 200 + i * 40))

        # Botón para comenzar el juego
        start_button_rect = pygame.Rect(WIDTH // 2 - 100, 600, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button_rect)
        start_text = font.render("Empezar Juego", True, (255, 255, 255))
        screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))

        pygame.display.flip()

        # Manejar eventos del menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False  # Salir del menú y empezar el juego

# Funciones para manejar la lógica proposicional
def create_propositions(suspect, weapon, location):
    return f"Sospechoso({suspect}), Arma({weapon}), Lugar({location})"

def evaluate_guess(guess):
    is_correct = (guess["suspect"] == case["suspect"] and 
                  guess["weapon"] == case["weapon"] and 
                  guess["location"] == case["location"])
    
    propositions = []
    if guess["suspect"] == case["suspect"]:
        propositions.append(f"Sospechoso({guess['suspect']}) es correcto.")
    else:
        propositions.append(f"Sospechoso({guess['suspect']}) es incorrecto.")
    
    if guess["weapon"] == case["weapon"]:
        propositions.append(f"Arma({guess['weapon']}) es correcto.")
    else:
        propositions.append(f"Arma({guess['weapon']}) es incorrecto.")
    
    if guess["location"] == case["location"]:
        propositions.append(f"Lugar({guess['location']}) es correcto.")
    else:
        propositions.append(f"Lugar({guess['location']}) es incorrecto.")
    
    return is_correct, propositions

# Lógica para resolver el caso
def resolve_case():
    return case["suspect"], case["weapon"], case["location"]

# Función principal del juego
def run_game():
    global selected_suspect, selected_weapon, selected_room
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Comprobar si se interactúa con las habitaciones
                for room_name, room_rect in rooms.items():
                    if room_rect.collidepoint(mouse_pos):
                        selected_room = room_name
                
                # Comprobar si se interactúa con los sospechosos
                for suspect, suspect_rect in suspect_rects.items():
                    if suspect_rect.collidepoint(mouse_pos):
                        selected_suspect = suspect

                # Comprobar si se interactúa con las armas
                for weapon, weapon_rect in weapon_rects.items():
                    if weapon_rect.collidepoint(mouse_pos):
                        selected_weapon = weapon
                
                # Comprobar si se hace clic en el botón "Resolver"
                resolve_button_rect = pygame.Rect(WIDTH - 250, 550, 230, 40)  # Ajustar la posición
                if resolve_button_rect.collidepoint(mouse_pos):
                    resolved_suspect, resolved_weapon, resolved_location = resolve_case()
                    resultado_mensaje = f"El asesino es {resolved_suspect}, el arma es {resolved_weapon}, y el lugar es {resolved_location}."
                    # Mostrar resultados en el cuadro de diálogo
                    resultado_rect = pygame.Rect(50, HEIGHT - 200, 1100, 180)  # Ubicación en la parte inferior
                    pygame.draw.rect(screen, (255, 255, 255), resultado_rect)
                    pygame.draw.rect(screen, (0, 0, 0), resultado_rect, 2)

                    resultado_text_surface = font.render(resultado_mensaje, True, (0, 0, 0))
                    screen.blit(resultado_text_surface, (resultado_rect.x + 5, resultado_rect.y + 5))
                    
                    pygame.display.flip()
                    pygame.time.wait(3000)  # Esperar 3 segundos antes de continuar

                    # Reiniciar el juego
                    selected_suspect = None
                    selected_weapon = None
                    selected_room = None
                    case = {
                        "suspect": random.choice(suspects),
                        "weapon": random.choice(weapons),
                        "location": random.choice(locations)
                    }

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter
                    if selected_suspect and selected_weapon and selected_room:
                        guess = {
                            "suspect": selected_suspect,
                            "weapon": selected_weapon,
                            "location": selected_room
                        }
                        is_correct, propositions = evaluate_guess(guess)

                        # Mostrar el resultado en un cuadro de diálogo en la parte inferior
                        resultado_rect = pygame.Rect(50, HEIGHT - 200, 1100, 180)  # Ubicación en la parte inferior
                        pygame.draw.rect(screen, (255, 255, 255), resultado_rect)
                        pygame.draw.rect(screen, (0, 0, 0), resultado_rect, 2)

                        for i, proposition in enumerate(propositions):
                            proposition_text_surface = small_font.render(proposition, True, (0, 0, 0))
                            screen.blit(proposition_text_surface, (resultado_rect.x + 5, resultado_rect.y + 5 + i * 30))

                        pygame.display.flip()
                        
                        pygame.time.wait(3000)  # Esperar 3 segundos antes de continuar

                        if is_correct:
                            # Si se acierta, reiniciar el juego
                            selected_suspect = None
                            selected_weapon = None
                            selected_room = None
                            case = {
                                "suspect": random.choice(suspects),
                                "weapon": random.choice(weapons),
                                "location": random.choice(locations)
                            }

        # Dibujar el tablero
        screen.fill((255, 255, 255))
        screen.blit(board_image, (0, 0))

        # Dibujar los rectángulos de las habitaciones
        for room_name, room_rect in rooms.items():
            if room_name == selected_room:
                pygame.draw.rect(screen, (255, 0, 0), room_rect, 5)  # Rojo si está seleccionado
            else:
                pygame.draw.rect(screen, (0, 0, 0), room_rect, 2)  # Negro por defecto

        # Dibujar los rectángulos de los sospechosos
        for suspect, suspect_rect in suspect_rects.items():
            if suspect == selected_suspect:
                pygame.draw.rect(screen, (255, 0, 0), suspect_rect)  # Rojo si está seleccionado
            else:
                pygame.draw.rect(screen, (255, 255, 255), suspect_rect)  # Blanco por defecto
            suspect_text_surface = font.render(suspect, True, (0, 0, 0))
            screen.blit(suspect_text_surface, (suspect_rect.x + 5, suspect_rect.y + 5))

        # Dibujar los rectángulos de las armas
        for weapon, weapon_rect in weapon_rects.items():
            if weapon == selected_weapon:
                pygame.draw.rect(screen, (255, 0, 0), weapon_rect)  # Rojo si está seleccionado
            else:
                pygame.draw.rect(screen, (255, 255, 255), weapon_rect)  # Blanco por defecto
            weapon_text_surface = font.render(weapon, True, (0, 0, 0))
            screen.blit(weapon_text_surface, (weapon_rect.x + 5, weapon_rect.y + 5))

        # Dibujar el botón "Resolver"
        resolve_button_rect = pygame.Rect(WIDTH - 250, 550, 230, 40)  # Ajustar la posición
        pygame.draw.rect(screen, (0, 255, 0), resolve_button_rect)
        resolve_text_surface = font.render("Resolver", True, (255, 255, 255))
        screen.blit(resolve_text_surface, (resolve_button_rect.x + 5, resolve_button_rect.y + 5))

        # Actualizar la pantalla
        pygame.display.flip()

# Mostrar el menú de inicio
show_menu()

# Iniciar el juego
run_game()
