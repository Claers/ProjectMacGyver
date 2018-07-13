import pygame
from lib import labygen 
from pygame.locals import *
import json

class App:

	COLLISION = {}

	def __init__(self,w_height,w_lenght): #Init App Class
		self._running = True
		self._window = None
		self.size = w_height, w_lenght

	def on_init(self): #Init Window
		pygame.init()
		self._window = pygame.display.set_mode(self.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
		self._window_resize = self._window.copy()
		self._running = True

	def on_event(self, event): #Each time that a event is caught in on_execute it check here for actions
		if event.type == pygame.QUIT: #If click on the redcross to quit
			self._running = False
		if event.type == VIDEORESIZE: #Refresh window size when resize event is caught
			self._window = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)
			self._window.blit(pygame.transform.scale(self._window_resize,event.dict['size']), (0,0))
			pygame.display.flip()


	def on_loop(self):
		playerp = self._window_resize.blit(self.player, self.player_pos)

	def on_render(self): #The render of the game each frames
		pygame.display.flip()

	def on_cleanup(self): #Quit app
		pygame.quit()

	def on_execute(self): #Main function 
		#if window not launched stop all
		if self.on_init() == False:
			self._running = False

		#Load textures before runtime of App
		self.wall = pygame.image.load("Assets/wall.png").convert_alpha()
		self.path = pygame.image.load("Assets/path.png").convert_alpha()
		self.player = pygame.image.load("Assets/macgyver.png").convert_alpha()

		self.player_pos = (0,0)

		self.open_lab("LabyrinthFiles/test.labyrinth")
		print(self.COLLISION.get(0,0))

		#main loop
		while (self._running):
			for event in pygame.event.get(): #Fo each event caught by pygame
				self.on_event(event) #Check if a action is bind
			self.on_loop() # Game Loop
			self.on_render() # Game Render
		self.on_cleanup() #On Quit

	def lab_init(self): 
		lab = labygen.Labyrinth()
		lab.CreateLab("test",20,20)

	def open_lab(self,filename): #Open labyrinth
		file = open(filename,"r")
		y = -1
		x = -1
		if file.mode == 'r':
			content = json.load(file) #Load labyrinth is json
			for lenght in content:
				y += 1
				for casetype in lenght:
					x += 1
					if(casetype == 0): #type 0 is wall
						wall = self._window_resize.blit(self.wall, (x*30,y*30))
						wall.change_layer()
						self.COLLISION.update({(wall.x,wall.y) : 0})
					elif(casetype == 1): #type 1 is path
						path = self._window_resize.blit(self.path, (x*30,y*30))
						self.COLLISION.update({(path.x,path.y) : 0})
				x = -1
			



class Player:
	def __init__(self,posx,posy):
		self.posx = posx
		self.posy = posy




if __name__ == "__main__":
	game = App(1200,750)
	game.on_execute()

	

