import arcade
import pathlib

"""Global Variables"""
SCREEN_W = 800
SCREEN_H = 600
SCREEN_TITLE = "Quaker's Hunt"
SPRITE_SCALING = 0.25

class BasePlayer(arcade.Sprite):

    def __init__(self,image_location, scaling, x_position, y_position):
        super().__init__(filename=image_location, scale=scaling, center_x=x_position,center_y=y_position)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_W- 1:
            self.right = SCREEN_W - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_H - 1:
            self.top = SCREEN_H - 1

class MinimalArcade(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        """This lets python know where the image and audio files will be located easier"""
        """.cwd is the file path of the current working directory"""
        """self.image_path = pathlib.Path.cwd() / 'Assests' / image_name"""
        """Sets background variable"""
        self.background = None
        self.background_x = 0
        self.background_y = 0;

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None

        """Holds player Sprite"""
        self.player_sprite = None

        """Sets background color"""
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

    def setup(self):
        # Set up your game here
        """Imports background"""
        self.background = arcade.load_texture("images/background.png")
        self.background_reflect = arcade.load_texture("images/background_reflect.png")
        self.background_x = SCREEN_W
        self.background_y = SCREEN_H

        """Sets up player sprite list"""
        self.player_list= arcade.SpriteList()

        """Sets up player"""
        self.player_sprite = BasePlayer("images/player.png", SPRITE_SCALING, 200, 200)
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle((self.background_x) // 2 , self.background_y // 2,
                                      SCREEN_W, SCREEN_H, self.background)
        arcade.draw_texture_rectangle((self.background_x + SCREEN_W*2) // 2, self.background_y // 2, SCREEN_W, SCREEN_H, self.background_reflect)

        """Draws the sprites"""
        self.player_list.draw()

        """Finalizes the screen render"""
        arcade.finish_render()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        print("center_x", self.background_x)
        """logic for scrollng background to the left"""

        if self.background_x > -(SCREEN_W*2):
            self.background_x -= 1
        else:
            self.background_x = 800


        """while 1:
            arcade.draw_texture_rectangle(self.background_x, self.background_y, SCREEN_W, SCREEN_H, self.background)
            if self.background_x < 1080:
                self.background_x += 1
            else:
                self.background = 0
        """



def main():
    """Main method"""
    window = MinimalArcade(SCREEN_W , SCREEN_H, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == '__main__':
    main()