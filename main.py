# 2D INTEGER SCALING TEMPLATE
from settings import *


# MAIN FUNCTION
def main():

    # PLAYER OBJECT
    class Player:
        def __init__(self, pos, speed):
            self.pos = pos
            self.speed = speed
            self.dir = Vector2()
            self.texture = load_texture(join('assets', 'textures', 'jack.png'))

        def update(self):
            self.dir.x = int(is_key_down(KeyboardKey.KEY_D)) - int(is_key_down(KeyboardKey.KEY_A))
            self.dir.y = int(is_key_down(KeyboardKey.KEY_S)) - int(is_key_down(KeyboardKey.KEY_W))
            self.dir = vector2_normalize(self.dir)

            dt = get_frame_time()

            self.pos.x += self.dir.x * self.speed * dt
            self.pos.y += self.dir.y * self.speed * dt

            self.rec = Rectangle(self.pos.x, self.pos.y, 32, 32)

            # Always stop on pixel grid
            if self.dir.x == 0:
                self.pos.x = int(self.pos.x)
            if self.dir.y == 0:
                self.pos.y = int(self.pos.y)

        def draw(self):
            draw_texture_v(self.texture, self.pos, WHITE)


# Initialize OpenGL window with desired flags
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"pixel scaling template")
    set_window_min_size(RENDER_WIDTH, RENDER_HEIGHT)

    # Load render texture for framebuffer
    target = load_render_texture(RENDER_WIDTH, RENDER_HEIGHT)

    # INITIALIZE PLAYER OBJECT
    player = Player(pos=Vector2(RENDER_WIDTH//2, RENDER_HEIGHT//2), speed=50)


    # LOAD ASSETS
    logo_image = load_image(
                            join(
                                 'assets',
                                 'textures',
                                 'raylib_64x64.png'
                            )
                 )

    image_color_invert(logo_image)

    logo_texture = load_texture_from_image(logo_image)

    background_texture = load_texture(
                                      join(
                                           'assets',
                                           'textures',
                                           'tilemap.png'
                                      )
                         )

    npc_sprites = [
        load_texture(
            join(
                'assets',
                'textures',
                'my_char.png'
            )
        ),

        load_texture(
            join(
                'assets',
                'textures',
                'ghosto.png'
            )
        ),

        load_texture(
            join(
                'assets',
                'textures',
                'red.png'
            )
        )
    ]

    vignette_frame = gen_image_gradient_radial(
                                               RENDER_WIDTH,
                                               RENDER_HEIGHT,
                                               0.25,
                                               Color(0, 0, 0, 0),
                                               Color(0, 0, 0, 255)
                     )

    vignette_texture = load_texture_from_image(vignette_frame)


    # Camera settings
    camera = Camera2D(
        Vector2(RENDER_WIDTH//2, RENDER_HEIGHT//2),  # Offset
        player.pos,                                  # Target
        0.0,                                         # Rotation
        1.0                                          # Zoom
    )


# STARTING SCREEN STATE

    current_screen = GameScreen.LOGO


# Set FPS to monitor setting and FPS counter state to not show by default

    FPS = get_monitor_refresh_rate(get_current_monitor())

    set_target_fps(FPS)

    show_fps = False


# GAME LOOP

    while not window_should_close():

# ALL SCREENS

    # Update loop
        mouse_pos = get_mouse_x()

    # Get current window dimensions
        window_width = get_render_width()
        window_height = get_render_height()

    # Limit window size to
        scale = int(min(window_width / RENDER_WIDTH, window_height / RENDER_HEIGHT))

    # Calculate the size of the scaled target
        scaled_width = RENDER_WIDTH * scale
        scaled_height = RENDER_HEIGHT * scale

    # Calculate position to center the scaled render texture on the window
        render_x = (window_width - scaled_width) * 0.5
        render_y = (window_height - scaled_height) * 0.5

    # Source rect for the render texture (negative height because OpenGL counts Y coordinates in the reverse direction)
        source_rec = Rectangle(0, 0, target.texture.width, -target.texture.height)
        dest_rec = Rectangle(render_x, render_y, scaled_width, scaled_height)

    # Delta time for consistent speed no matter the framerate
        dt = get_frame_time()

    # Only hide cursor when fullscreen
        if is_window_resized():
            show_cursor()
        elif is_window_fullscreen():
            hide_cursor()
            disable_cursor()

    # Toggle fullscreen with F4
        if is_key_pressed(KeyboardKey.KEY_F4):
            toggle_fullscreen()
        if is_key_pressed(KeyboardKey.KEY_F3):
            show_fps = not show_fps

    # Draw loop
    # Begin drawing to render texture
        begin_texture_mode(target)
        clear_background(BLACK)

# LOGO SCREEN

        if current_screen == GameScreen.LOGO:

    # Update loop

        # Check for screen switch conditions
            if get_time() > 5 or is_key_pressed(KeyboardKey.KEY_SPACE) or is_gesture_detected(Gesture.GESTURE_TAP):
                current_screen = GameScreen.TITLE


    # Draw loop

        # Logo from texture
            draw_texture_v(logo_texture, Vector2(RENDER_WIDTH//2 - 32, RENDER_HEIGHT//2 - 32), WHITE)


# TITLE SCREEN

        elif current_screen == GameScreen.TITLE:

    # Update loop

        # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE) or is_gesture_detected(Gesture.GESTURE_TAP):
                current_screen = GameScreen.GAMEPLAY


    # Draw loop

        # Background
            draw_texture_v(background_texture, Vector2(), WHITE)

            draw_texture_v(vignette_texture, Vector2(), WHITE)

            

        # Title
            draw_text("GAME TITLE",
                      RENDER_WIDTH//2 - measure_text("GAME TITLE", 50)//2,
                      RENDER_HEIGHT//6,
                      50,
                      WHITE
            )

        # Start instruction
            draw_text(
                      "PRESS SPACE TO PLAY",
                      RENDER_WIDTH//2 - measure_text("PRESS SPACE TO PLAY", 10) // 2,
                      RENDER_HEIGHT//6 * 5,
                      10,
                      WHITE
            )


# GAMEPLAY SCREEN

        elif current_screen == GameScreen.GAMEPLAY:

    # Update loop

        # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE) or is_gesture_detected(Gesture.GESTURE_TAP):
                current_screen = GameScreen.TITLE

        # Update player
            player.update()

        # Camera follows player
            camera.target = Vector2(player.pos.x + 8, player.pos.y + 8)

        # Camera zoom
            if is_key_pressed(KeyboardKey.KEY_ONE):
                camera.zoom = camera.zoom * 0.5
            if is_key_pressed(KeyboardKey.KEY_TWO):
                camera.zoom = camera.zoom * 2.0

            camera.zoom = max(1.0, min(2.0, camera.zoom))


    # Draw loop

        # Lock screen to camera
            begin_mode_2d(camera)

        # Draw background
            draw_texture_v(background_texture, Vector2(), WHITE)

        # Draw NPCs
            draw_texture_v(npc_sprites[0], Vector2(100, 100), WHITE)
            draw_texture_v(npc_sprites[1], Vector2(300, 300), WHITE)

        # Draw player
            player.draw()

            draw_texture_v(vignette_texture, Vector2(camera.target.x - RENDER_WIDTH//2, camera.target.y - RENDER_HEIGHT//2), WHITE)

            end_mode_2d()
        end_texture_mode()


# NATIVE RESOLUTION DRAWING ON ALL SCREENS
        begin_drawing()

        clear_background(BLACK)

        # Draw scaled render texture to window resolution
        draw_texture_pro(
                         target.texture,  # Texture
                         source_rec,      # Source rectangle
                         dest_rec,        # Destination rectangle
                         Vector2(0, 0),   # Origin
                         0,               # Rotation
                         WHITE            # Tint
        )

    # Anything that you want to be drawn at native resolution has to go between draw_texture_pro() for the render texture and end_drawing()

        # Custom FPS counter and basic debug info
        #if show_fps:
        draw_text(f"FPS: {FPS}", 0, 0, 20, WHITE)
        draw_text(f"FRAME TIME: {dt:.4f}s", 0, 20, 20, WHITE)
        draw_text(f"WINDOW RESOLUTION: {window_width, window_height}", 0, 60, 20, WHITE)
        draw_text(f"ZOOM: {camera.zoom}", 0, 40, 20, WHITE)
        draw_text(f"PLAYER POSITION: {mouse_pos}", 0, 80, 20, WHITE)

        # Close the loop
        end_drawing()


    # Clean up data when program ends
    unload_render_texture(target)

    unload_image(logo_image)
    unload_image(vignette_frame)

    unload_texture(vignette_texture)
    unload_texture(background_texture)
    unload_texture(logo_texture)
    unload_texture(player.texture)
    unload_texture(npc_sprites[0])
    unload_texture(npc_sprites[1])
    unload_texture(npc_sprites[2])

    close_window()


# Run main function upon execution
if __name__ == "__main__":
    main()
