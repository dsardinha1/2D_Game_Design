import arcade
import pathlib

"""Global Variables"""
SCREEN_W = 800
SCREEN_H = 600
SCREEN_TITLE = "Quaker's Hunt"
SPRITE_SCALING = 0.25
MOVEMENT_SPEED = 10


class BasePlayer(arcade.Sprite):

    def __init__(self,image_location, scaling, x_position, y_position):
        super().__init__(filename=image_location, scale=scaling, center_x=x_position,center_y=y_position)
        self.direction = None

    def move(self):
        """Player's direction logic"""
        """Makes the player sprite bounce from the borders of the screen"""
        if(self.top > SCREEN_H):
            self.center_y -= 1
            self.direction = None
        elif (self.bottom < 0):
            self.center_y += 1
            self.direction = None

        if (self.direction == "up"):
            self.center_y += MOVEMENT_SPEED
        elif (self.direction == "down"):
            self.center_y -= MOVEMENT_SPEED
        pass


class MinimalArcade(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        """Sets up file path variables"""
        self.sound_path = None
        self.image_path = None

        """Sets background variable"""
        self.background = None
        self.background_x = 0
        self.background_y = 0
        self.background_reflect_x = 0
        self.background_reflect_y = 0

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None
        self.player_weapon_list = None

        """Holds player Sprite"""
        self.player_sprite = None
        self.player_weapon_sprite = None

        """Holds the sound variables"""
        self.weapon_throw_sound = None

        """Sets background color"""
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

    def setup(self):
        # Set up your game here
        self.sound_path = str(pathlib.Path.cwd()) + '/audio/'
        self.image_path = str(pathlib.Path.cwd()) + '/images/'

        """Imports background images for side scrolling"""
        self.background = arcade.load_texture(self.image_path + "background.png")
        self.background_reflect = arcade.load_texture(self.image_path + "background_reflect.png")
        self.background_x = SCREEN_W
        self.background_y = SCREEN_H
        self.background_reflect_x = SCREEN_W*3
        self.background_reflect_y = SCREEN_H

        """Sets up sprites' list"""
        self.player_list= arcade.SpriteList()
        self.player_weapon_list = arcade.SpriteList()

        """Sets weapon sound"""

        self.weapon_throw_sound = arcade.load_sound(self.sound_path + "throwing_spear.wav")

        #Image from OrgeofWart on opengameart.org
        """Sets up player"""
        self.player_sprite = BasePlayer(self.image_path + "player.png", SPRITE_SCALING, 200, 200)
        self.player_list.append(self.player_sprite)

    def on_key_press(self, key, modifiers):
        """Controls when  key is pressed"""
        if (key == arcade.key.UP or key == arcade.key.W):
            self.player_sprite.direction = "up"
        elif (key == arcade.key.DOWN or key == arcade.key.S):
            self.player_sprite.direction = "down"
        elif (key == arcade.key.SPACE):
            self.player_shoot()

    def on_key_release(self, key, modifiers):
        """Controls when a key is released"""

        """Resets player's sprite movement variable"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
            self.player_sprite.direction == "up":
            self.player_sprite.direction = None
        elif (key == arcade.key.DOWN or key == arcade.key.S) and \
            self.player_sprite.direction == "down":
            self.player_sprite.direction = None

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle((self.background_x) // 2 , self.background_y // 2,
                                      SCREEN_W, SCREEN_H, self.background)
        arcade.draw_texture_rectangle(self.background_reflect_x // 2, self.background_y // 2, SCREEN_W, SCREEN_H, self.background_reflect)

        """Draws the sprites"""
        self.player_list.draw()
        self.player_weapon_list.draw()

        """Finalizes the screen render"""
        arcade.finish_render()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        #print("center_X2", self.background_reflect_x)
        """logic for scrollng background to the left"""
        """Background One"""
        if (self.background_x > -(SCREEN_W)):
            self.background_x -= 1
        else:
            self.background_x = SCREEN_W *3 - 1

        """Background Two_Reflect"""
        if(self.background_reflect_x > -(SCREEN_W)):
            self.background_reflect_x -= 1
        else:
            self.background_reflect_x = SCREEN_W * 3 - 1

        """Calls to move player"""
        self.player_sprite.move()
        self.player_weapon_list.update()

    def player_shoot(self):
        """Logic when the player activates weapon"""
        arcade.play_sound(self.weapon_throw_sound)
        self.player_weapon_sprite = BasePlayer("images/spear.png", SPRITE_SCALING,  100, 150)
        self.player_weapon_sprite.center_x = self.player_sprite.center_x
        self.player_weapon_sprite.center_y = self.player_sprite.center_y
        self.player_weapon_sprite.change_x = MOVEMENT_SPEED
        self.player_weapon_list.append(self.player_weapon_sprite)
        arcade.stop_sound(self.weapon_throw_sound)
        pass



def main():
    """Main method"""
    window = MinimalArcade(SCREEN_W , SCREEN_H, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == '__main__':
    main()