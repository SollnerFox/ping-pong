import json
import os
import socket
import sys
from threading import Thread
from pygame import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 600
HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
PLAYER_NAME = sys.argv[3] if len(sys.argv) > 3 else "Гравець"

init()
mixer.init()

screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption(f"Пінг-Понг — {PLAYER_NAME}")


def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            time.sleep(0.5)


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            if isinstance(game_state, dict):
                game_state["winner"] = -1
            break


font_win = font.Font(None, 72)
font_main = font.Font(None, 36)

try:
    background = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
except:
    background = Surface((WIDTH, HEIGHT))
    background.fill((30, 30, 30))

try:
    WALL_HIT_SOUND = mixer.Sound("1.mp3")
except:
    WALL_HIT_SOUND = None

try:
    PLATFORM_HIT_SOUND = mixer.Sound("2.mp3")
except:
    PLATFORM_HIT_SOUND = None

try:
    COUNTDOWN_SOUND = mixer.Sound("countdown.wav")
except:
    COUNTDOWN_SOUND = None

#try:
    #mixer.music.load("251461__joshuaempyre__arcade-music-loop.wav")
    #mixer.music.set_volume(0.2)
    #mixer.music.play(-1)
#except:
    #pass

game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()

last_sound_event = None
last_countdown_val = None

while True:
    for e in event.get():
        if e.type == QUIT:
            mixer.music.stop()
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        current_cd = game_state["countdown"]

        if current_cd != last_countdown_val:
            if COUNTDOWN_SOUND:
                COUNTDOWN_SOUND.stop()
                COUNTDOWN_SOUND.play()
            last_countdown_val = current_cd

        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(
            str(current_cd), True, (255, 255, 255)
        )
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False

        if you_winner:
            text = "Ти переміг!"
        else:
            text = "Пощастить наступним разом!"

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render("К - рестарт", True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue

    if game_state:
        screen.blit(background, (0, 0))
        draw.rect(
            screen, (0, 255, 0), (20, game_state["paddles"]["0"], 20, 100)
        )
        draw.rect(
            screen,
            (255, 0, 255),
            (WIDTH - 40, game_state["paddles"]["1"], 20, 100),
        )
        draw.circle(
            screen,
            (255, 255, 255),
            (game_state["ball"]["x"], game_state["ball"]["y"]),
            10,
        )
        score_text = font_main.render(
            f"{game_state['scores'][0]} : {game_state['scores'][1]}",
            True,
            (255, 255, 255),
        )
        screen.blit(score_text, (WIDTH // 2 - 25, 20))
        name_text = font_main.render(PLAYER_NAME, True, (255, 255, 255))
        screen.blit(name_text, (20, HEIGHT - 40))

        sound_ev = game_state.get("sound_event")
        if sound_ev and sound_ev != last_sound_event:
            if sound_ev == "wall_hit" and WALL_HIT_SOUND:
                WALL_HIT_SOUND.play()
            elif sound_ev == "platform_hit" and PLATFORM_HIT_SOUND:
                PLATFORM_HIT_SOUND.play()
        last_sound_event = sound_ev

    else:
        wating_text = font_main.render(
            "Очікування гравців...", True, (255, 255, 255)
        )
        screen.blit(wating_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")