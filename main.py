#!/home/hampter/Desktop/cablebox/cablebox/bin/python

import pygame
import sys
import random
import time
from config import *
from sound import load_sounds
from media import load_shows
from ui import draw_show_menu, draw_episode_menu
from video import play_video_vlc
from encoders import EncoderManager

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("TV Box")
clock = pygame.time.Clock()
pygame.mouse.set_pos(0, 0)

scroll_sound, select_sound, close_sound, random_sound = load_sounds()

try:
    bg_image = pygame.image.load(BG_IMAGE_PATH)
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print("Error loading background:", e)
    bg_image = None

# ----------------------------
# Encoder setup
# ----------------------------
manager = EncoderManager(ENCODER_CONFIG)

# --- Encoder 1: menu navigation ---
def enc1_cw():   # rotate clockwise ? RIGHT arrow
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

def enc1_ccw():  # rotate counter-clockwise ? LEFT arrow
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))

def enc1_button():  # press ? RETURN / select
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

manager.set_callbacks("Encoder1", clockwise=enc1_cw, counter_clockwise=enc1_ccw, button=enc1_button)

# --- Encoder 2: video seek / pause ---
def enc2_cw():       # rotate clockwise ? fast forward
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f))

def enc2_ccw():      # rotate counter-clockwise ? rewind
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

def enc2_button():   # press ? SPACE (pause/play)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))

manager.set_callbacks("Encoder2", clockwise=enc2_cw, counter_clockwise=enc2_ccw, button=enc2_button)


# --- Encoder 3: video volume / quit ---
def enc3_cw():       # rotate clockwise ? UP arrow (volume up)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

def enc3_ccw():      # rotate counter-clockwise ? DOWN arrow (volume down)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))

def enc3_button():   # press ? Q (quit video)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q))

manager.set_callbacks("Encoder3", clockwise=enc3_cw, counter_clockwise=enc3_ccw, button=enc3_button)


