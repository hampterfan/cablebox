# video.py
import pygame
import sys
import time
import vlc
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from sound import load_sounds

scroll_sound, select_sound, close_sound, random_sound = load_sounds()

# require an additional scroll at end of video
skip_confirm = False

def play_video_vlc(file_path, screen, preload_only=False):
    
    if pygame.mixer.get_init():
        pygame.mixer.quit()

    clock = pygame.time.Clock()
    instance = vlc.Instance('--no-xlib', '--no-video-title-show')
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)

    wm_info = pygame.display.get_wm_info()
    window_id = wm_info.get('window')
    try:
        player.set_xwindow(window_id)
    except AttributeError:
        pass

    player.play()
    time.sleep(0.2)  # short delay for VLC to initialize
    player.video_set_aspect_ratio(f"{SCREEN_WIDTH}:{SCREEN_HEIGHT}")
    player.set_fullscreen(True)

    # === NORMAL PLAYBACK ===
    result = "ended"
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.stop()
                    playing = False
                    result = "quit"
                elif event.key == pygame.K_p:
                    player.pause()
                elif event.key == pygame.K_f:
                    t = player.get_time()
                    length = player.get_length()
                    remaining = length - t

                    if remaining > 30_000:
                        player.set_time(t + 30_000)
                        skip_confirm = False
                    else:
                        if not skip_confirm:
                            skip_confirm = True
                        else:
                            player.set_time(length - 1)
                            skip_confirm = False
                elif event.key == pygame.K_r:
                    t = player.get_time()
                    player.set_time(max(t - 30_000, 0))
                elif event.key == pygame.K_UP:
                    vol = min(player.audio_get_volume() + 10, 100)
                    player.audio_set_volume(vol)
                elif event.key == pygame.K_DOWN:
                    vol = max(player.audio_get_volume() - 10, 0)
                    player.audio_set_volume(vol)

        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Error]:
            playing = False

        clock.tick(FPS)

    # cleanup audio mixer
    pygame.mixer.init()
    scroll_sound.set_volume(0.5)
    select_sound.set_volume(0.5)
    close_sound.set_volume(0.5)

    # release VLC resources
    player.release()
    media.release()
    instance.release()

    return result


