import arcade
import pathlib

"""Global Variables"""
SCREEN_W = 800
SCREEN_H = 600
SCREEN_TITLE = "Quaker's Hunt"

class MinimalArcade(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        """This lets python know where the image and audio files will be located easier"""
        """.cwd is the file path of the current working directory"""
        """self.image_path = pathlib.Path.cwd() / 'Assests' / image_name"""
        """Sets background variable"""
        self.background = None

        """Sets background color"""
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

    def setup(self):
        # Set up your game here
        """Imports background"""
        self.background = arcade.load_texture("images/background.png")
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_W// 2, SCREEN_H // 2,
                                      SCREEN_W, SCREEN_H, self.background)
        """Finalizes the screen render"""
        arcade.finish_render()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass

def main():
    """Main method"""
    window = MinimalArcade(SCREEN_W , SCREEN_H, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == '__main__':
    main()