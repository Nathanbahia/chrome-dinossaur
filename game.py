### CREATED BY: NATHAN BAHIA - @NOOBPYTHONBR ###
### SOUNDTRACK: WYS - SNOWMAN
### PIXEL ART MADE WITH PISKELAPP.COM

import os
import pygame
from random import randint, choice

pygame.init()

tela = pygame.display.set_mode((500, 300))
pygame.display.set_caption("@noobpythonbr")
music = pygame.mixer.Sound(os.path.join("sounds/music.ogg"))
clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont("System", 18, bold=True, italic=False)

class Dino:
	def __init__(self):
		self.image = pygame.image.load(os.path.join("images/dino.png"))
		self.sprite_x = 0
		self.sprite_w = 32
		self.sprite_h = 35
		self.sprite_count = 0
		self.sprite_speed = 5
		self.sprite = self.image.subsurface((self.sprite_x, 0), (self.sprite_w, self.sprite_h))
		self.rect = self.sprite.get_rect()
		self.rect.x, self.rect.y = 100, 210

		self.jump_speed = 5
		self.jump_force = 50
		self.weight = 1
		self.is_jumping = True
		
	def update(self):
		if self.sprite_count == self.sprite_speed:
			if self.sprite_x < self.image.get_size()[0] - (self.rect.w + 1):
				self.sprite_x += self.sprite_w
			else:
				self.sprite_x = 0		
			self.sprite_count = 0
		self.sprite_count += 1
		
		
		if self.is_jumping == True:
			if self.jump_speed > 0:
				F = ( 0.5 * self.weight * (self.jump_speed * self.jump_speed))
			else:
				F = -( 0.5 * self.weight * (self.jump_speed * self.jump_speed))			
			self.rect.y = self.rect.y - F
						
			self.jump_speed -=  1

			if self.rect.y >= 210:
				self.rect.y = 210
				self.is_jumping = False
				self.jump_speed = 8 			
		
		self.jump()
		
		self.sprite = self.image.subsurface((self.sprite_x, 0), (self.sprite_w, self.sprite_h))
		tela.blit(self.sprite, (self.rect.x, self.rect.y))
		
	def jump(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			if self.is_jumping == False:
				self.is_jumping = True
				
				
	def check_collision(self, element):
		self.element = element
		if self.rect.colliderect(self.element.rect):
			pygame.time.delay(1500)
			self.element.rect.x = 600
			global score
			score = 0
		
		
class Cactus:
	def __init__(self):		
		self.image = pygame.image.load(os.path.join("images/cactus.png"))
		self.sprite_x = choice([0, 32])
		self.sprite = self.image.subsurface((self.sprite_x, 0),(32, 32))
		self.rect = self.sprite.get_rect()
		self.rect.x, self.rect.y = 1000, 210
		self.speed = 8
		
		
	def update(self):
		if self.rect.x + self.rect.w < 0:			
			self.rect.x = randint(500, 700)
			self.sprite_x = choice([0, 32])	
			self.sprite = self.image.subsurface((self.sprite_x, 0),(32, 32))
		self.rect.x -= self.speed				
		tela.blit(self.sprite, (self.rect.x, self.rect.y))


class Clouds:
	def __init__(self):
		self.image = pygame.image.load(os.path.join("images/cloud.png"))
		self.sprite_x = choice([0, 64, 128])
		self.sprite = self.image.subsurface((self.sprite_x, 0), (64, 32))
		self.rect = self.sprite.get_rect()
		self.rect.x, self.rect.y = 50, randint(0, 130)			
						
						
	def update(self):							
		if self.rect.x + self.rect.w < 0:
			self.rect.x = 500
			self.rect.y = randint(0, 130)			
			self.sprite_x = choice([0, 64, 128])
			self.sprite = self.image.subsurface((self.sprite_x, 0), (64, 32))
		
		self.rect.x -= 1						
		tela.blit(self.sprite, (self.rect.x, self.rect.y))				
									
cactus = Cactus()				
dino = Dino()

c1 = Clouds()
c2 = Clouds(); c2.rect.x = 200
c3 = Clouds(); c3.rect.x = 400
clouds = [c1, c2, c3]

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	
	tela.fill((150,30,50))
	tela.blit(pygame.image.load(os.path.join("images/mountains.png")), (0, 0))
	music.play()
		
	[c.update() for c in clouds]
	cactus.update()
	dino.update()
	dino.check_collision(cactus)
	
	score += 0.1
	s = font.render(str(int(score)), True, (0,0,0), None)
	tela.blit(s, (450, 10))
		
	clock.tick(30)
	pygame.display.update()
