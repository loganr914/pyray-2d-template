from settings import *

# Main function
def main():

    # Initialize window with desired flags and parameters
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"pixel scaling template")

    # Load render texture for framebuffer
    target = load_render_texture(RENDER_WIDTH, RENDER_HEIGHT)

    # Monitor class to easily get monitor info
    class Monitor:
        def __init__(self):
            self.id = get_current_monitor()
            self.width = get_monitor_width(self.id)
            self.height = get_monitor_height(self.id)
            self.refresh_rate = get_monitor_refresh_rate(self.id)

    monitor = Monitor()

    # Player class
    class Player:
        def __init__(self, pos, speed):
            self.pos = pos
            self.speed = speed
            self.dir = Vector2()

            self.texture = load_texture(
                join(
                    'assets',
                    'textures',
                    'jack.png'
                )
            )

        def update(self):
            dt = get_frame_time()

            self.dir.x = (
                int(is_key_down(KeyboardKey.KEY_D)) -
                int(is_key_down(KeyboardKey.KEY_A))
            )
            
            self.dir.y = (
                int(is_key_down(KeyboardKey.KEY_S)) -
                int(is_key_down(KeyboardKey.KEY_W))
            )

            self.dir = vector2_normalize(self.dir)

            self.pos.x += (self.dir.x *
                           self.speed *
                           dt)

            self.pos.y += (self.dir.y *
                           self.speed *
                           dt)

            # Always stop on pixel grid
            if self.dir.x == 0:
                self.pos.x = int(self.pos.x)
            if self.dir.y == 0:
                self.pos.y = int(self.pos.y)

            self.rec = Rectangle(
                self.pos.x,
                self.pos.y,
                32,
                32
            )

        def draw(self):
            draw_texture_v(
                self.texture,
                self.pos,
                WHITE
            )

    player = Player(
        pos=Vector2(
            RENDER_WIDTH//2 - 8,
            RENDER_HEIGHT//2 - 8
        ),
        speed=20
    )

    # Load and manipulate assets
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

    background = load_texture(
        join(
            'assets',
            'textures',
            'tilemap.png'
        )
    )

    logo_image = load_image(
        join(
            'assets',
            'textures',
            'raylib_64x64.png'
        )
    )
    
    image_color_invert(logo_image)

    logo = load_texture_from_image(logo_image)

    # Camera settings
    camera = Camera2D(
        Vector2(             # Offset
            RENDER_WIDTH//2,
            RENDER_HEIGHT//2
        ),
        player.pos,          # Target
        0.0,                 # Rotation
        1.0                  # Zoom
    )


    # Limit window size between render and native resolution
    set_window_min_size(RENDER_WIDTH, RENDER_HEIGHT)
    set_window_max_size(monitor.width, monitor.height)

    # Set FPS to monitor setting and FPS counter state to not show by default
    set_target_fps(FPS)
    show_fps = False

    # Starting screen state
    current_screen = GameScreen.LOGO

    # FRAME LOOP ############################################################
    while not window_should_close():

        # UPDATE LOOP - ALL SCREENS #########################################
        
        # Delta time/frame time
        dt = get_frame_time()

        # Get current window dimensions
        window_width = get_render_width()
        window_height = get_render_height()

        # Calculate integer scaling factor 
        scale = int(
            min(
                window_width / RENDER_WIDTH,
                window_height / RENDER_HEIGHT
            )
        )

        # Calculate the size of the scaled target
        scaled_width = RENDER_WIDTH * scale
        scaled_height = RENDER_HEIGHT * scale

        # Calculate 
        render_x = (window_width - scaled_width) * 0.5
        render_y = (window_height - scaled_height) * 0.5

        # Source rect for the render texture (
        source_rec = Rectangle(
            0,
            0,
            target.texture.width,
            -target.texture.height
        )

        dest_rec = Rectangle(
            render_x,
            render_y,
            scaled_width,
            scaled_height
        )

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

        # ALL SCREENS
        # Begin drawing to render texture
        begin_texture_mode(target)
        clear_background(BLACK)

        # LOGO SCREEN #######################################################
        if current_screen == GameScreen.LOGO:

            # UPDATE LOOP ###################################################
            # Check for screen switch conditions
            if (get_time() > 5 or
                is_key_pressed(KeyboardKey.KEY_SPACE)):

                current_screen = GameScreen.TITLE

            # DRAW LOOP #####################################################
            draw_texture_v(
                logo,
                Vector2(RENDER_WIDTH//2 - 32,
                        RENDER_HEIGHT//2 - 32
                ),
                WHITE
            )

        # TITLE SCREEN ######################################################
        elif current_screen == GameScreen.TITLE:

            # UPDATE LOOP #

            # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE):

                current_screen = GameScreen.GAMEPLAY

            # DRAW LOOP #

            draw_texture_v(
                background,
                Vector2(),
                WHITE
            )

            draw_text(
                TITLE,
                RENDER_WIDTH//2 - measure_text(TITLE, 20)//2,
                RENDER_HEIGHT//6,
                20,
                WHITE
            )

            draw_text(
                "PRESS SPACE TO PLAY",
                RENDER_WIDTH//2 - measure_text("PRESS SPACE TO PLAY", 10) // 2,
                RENDER_HEIGHT//6 * 5,
                10,
                WHITE
            )

        # GAMEPLAY SCREEN ###################################################
        elif current_screen == GameScreen.GAMEPLAY:

            # Update loop
            # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE):

                current_screen = GameScreen.END

            # Update player
            player.update()

            # Camera follows player
            camera.target = Vector2(
                player.pos.x + 8,
                player.pos.y + 8
            )

            # Draw loop
            # Lock screen to camera
            begin_mode_2d(camera)

            # Draw background
            draw_texture_v(
                background,
                Vector2(),
                WHITE
            )

            # Draw NPCs
            draw_texture_v(
                npc_sprites[0],
                Vector2(100, 100),
                 WHITE
            )

            draw_texture_v(
                npc_sprites[1],
                Vector2(300, 300),
                WHITE
            )

            # Draw player
            player.draw()

            end_mode_2d()

        # END SCREEN ########################################################
        elif current_screen == GameScreen.END:

            # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE):

                current_screen = GameScreen.CREDITS

            draw_text(
                "THE END",
                RENDER_WIDTH//2 - measure_text("THE END", 20)//2,
                RENDER_HEIGHT//2 - 10,
                20,
                WHITE
            )

        # CREDITS SCREEN ####################################################
        elif current_screen == GameScreen.CREDITS:

            # Check for screen switch conditions
            if is_key_pressed(KeyboardKey.KEY_SPACE):

                if is_key_pressed(KeyboardKey.KEY_Q):
                    exit()

            draw_text(
                f"Made by {CREATOR}",
                RENDER_WIDTH//2 -measure_text(f"Made by {CREATOR}", 10)//2,
                RENDER_HEIGHT//3 - 5,
                10,
                WHITE
            )

            draw_text(
                "PRESS SPACE TO PLAY AGAIN",
                RENDER_WIDTH//2 - measure_text("PRESS SPACE TO PLAY AGAIN", 10)//2,
                RENDER_HEIGHT//2 - 5,
                10,
                WHITE
            )

            draw_text(
                "PRESS Q TO QUIT",
                RENDER_WIDTH//2 - measure_text("PRESS Q TO QUIT", 10)//2,
                RENDER_HEIGHT//3 * 2,
                10,
                WHITE
            )

        end_texture_mode()

        # DRAW TO WINDOW CANVAS #################################################
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