# ----------------------------
# Main loop
# ----------------------------
def main():
    
    print("screen size: ", SCREEN_WIDTH, " x ", SCREEN_HEIGHT);
    
    shows = load_shows(MEDIA_PATH)
    if not shows:
        print("No shows found in", MEDIA_PATH)
        sys.exit(1)

    state = "show_select"
    selected_show = 0
    selected_episode = 0
    top_row = 0
    running = True

    rows = 2
    cols = 5   # force 5 icons per row
    num_shows = len(shows)
    total_rows = (num_shows + cols - 1) // cols
    

    first_show = shows[0]
    first_episode = first_show["episodes"][0]
    ep_file = first_show["path"] + "/" + first_episode
    play_video_vlc(ep_file, screen, preload_only=True)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_sound.play()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_sound.play()
                    running = False
                    break

                if state == "show_select":
                    row = selected_show // cols
                    col = selected_show % cols

                    if event.key == pygame.K_RIGHT:
                        scroll_sound.play()
                        if selected_show + 1 < num_shows:
                            selected_show += 1
                        else:
                            # wrap to beginning
                            selected_show = 0

                    elif event.key == pygame.K_LEFT:
                        scroll_sound.play()
                        if selected_show > 0:
                            selected_show -= 1
                        else:
                            # wrap to end
                            selected_show = num_shows - 1
                    
                    elif event.key == pygame.K_f:
                        # Jump forward one column
                        scroll_sound.play()
                        if selected_show + cols < num_shows:
                            selected_show += cols
                        else:
                            selected_show = num_shows - 1  # clamp to last item

                    elif event.key == pygame.K_r:
                        # Jump backward one column
                        scroll_sound.play()
                        if selected_show - cols >= 0:
                            selected_show -= cols
                        else:
                            selected_show = 0  # clamp to first item

                    elif event.key == pygame.K_p:   # NEW: jump to random show
                        random_sound.play()
                        selected_show = random.randrange(num_shows)

                    elif event.key == pygame.K_RETURN:
                        select_sound.play()
                        state = "episode_select"
                        selected_episode = 0


                    current_row = selected_show // cols
                    max_top_row = max(0, total_rows - rows)
                    if current_row < top_row:
                        top_row = current_row
                    elif current_row >= top_row + rows:
                        top_row = min(current_row - rows + 1, max_top_row)

                elif state == "episode_select":
                    num_episodes = len(shows[selected_show]["episodes"])
                    EP_BOX_HEIGHT = 40
                    EP_BOX_SPACING = 10
                    available_height = SCREEN_HEIGHT - 150
                    max_visible_episodes = available_height // (EP_BOX_HEIGHT + EP_BOX_SPACING)
                    if "top_episode_index" not in locals():
                        top_episode_index = 0

                    if event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                        old_episode = selected_episode
                        if event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                            selected_episode = (selected_episode + 1) % num_episodes
                        else:
                            selected_episode = (selected_episode - 1) % num_episodes
                        if selected_episode != old_episode:
                            scroll_sound.play()
                        if selected_episode < top_episode_index:
                            top_episode_index = selected_episode
                        elif selected_episode >= top_episode_index + max_visible_episodes:
                            top_episode_index = selected_episode - max_visible_episodes + 1

                    elif event.key == pygame.K_RETURN:
                        # Normal sequential playback
                        select_sound.play()
                        time.sleep(0.3)  # let the select sound play
                        screen.fill((0,0,0))
                        pygame.display.flip()

                        while True:
                            ep_file = shows[selected_show]["path"] + "/" + shows[selected_show]["episodes"][selected_episode]
                            result = play_video_vlc(ep_file, screen)

                            # clear screen after each video
                            pygame.mouse.set_pos(0, 0)
                            screen.fill((0,0,0))
                            pygame.display.flip()

                            if result == "ended":
                                # advance to next episode if available
                                if selected_episode + 1 < num_episodes:
                                    selected_episode += 1
                                    continue
                                else:
                                    # no more episodes, return to menu
                                    state = "episode_select"
                                    break
                            elif result == "quit":
                                close_sound.play()
                                state = "episode_select"
                                break
                            else:
                                # stopped or interrupted
                                state = "episode_select"
                                break


                    elif event.key == pygame.K_p:
                        # Random playback loop
                        random_sound.play()
                        selected_episode = random.randrange(num_episodes)
                        # Update the display to show the newly chosen episode
                        screen.fill((0,0,0))
                        if bg_image:
                            screen.blit(bg_image, (0,0))
                        draw_episode_menu(
                            screen, bg_image, shows[selected_show],
                            selected_episode,
                            top_index=top_episode_index,
                            max_visible=max_visible_episodes
                        )
                        pygame.display.flip()
                        
                        
                        time.sleep(0.5)
                        screen.fill((0,0,0))
                        pygame.display.flip()
                        
                        while True:
                            ep_file = shows[selected_show]["path"] + "/" + shows[selected_show]["episodes"][selected_episode]
                            result = play_video_vlc(ep_file, screen)

                            # clear screen after each video
                            pygame.mouse.set_pos(0, 0)
                            screen.fill((0,0,0))
                            pygame.display.flip()

                            if result == "ended":
                                # immediately pick another random episode
                                selected_episode = random.randrange(num_episodes)
                                continue
                            elif result == "quit":   # <-- handle quit explicitly
                                close_sound.play()
                                state = "episode_select"
                                break
                            else:
                                # stopped or interrupted
                                state = "episode_select"
                                break

                                


                    elif event.key == pygame.K_q:
                        close_sound.play()
                        state = "show_select"

                    top_episode_index = draw_episode_menu(
                        screen, bg_image, shows[selected_show],
                        selected_episode,
                        top_index=top_episode_index,
                        max_visible=max_visible_episodes
                    )

        if state == "show_select":
            draw_show_menu(
                screen, bg_image, shows,
                selected_show,
                top_index=top_row * cols,
                rows=rows,
                cols=cols   # <-- pass fixed cols
            )
        elif state == "episode_select":
            draw_episode_menu(screen, bg_image, shows[selected_show], selected_episode)

    pygame.quit()

if __name__ == "__main__":
    main()
    
