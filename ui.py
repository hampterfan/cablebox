import pygame
from config import *

def draw_show_menu(screen, bg_image, shows, selected_index, top_index=0, rows=2, cols=5):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((0, 0, 0))

    max_visible = rows * cols
    visible_shows = shows[top_index : top_index + max_visible]

    # TRUE EVEN DISTRIBUTION ACROSS FULL WIDTH
    spacing_x = (SCREEN_WIDTH - cols * ICON_WIDTH) / (cols + 1)
    spacing_y = (SCREEN_HEIGHT - rows * ICON_HEIGHT) / (rows + 1)

    for idx, show in enumerate(visible_shows):
        row = idx // cols
        col = idx % cols

        # POSITION IS:
        # spacing + icon + spacing + icon + ...
        x = spacing_x + col * (ICON_WIDTH + spacing_x)
        y = spacing_y + row * (ICON_HEIGHT + spacing_y)

        thumb = pygame.image.load(show["thumbnail"])
        thumb = pygame.transform.scale(thumb, (ICON_WIDTH, ICON_HEIGHT))

        # highlight
        if top_index + idx == selected_index:
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                (x - 5, y - 5, ICON_WIDTH + 10, ICON_HEIGHT + 10),
                3
            )

        screen.blit(thumb, (x, y))

    pygame.display.flip()





    
def draw_episode_menu(screen, bg_image, show, selected_index, top_index=0, max_visible=11):
    """
    Draws episode list with scrolling on the left and a large thumbnail on the right.
    Returns the updated top_index to maintain scroll position.
    """
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48, bold=True)

    # Layout configuration
    THUMB_WIDTH = 600
    THUMB_HEIGHT = 800
    MARGIN_RIGHT = 50
    MARGIN_BETWEEN = 30
    LEFT_MARGIN = 50
    TOP_OFFSET = 50
    EP_BOX_HEIGHT = 40
    EP_BOX_SPACING = 10
    EP_BOX_WIDTH = 500
    MAX_EP_NAME_LENGTH = 40

    # Left area width (for title + episode list)
    left_area_width = SCREEN_WIDTH - THUMB_WIDTH - MARGIN_RIGHT - MARGIN_BETWEEN

    # Title centered within left area
    title_text = title_font.render(show["name"], True, (255, 255, 255))
    title_rect = title_text.get_rect()
    title_x = LEFT_MARGIN + (left_area_width - LEFT_MARGIN - title_rect.width) // 2
    title_y = TOP_OFFSET
    screen.blit(title_text, (title_x, title_y))

    # Line under title, aligned to episode box width
    rect_x = LEFT_MARGIN + (left_area_width - LEFT_MARGIN - EP_BOX_WIDTH) // 2
    line_y = title_y + title_rect.height + 10
    pygame.draw.line(
        screen, (255, 255, 255),
        (rect_x, line_y),
        (rect_x + EP_BOX_WIDTH, line_y),
        2
    )

    # Episode list start position
    ep_start_y = line_y + 20

    # Ensure the episodes fit vertically without exceeding screen
    available_height = SCREEN_HEIGHT - ep_start_y - 20
    max_visible_to_draw = min(max_visible, available_height // (EP_BOX_HEIGHT + EP_BOX_SPACING))

    num_episodes = len(show["episodes"])

    # Adjust top_index to keep selected in view
    if selected_index < top_index:
        top_index = selected_index
    elif selected_index >= top_index + max_visible_to_draw:
        top_index = selected_index - max_visible_to_draw + 1

    # Slice visible episodes
    visible_episodes = show["episodes"][top_index: top_index + max_visible_to_draw]

    # Draw episodes
    for i, ep in enumerate(visible_episodes):
        real_index = top_index + i
        color = (255, 255, 0) if real_index == selected_index else (255, 255, 255)
        rect_y = ep_start_y + i * (EP_BOX_HEIGHT + EP_BOX_SPACING)

        # Remove .mp4 and truncate long names
        ep_name = ep.rsplit(".mp4", 1)[0]
        ep_display = ep_name if len(ep_name) <= MAX_EP_NAME_LENGTH else ep_name[:MAX_EP_NAME_LENGTH] + "..."

        pygame.draw.rect(screen, color, (rect_x, rect_y, EP_BOX_WIDTH, EP_BOX_HEIGHT), 2)
        text = font.render(ep_display, True, color)
        text_rect = text.get_rect(center=(rect_x + EP_BOX_WIDTH // 2, rect_y + EP_BOX_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Thumbnail on right, vertically centered
    try:
        thumb = pygame.image.load(show["thumbnail"])
        thumb = pygame.transform.scale(thumb, (THUMB_WIDTH, THUMB_HEIGHT))
        thumb_x = SCREEN_WIDTH - THUMB_WIDTH - MARGIN_RIGHT
        thumb_y = (SCREEN_HEIGHT - THUMB_HEIGHT) // 2
        screen.blit(thumb, (thumb_x, thumb_y))
    except Exception:
        # Draw placeholder if missing
        thumb_x = SCREEN_WIDTH - THUMB_WIDTH - MARGIN_RIGHT
        thumb_y = (SCREEN_HEIGHT - THUMB_HEIGHT) // 2
        pygame.draw.rect(screen, (60, 60, 60), (thumb_x, thumb_y, THUMB_WIDTH, THUMB_HEIGHT), 2)

    pygame.display.flip()
    return top_index