# Anything that should be drawn at native resolution has to go here, between
# draw_texture_pro() and end_drawing()
        
        # Custom FPS and debug info toggle
        if show_fps:
            draw_text(
                f"{get_fps()} FPS",
                0,
                0,
                10,
                WHITE
            )

            draw_text(
                f"FRAME TIME: {dt:.4f}s",
                0,
                10,
                10,
                WHITE
            )

            draw_text(
                f"WINDOW RESOLUTION: {window_width, window_height}",
                0,
                20,
                10,
                WHITE
            )

            draw_text(
                f"RENDER RESOLUTION: {RENDER_WIDTH, RENDER_HEIGHT}",
                0,
                30,
                10,
                WHITE
            )

            draw_text(
                f"ZOOM: {camera.zoom}",
                0,
                40,
                10,
                WHITE
            )

            draw_text(
                f"PLAYER POSITION: {int(player.pos.x), int(player.pos.y)}",
                0,
                50,
                10,
                WHITE
            )

        # Close the loop
        end_drawing()

    # Clean up data when program ends

    #unload_music_stream()

    #unload_sound()

    #unload_font(primary_font)

    unload_image(logo_image)

    unload_texture(background)
    unload_texture(logo)
    unload_texture(player.texture)
    unload_texture(npc_sprites[0])
    unload_texture(npc_sprites[1])
    unload_texture(npc_sprites[2])

    unload_render_texture(target)

    close_window()

# Run main function upon execution
if __name__ == "__main__":
    main()
