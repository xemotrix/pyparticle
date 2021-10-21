import pygame
import numpy as np

import random
WHITE = (255,255,255)

class particle:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.x_v = random.randint(-1000,1000)/200.0
		self.y_v = random.randint(-1000,1000)/200.0
		#self.y_v = -10.0

		self.life_span = 60*5
		self.timer = random.randint(0,self.life_span)

	
		self.color = WHITE
		
	@property
	def radius(self):
		return int(40 * (self.timer/self.life_span))

	def update(self, screen, current_w, current_h):

		if self.timer <= 0:
			return False

		if self.x<0 or self.x>current_w or self.y<0 or self.y>current_h:
			return False

		#gravity
		#self.y_v -= 0.25
		#wind
		#self.x_v += 0.3

		color_value = 255*(self.timer/self.life_span)
		self.color = (color_value, self.color[1], self.color[2])
		
		self.y_v += random.randint(-100,100)/100.0
		self.x_v += random.randint(-100,100)/100.0


		speed_cap = 5
		if self.y_v > speed_cap:
			self.y_v = speed_cap
		elif self.y_v < -speed_cap:
			self.y_v = -speed_cap

		if self.x_v > speed_cap:
			self.x_v = speed_cap
		elif self.x_v < -speed_cap:
			self.x_v = -speed_cap

		self.x = self.x + self.x_v
		self.y = self.y + self.y_v

		self.timer -= 1

		return True
		

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.x),int(self.y)), self.radius, width=0)
		pygame.draw.circle(screen, (0,0,0), (int(self.x),int(self.y)), self.radius, width=1)



if __name__ == '__main__':

	pygame.init()
	clock = pygame.time.Clock()
	infoObject = pygame.display.Info()
	current_w, current_h = infoObject.current_w, infoObject.current_h

	screen = pygame.display.set_mode((current_w,current_h), pygame.FULLSCREEN)
	#S = 1000
	#screen = pygame.display.set_mode((S,S))
	
	particles = []

	for i in range(1000):
		particles.append(particle(500,500))
	
	generating = False

	running = True
	count_f = 0
	while running:
		
		screen.fill((0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				generating = True

			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				generating = False

		mouse_x, mouse_y = pygame.mouse.get_pos()
		if generating:
			for _ in range(10):
				particles.append(particle(mouse_x,mouse_y))

		p_to_remove = []
		for p in particles:
			if not p.update(screen, current_w, current_h):
				p_to_remove.append(p)
			else:
				p.draw(screen)

		for p in p_to_remove:	
			particles.remove(p)

		count_f += 1
		if count_f >= 60:
			count_f = 0
			print('fps:',int(clock.get_fps()), 'particles:', len(particles))

		clock.tick(60)
		pygame.display.update()