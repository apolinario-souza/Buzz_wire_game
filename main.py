import time
from pynput import keyboard
import pygame
import openpyxl
from threading import Thread
from constants import SUJ, TEMPO_FECHAR_INICIAR_TAREFA

# Inicializa o pygame e o mixer
pygame.init()
pygame.mixer.init()

start_time = 0
is_pressed = False
touch_count = 0
game_start_time = None  # Para armazenar o início do jogo
long_press_detected = False  # Para verificar se a tecla 'q' foi pressionada por mais de 5 segundos
task_active = False  # Para verificar se a tarefa está ativa
buzz_sound = pygame.mixer.Sound("audios/buzz.wav")

def play_buzz():
    """Inicia a reprodução contínua do áudio buzz."""
    buzz_sound.play(loops=-1)

def stop_buzz():
    """Para a reprodução do áudio buzz."""
    buzz_sound.stop()

def play_audio(file):
    """Reproduz um arquivo de áudio usando pygame.mixer.Sound."""
    try:
        sound = pygame.mixer.Sound(file)
        sound.play()
        pygame.time.delay(int(sound.get_length() * 1000))  # Aguarda o áudio terminar
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")

def save_to_excel(duration, touches, total_time, press_moment):
    """Salva os dados no arquivo Excel."""
    file_name = "resultados/"+str(SUJ)+"_dados.xlsx"
    try:
        wb = openpyxl.load_workbook(file_name)
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        wb.active.append(["Tempo Total da Tarefa (s)", "Tempo Pressionado (s)"])
    
    sheet = wb.active
    sheet.append([total_time, duration])
    wb.save(file_name)

def log_time():
    """Função para registrar continuamente o tempo da tarefa."""
    global task_active, game_start_time, is_pressed
    while True:
        if task_active:
            total_time = time.time() - game_start_time
            duration = time.time() - start_time if is_pressed else 0
            save_to_excel(duration, touch_count, total_time, 0)
        time.sleep(0.005)  # 50 Hz

def on_press(key):
    global start_time, is_pressed, touch_count, game_start_time, long_press_detected, task_active
    if isinstance(key, keyboard.KeyCode) and key.char == 'q' and not is_pressed:
        start_time = time.time()
        is_pressed = True
        play_buzz()
        if task_active:
            touch_count += 1

def on_release(key):
    global is_pressed, game_start_time, long_press_detected, task_active
    if isinstance(key, keyboard.KeyCode) and key.char == 'q' and is_pressed:
        press_duration = time.time() - start_time
        is_pressed = False
        stop_buzz()
        if press_duration > TEMPO_FECHAR_INICIAR_TAREFA and not long_press_detected:
            long_press_detected = True
            print("Tarefa iniciada!")
            
            # Contagem regressiva de 5 segundos com áudios
            for i in range(5, 0, -1):
                print(f"Iniciando em {i}...")
                play_audio(f"audios/{i}.wav")  # Reproduz o áudio correspondente
            
            play_audio("audios/comece.mp3")
            game_start_time = time.time()
            task_active = True
        elif long_press_detected and press_duration > TEMPO_FECHAR_INICIAR_TAREFA:
            task_active = False
            print("Tarefa finalizada!")
            return False

# Iniciar a thread para registrar continuamente o tempo
Thread(target=log_time, daemon=True).start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
