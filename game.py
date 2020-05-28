import os
import pygame
from random import randint, choice
pygame.init()


tela = pygame.display.set_mode((800, 480))
pygame.display.set_caption("@noobpythonbr")

clock = pygame.time.Clock()
background = pygame.image.load(os.path.join("images/background.png"))

score = 0
font = pygame.font.SysFont("System", 22, bold=True, italic=False)

class Dino:
	def __init__(self):
		self.image = pygame.image.load(os.path.join("images/dino.png"))
		# definição das dimensões do sprite
		self.sprite_x = 0
		self.sprite_w = 32
		self.sprite_h = 35
		self.sprite = self.image.subsurface((self.sprite_x, 0), (self.sprite_w, self.sprite_h))
		# definição da velocidade de transição dos sprites
		self.sprite_count = 0
		self.sprite_speed = 5
		
		# definições da área de colisão e posicionamento
		self.rect = self.sprite.get_rect()
		self.rect.x, self.rect.y = 100, 210
      	# self.rect tem 4 atributos [ x (posição no eixo X), y (posição no eixo Y), w (largura), h (altura) ]

		# definições do sistema de pulo
		self.jump_speed = 5
		self.jump_force = 50
		self.weight = 1
		self.is_jumping = True
		
	def update(self):
		'''
		Animação dos sprites
		'''
      
		if self.sprite_count == self.sprite_speed:
			if self.sprite_x < self.image.get_size()[0] - (self.rect.w + 1):
				self.sprite_x += self.sprite_w
			else:
				self.sprite_x = 0		
			self.sprite_count = 0
		self.sprite_count += 1
		
		'''
		Sitema de pulo.
		'''
              
		if self.is_jumping == True:
			if self.jump_speed > 0:
				F = ( 0.5 * self.weight * (self.jump_speed * self.jump_speed))
			else:
				F = -( 0.5 * self.weight * (self.jump_speed * self.jump_speed))			              
			self.rect.y = self.rect.y - F						
			self.jump_speed -=  1

			if self.rect.y >= 370:
				self.rect.y = 370
				self.is_jumping = False
				self.jump_speed = 8 					
		
		'''
		Plotagem do sprite na tela.
		'''
              
		self.sprite = self.image.subsurface((self.sprite_x, 0), (self.sprite_w, self.sprite_h))
		tela.blit(self.sprite, (self.rect.x, self.rect.y))
		
	def jump(self):
		'''
		Verifica o pressionamento da tecla espaço e checa se o dino já não está pulando,
		então, troca o status de self.is_jumping para verdadeiro.
		'''

		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			if self.is_jumping == False:
				self.is_jumping = True
				
				
	def check_collision(self, element):
		'''
		Verifica a colisão do dino com os obstáculos.
		'''	
      
		global score
		self.element = element # grupo de elementos que podem colidir com o dino
		for e in self.element:
			if self.rect.colliderect(e.rect):
				pygame.time.delay(1500)
				e.rect.x -= 100			
				score = 0

class Cactus:
	def __init__(self):		
		self.image = pygame.image.load(os.path.join("images/cactus.png"))
		self.sprite_x = choice([0, 32])
		self.sprite_y = 0
		self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),(32, 32))
		self.rect = self.sprite.get_rect()
		self.rect.x, self.rect.y = 1000, 370
		self.speed = 8

	def update(self):                                
		if score < 50:
			self.sprite_y = 0
		elif score < 100:                
			self.sprite_y = 64
		else:            
			self.sprite_y = 32

		if self.rect.x + self.rect.w < 0:			
			self.rect.x = randint(800, 900)
			self.sprite_x = choice([0, 32])
			self.sprite = self.image.subsurface((self.sprite_x, self.sprite_y),(32, 32))
		self.rect.x -= self.speed				
		tela.blit(self.sprite, (self.rect.x, self.rect.y))


class Clouds:
    def __init__(self):
        self.image = pygame.image.load(os.path.join("images/cloud.png"))                                
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, randint(0, 270)


    def update(self):							
        if self.rect.x + self.rect.w < 0:
            self.rect.x = 800
            self.rect.y = randint(0, 270)			                                                
        self.rect.x -= 1						
        tela.blit(self.image, (self.rect.x, self.rect.y))

									
cactus1 = Cactus()				
cactus2 = Cactus(); cactus2.rect.x = 500
cactus = [cactus1, cactus2]

dino = Dino()

nuvem1 = Clouds()
nuvem2 = Clouds(); nuvem2.rect.x = 200
nuvem3 = Clouds(); nuvem3.rect.x = 400
nuvem4 = Clouds(); nuvem4.rect.x = 560
nuvem5 = Clouds(); nuvem5.rect.x = 780
nuvens = [nuvem1, nuvem2, nuvem3, nuvem4, nuvem5]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    if score < 100:
        tela.blit(background.subsurface((0,0),(800,480)), (0, 0))
    elif score < 300:
        tela.blit(background.subsurface((800,0),(800,480)), (0, 0))
    else:
        tela.blit(background.subsurface((1600,0),(800,480)), (0, 0))
    
    [n.update() for n in nuvens]
    [c.update() for c in cactus]    

    dino.update()
    dino.check_collision(cactus)
    dino.jump()
        
    score += 0.1
    s = font.render(str(int(score)), True, (0,0,0), None)
    tela.blit(s, (700, 10))

    clock.tick(30)
    pygame.display.update()
