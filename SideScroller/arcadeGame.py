import random
import threading

import arcade
import pathlib

"""Global Variables"""
SCREEN_W = 800
SCREEN_H = 600
SCREEN_TITLE = "Quaker's Hunt"
PLAYER_SPRITE_SCALING = 0.25
MOVEMENT_SPEED = 10

"""Enemy Variables"""
ENEMY_SPRITE_SCALING = 0.625


class BaseEnemy(arcade.Sprite):
    def __init__(self,image_location, scaling, x_position, y_position, motionSpeed = 0, moveAuto = False):
        super().__init__(filename=image_location, scale=scaling, center_x=x_position,center_y=y_position)
        self.moveAuto = moveAuto
        self.motionSpeed = motionSpeed

    def update(self):
        if self.moveAuto == True:
           self.center_x -= self.motionSpeed
        pass




class BasePlayer(arcade.Sprite):

    def __init__(self,image_location, scaling, x_position, y_position):
        super().__init__(filename=image_location, scale=scaling, center_x=x_position,center_y=y_position)
        self.direction = None
        self.fire_weapon = True

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

    def changeWeaponFire(self):
        self.fire_weapon = not self.fire_weapon

class MinimalArcade(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        "Sets up current game state variable"
        self.currentGameState = None

        """Sets up file path variables"""
        self.sound_path = None
        self.image_path = None

        """Sets background variable"""
        self.background = None
        self.background_x, background_y = 0, 0
        self.background_reflect_x, background_reflect_y = 0, 0


        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None
        self.player_weapon_list = None
        self.enemy_list = None
        self.enemy_weapon_list = None

        """Holds player Sprite"""
        self.player_sprite = None
        self.player_weapon_sprite = None
        self.enemy_sprite = None
        self.enemy_weapon_sprite = None

        """Holds the sound variables"""
        self.weapon_throw_sound = None
        self.energy_sound = None
        self.player_death_sound = None
        self.enemy_death_sound = None

        """Sets background color"""
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

    def setup(self):
        # Set up your game here
        """Check collision logic here"""
        self.currentGameState = 'GAME_RUNNING'

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
        self.enemy_list = arcade.SpriteList()
        self.enemy_weapon_list = arcade.SpriteList()

        """Sets weapon sound"""
        self.weapon_throw_sound = arcade.load_sound(self.sound_path + "throwing_spear.wav")
        self.energy_sound = arcade.load_sound(self.sound_path + "energy.wav")
        self.enemy_death_sound = arcade.load_sound(self.sound_path + "enemy_death.wav")
        self.player_death_sound = arcade.load_sound(self.sound_path + "player_death.wav")

        #Image from OrgeofWart on opengameart.org
        """Sets up player"""
        self.player_sprite = BasePlayer(self.image_path + "player.png", PLAYER_SPRITE_SCALING, 200, 200)
        self.player_weapon_sprite = BasePlayer(self.image_path + "spear.png", PLAYER_SPRITE_SCALING, 100, 150)
        self.player_list.append(self.player_sprite)

        """Function to spawn first enemy is called"""
        self.spawn_enemy()


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

        if self.currentGameState == 'GAME_RUNNING':
            arcade.draw_texture_rectangle((self.background_x) // 2 , self.background_y // 2,
                                              SCREEN_W, SCREEN_H, self.background)
            arcade.draw_texture_rectangle(self.background_reflect_x // 2, self.background_y // 2, SCREEN_W, SCREEN_H, self.background_reflect)

            """Draws the sprites"""
            self.player_list.draw()
            self.player_weapon_list.draw()
            self.enemy_weapon_list.draw()
            self.enemy_list.draw()
        elif self.currentGameState == 'GAME_OVER':
            self.draw_game_over()
            pass


        """Finalizes the screen render"""
        arcade.finish_render()

    def draw_game_over(self):
        """Logic for Game over screen"""
        arcade.draw_text("You lost!", SCREEN_W/2, SCREEN_H/2, arcade.color.ANTIQUE_RUBY, font_size=48, font_name='arial', anchor_x='center')
        arcade.set_background_color(arcade.color.PURPLE_HEART)
        pass

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        #print("center_X2", self.background_reflect_x)
        """logic for scrollng background to the left"""

        if self.currentGameState == 'GAME_RUNNING':

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
            self.enemy_sprite.update()
            self.enemy_weapon_list.update()

            """Kills spears the go off screen and enable for periodic shots"""
            for spear in self.player_weapon_list:
                if spear.center_x == SCREEN_W:
                    spear.kill()
                elif spear.center_x ==SCREEN_W-200:
                    self.player_sprite.changeWeaponFire()

            """Randomly spawns an enemy couple of seconds"""
            if random.randrange(250) == 0:
                self.spawn_enemy()
            self.enemy_shoot()

            """Creates list for player spears with enemy mobs"""
            for spear in self.player_weapon_list:
                spear_hit_list = arcade.check_for_collision_with_list(spear, self.enemy_list)
                """Removes enemies from the hit list"""
                for enemy in spear_hit_list:
                    enemy.remove_from_sprite_lists()
                    arcade.play_sound(self.enemy_death_sound)

            """Creates list for enemys' energy blasts with player """
            for energy_blast in self.enemy_weapon_list:
                enemy_hit_list = arcade.check_for_collision_with_list(energy_blast, self.player_list)
                """Removes enemies from the hit list"""
                for player in enemy_hit_list:
                    player.remove_from_sprite_lists()
                    arcade.play_sound(self.player_death_sound)
                    arcade.pause(2)
                    self.currentGameState = 'GAME_OVER'
        elif self.currentGameState == 'GAME_OVER':
            pass

    def spawn_enemy(self):
        #Image is by TearOfTheStar on opengameart.org
        self.enemy_sprite = BaseEnemy(self.image_path + "enemy.png", ENEMY_SPRITE_SCALING, random.randrange(SCREEN_W / 2, SCREEN_W),
                                      random.randrange(SCREEN_H))
        self.enemy_list.append(self.enemy_sprite)
        pass

    def player_shoot(self):
        """Logic when the player activates weapon"""
        if self.player_sprite.fire_weapon == True:
            arcade.play_sound(self.weapon_throw_sound)
            self.player_weapon_sprite = BasePlayer(self.image_path + "spear.png", PLAYER_SPRITE_SCALING, 100, 150)
            self.player_weapon_sprite.center_x = self.player_sprite.center_x
            self.player_weapon_sprite.center_y = self.player_sprite.center_y
            self.player_weapon_sprite.change_x = MOVEMENT_SPEED
            self.player_weapon_list.append(self.player_weapon_sprite)
            self.player_sprite.changeWeaponFire()
        pass

    def enemy_shoot(self):
        """Goes through each enemy"""
        for enemy in self.enemy_list:
            #if the following random condition meets, then that enemy fire a shoot
            if random.randrange(200) == 25:
                enemy_weapon_sprite = BaseEnemy(self.image_path + "energy_Blast.png", PLAYER_SPRITE_SCALING / 2, enemy.center_x,
                                                enemy.center_y, 5, True)

                self.enemy_weapon_list.append(enemy_weapon_sprite)
                arcade.play_sound(self.energy_sound)
        pass

def main():
    """Main method"""
    window = MinimalArcade(SCREEN_W , SCREEN_H, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == '__main__':
    main()