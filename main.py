import time
from pynput import keyboard
import pygame

# Inicializa o pygame e o mixer
pygame.init()
pygame.mixer.init()

start_time = 0
is_pressed = False
touch_count = 0
game_start_time = None  # Para armazenar o início do jogo
long_press_detected = False  # Para verificar se a tecla 'q' foi pressionada por mais de 5 segundos
task_active = False  # Para verificar se a tarefa está ativa

def play_audio(file):
    """Reproduz um arquivo de áudio usando pygame.mixer.Sound."""
    try:
        sound = pygame.mixer.Sound(file)
        sound.play()
        pygame.time.delay(int(sound.get_length() * 1000))  # Aguarda o áudio terminar
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")

def on_press(key):
    global start_time, is_pressed, touch_count, game_start_time, long_press_detected, task_active
    if isinstance(key, keyboard.KeyCode) and key.char == 'q' and not is_pressed:
        start_time = time.time()
        is_pressed = True

        # Só incrementa o contador de toques se a tarefa estiver ativa
        if task_active:
            touch_count += 1

def on_release(key):
    global is_pressed, game_start_time, long_press_detected, task_active
    if isinstance(key, keyboard.KeyCode) and key.char == 'q' and is_pressed:
        press_duration = time.time() - start_time
        is_pressed = False

        # Verifica se a tecla 'q' foi pressionada por mais de 5 segundos
        if press_duration > 5:
            if not long_press_detected:
                # Inicia a tarefa
                long_press_detected = True
                print("Tarefa iniciada! Iniciando contagem regressiva de 5 segundos...")

                # Reproduz o áudio "comece.mp3"
                play_audio("áudios/comece.mp3")

                # Contagem regressiva de 5 segundos com áudios
                for i in range(5, 0, -1):
                    print(f"Iniciando em {i}...")
                    play_audio(f"audios/{i}.wav")  # Reproduz o áudio correspondente
                    time.sleep(1)  # Aguarda 1 segundo

                game_start_time = time.time()  # Inicia a contagem do tempo total da tarefa
                task_active = True  # Marca a tarefa como ativa
                print("Contagem regressiva finalizada! Agora contabilizando toques e tempo total.")
            else:
                # Finaliza a tarefa
                task_active = False
                game_duration = time.time() - game_start_time
                print("\nTarefa finalizada!")
                print(f"Tempo total da tarefa (s): {game_duration:.2f}")
                print(f"Número total de toques: {touch_count}")
                print("Obrigado por participar!")
                return False  # Encerra o listener

        # Só contabiliza o tempo total e exibe os dados se a tarefa estiver ativa
        if task_active:
            game_duration = time.time() - game_start_time
            print(f"Tempo pressionado (s): {press_duration:.2f}")
            print(f"Número de toques: {touch_count}")
            print(f"Tempo total da tarefa (s): {game_duration:.2f}")
        else:
            print("Aguardando pressionamento longo da tecla 'q' para iniciar a tarefa.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()