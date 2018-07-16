import pygame
from lib import labygen
from pygame.locals import *
import json
import random
from threading import *


def TestObjectCollision(player, objectlist):
    if(len(objectlist) != 0):
        for obj in objectlist:
            if((obj.posx == player.posx) and (obj.posy == player.posy)):
                return ["True", obj]


class App:
    COLLISION = {}  # Dictionnary that stock position of walls/path

    def __init__(self, w_height, w_lenght):  # Init App Class
        self._running = True
        self._window = None
        self.size = w_height, w_lenght

    def on_init(self):  # Init Window
        pygame.init()
        self.textfont = pygame.font.SysFont("monospace", 18)
        self._window = pygame.display.set_mode(
            self.size, HWSURFACE | DOUBLEBUF)
        self._window_resize = self._window.copy()
        self._running = True

    # Each time that a event is caught in on_execute it check here for actions
    def on_event(self, event):
        if event.type == pygame.QUIT:  # If click on the redcross to quit
            self._running = False

        if event.type == VIDEORESIZE:  # Refresh window size when resize event is caught
            self._window = pygame.display.set_mode(
                event.dict['size'], HWSURFACE | DOUBLEBUF)
            self._window.blit(pygame.transform.scale(
                self._window_resize, event.dict['size']), (0, 0))
            pygame.display.flip()

        if self.playerobj.alive:
            if event.type == pygame.KEYDOWN:  # Get Key Events
                if event.key == pygame.K_RIGHT:
                    if self.COLLISION.get((self.playerobj.posx + 30, self.playerobj.posy)) == 1:
                        self.playerobj.move_right(30)
                if event.key == pygame.K_LEFT:
                    if self.COLLISION.get((self.playerobj.posx - 30, self.playerobj.posy)) == 1:
                        self.playerobj.move_left(30)
                if event.key == pygame.K_UP:
                    if self.COLLISION.get((self.playerobj.posx, self.playerobj.posy - 30)) == 1:
                        self.playerobj.move_up(30)
                if event.key == pygame.K_DOWN:
                    if self.COLLISION.get((self.playerobj.posx, self.playerobj.posy + 30)) == 1:
                        self.playerobj.move_down(30)
                self.update = True

    def on_gui(self):
        self.label = self.textfont.render("Loot Collected : " + str(
            self.playerobj.lootcollected) + "/" + str(self.objnumber), 1, (255, 255, 255))
        if self.win:
            self.wintext = self.textfont.render("YOU WIN", 1, (255, 255, 255))
        if self.loose:
            self.loosetext = self.textfont.render(
                "YOU LOOSE", 1, (255, 255, 255))

    def on_loop(self):
        if(len(self.loots) != 0):  # Check if loot is all collected or not
            # Making a simple check with oldppos vars to avoid collision check
            # every frame
            if(self.oldposx != self.playerobj.posx or self.oldposy != self.playerobj.posy):
                # Use The Function to test collision between player and objects
                ObjCollision = TestObjectCollision(self.playerobj, self.loots)
                if(ObjCollision != None):  # If there's a collision
                    if (ObjCollision[0] == "True"):
                        self.playerobj.lootcollected += 1
                        # Remove the loot from the list
                        self.loots.remove(ObjCollision[1])
                        # Remove the loot from the render
                        self.obj_group.remove(ObjCollision[1])
                self.oldposx = self.playerobj.posx  # Update position when it have changed
                self.oldposy = self.playerobj.posy

        # If player is front of the guard / HARDCODED : The test check only
        # left of the guard
        if(self.playerobj.posx == self.guard.posx - 30 and self.playerobj.posy == self.guard.posy):
            if(len(self.loots) == 0):
                self.win = True
                self.playerobj.alive = False
                t = Timer(2, self.end_game)
                t.start()
            else:
                self.loose = True
                self.playerobj.alive = False
                t = Timer(3, self.end_game)
                t.start()

    def end_game(self):
        self._running = False

    def on_render(self):  # The render of the game each frames
        self.font_group.draw(self._window)  # Render Wall and Path
        self.obj_group.draw(self._window)  # Render Objects And Player
        self._window.blit(self.label, (100, 0))  # Render text from on_gui()
        if self.win:
            self._window.blit(
                self.wintext, (self.size[1] / 2, self.size[0] / 2))
        if self.loose:
            self._window.blit(
                self.loosetext, (self.size[1] / 2, self.size[0] / 2))
        pygame.display.flip()
        self.update = False

    def on_cleanup(self):  # Quit app
        pygame.quit()

    def on_execute(self):  # Main function
        # If window not launched stop all
        if self.on_init() == False:
            self._running = False

        self.win = False
        self.loose = False

        self.font_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()

        # Used for collision check in loop section
        self.oldposx = 0
        self.oldposy = 30

        # Used for Optimisation
        self.update = True

        self.loots = []

        self.open_lab("LabyrinthFiles/test.labyrinth")

        # main loop
        while (self._running):
            for event in pygame.event.get():  # For each event caught by pygame
                self.on_event(event)  # Check if a action is bind
            if self.update:  # If Player moved update all game elements used for optimisation
                self.on_loop()  # Game Loop
                self.on_gui()  # Draw GUI
                self.on_render()  # Game Render
        self.on_cleanup()  # On Quit

    def lab_init(self):
        lab = labygen.Labyrinth()
        lab.CreateLab("test", 15, 15)

    def open_lab(self, filename):  # Open labyrinth
        file = open(filename, "r")
        y = -1
        x = -1
        self.objnumber = random.randint(1, 8)
        if file.mode == 'r':
            content = json.load(file)  # Load labyrinth is json
            for lenght in content:
                y += 1
                for casetype in lenght:
                    x += 1
                    if(casetype == 0):  # type 0 is wall
                        wall = Wall(x * 30, y * 30)
                        # add wall to background sprite group
                        self.font_group.add(wall)
                        self.COLLISION.update({(wall.posx, wall.posy): 0})
                    elif(casetype == 1):  # type 1 is path
                        path = Path(x * 30, y * 30)
                        # add path to background sprite group
                        self.font_group.add(path)
                        self.COLLISION.update({(path.posx, path.posy): 1})
                    elif(casetype == 2):  # type 2 is player
                        self.playerobj = Player(x * 30, y * 30)
                        self.obj_group.add(self.playerobj)
                        path = Path(x * 30, y * 30)
                        self.font_group.add(path)
                        self.COLLISION.update({(path.posx, path.posy): 1})
                    elif(casetype == 3):  # type 3 is guard
                        self.guard = Guard(x * 30, y * 30)
                        self.obj_group.add(self.guard)
                        path = Path(x * 30, y * 30)
                        self.font_group.add(path)
                        self.COLLISION.update({(path.posx, path.posy): 1})
                x = -1

            i = 0
            while i < self.objnumber:  # Spawn objects randomly
                position = random.choice(list(self.COLLISION.items()))
                if (position[1] == 1):
                    if(position[0][0] != self.playerobj.posx and position[0][1] != self.playerobj.posy):
                        if(position[0][0] != self.guard.posx and position[0][1] != self.guard.posy):
                            i += 1
                            loot = Loot(position[0][0], position[0][1])
                            self.obj_group.add(loot)
                            self.loots.append(loot)

            # Make the windows size fit the labyrinth size
            for lenght in content:
                for casetype in lenght:
                    x += 1
                self.size = ((y + 1) * 30, (x + 1) * 30)
                x = -1

            self._window = pygame.display.set_mode(
                self.size, HWSURFACE | DOUBLEBUF)


# Player Sprite Class
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/macgyver.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.posx + 15, self.posy + 15)
        self.lootcollected = 0
        self.alive = True

    # Movement definitions
    def move_right(self, pixels):
        self.rect.x += pixels
        self.posx += pixels

    def move_left(self, pixels):
        self.rect.x -= pixels
        self.posx -= pixels

    def move_up(self, pixels):
        self.rect.y -= pixels
        self.posy -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels
        self.posy += pixels


# Guard Sprite Class:
class Guard(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/guard.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x + 16, y + 16)


# Wall Sprite Class
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/wall.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x + 16, y + 16)

# Path Sprite Class
class Path(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/path.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x + 16, y + 16)

# Loot Sprite Class
class Loot(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/lootmodif.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x + 16, y + 16)


if __name__ == "__main__":
    game = App(450, 450)
    game.on_execute()
