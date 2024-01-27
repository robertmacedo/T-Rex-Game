#IMPORTAÇÕES
from cmath import rect
import pygame 
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice


#INICIALIZANDO O PYGAME
pygame.init()


#VÍDEO
'''CONFIGURAÇÕES DE TELA:'''
Largura = 640
Altura = 480
Tela = pygame.display.set_mode((Largura, Altura))
pygame.display.set_caption('T-Rex Game')
Diretório_Principal = os.path.dirname(__file__)
Diretório_Imagens = os.path.join(Diretório_Principal, 'Imagens')
Diretório_Sons = os.path.join(Diretório_Principal, 'Sons')
'''CONVERT_ALPHA() SERVE PARA PRESERVAR O FUNDO TRANSPARENTE DA IMAGEM:'''
Sprite_Sheet = pygame.image.load(os.path.join(Diretório_Imagens, 'dinoSpritesheet.png')).convert_alpha()
Escolha_Obstáculo = choice([0, 1])
def Exibe_Mensagem(MSG, Tamanho, Cor):
    Fonte = pygame.font.SysFont('comicsanssms', Tamanho, True, False)
    Mensagem = f'{MSG}'
    Formatação = Fonte.render(Mensagem, True, Cor)
    return Formatação


#ÁUDIO
'''CONFIGURAÇÕES DE SOM:'''
pygame.mixer.init()
Som_Colisão = pygame.mixer.Sound(os.path.join(Diretório_Sons, 'death_sound.wav'))
Som_Colisão.set_volume(1)
Som_Pontuação = pygame.mixer.Sound(os.path.join(Diretório_Sons, 'score_sound.wav'))
Som_Pontuação.set_volume(1)


#JOGO
Fim_de_Jogo = False
Dificuldade = 23
Pontos = 0

'''CONFIGURAÇÕES DA SPRITE TIRANOSSAURO:'''
class Dino(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Som_Pulo = pygame.mixer.Sound(os.path.join(Diretório_Sons, 'jump_sound.wav'))
        self.Som_Pulo.set_volume(1)
        self.Imagens_Tiranossauro = []
        for Contador in range(3):
            IMG = Sprite_Sheet.subsurface((Contador * 32, 0), (32, 32))
            IMG = pygame.transform.scale(IMG, (32*3, 32*3))
            self.Imagens_Tiranossauro.append(IMG)

        self.Index_Lista = 0
        self.image = self.Imagens_Tiranossauro[self.Index_Lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.Y_Tiranossauro = Altura - 64 - 96//2
        self.rect.topleft = (100, self.Y_Tiranossauro)
        self.Pulo = False

    def pular(self):
        self.Pulo = True
        self.Som_Pulo.play()

    def update(self):
        if self.Pulo == True:
            if self.rect.y <= 250:
                self.Pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.Y_Tiranossauro: 
                self.rect.y += 20
            else:
                self.rect.y = self.Y_Tiranossauro

        if self.Index_Lista > 2:
            self.Index_Lista = 0
        self.Index_Lista += 0.25
        self.image = self.Imagens_Tiranossauro[int(self.Index_Lista)]

'''CONFIGURAÇÕES DA SPRITE NUVEM:'''
class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        '''O NÚMERO "7" SE REFERE A POSIÇÃO DA IMAGEM E "32" SE AO NÚMERO DE PIXELS:'''
        self.image = Sprite_Sheet.subsurface((7*32, 0), (32, 32))
        '''TRANSFORMANDO O TAMANHO DAS NUVENS. NESTE CASO, A IMAGEM PASSARÁ DE 32 PARA 96 PIXELS:'''
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        '''COLOCANDO AS IMAGENS DENTRO DE UM RETÂNGULO PARA SE ALINHAR A TELA:'''
        self.rect = self.image.get_rect()
        '''DEFININDO A POSIÇÃO "Y" E "X" DAS NUVENS:'''
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = Largura - randrange(30, 300, 90)
    '''DEFININDO COMO AS NUVENS DEVERÃO REAPARECER NA TELA:'''
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = Largura
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= Dificuldade

'''CONFIGURAÇÕES DA SPRITE CHÃO:'''
class Superfície(pygame.sprite.Sprite):
    def __init__(self, X_Chão):
        pygame.sprite.Sprite.__init__(self)
        self.image = Sprite_Sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        '''DEFININDO A POSIÇÃO DO CHÃO:'''
        self.rect.y = Altura - 64
        self.rect.x = X_Chão * 64
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = Largura
        '''ENQUANTO A POSIÇÃO DO CHÃO NÃO FOR MENOR QUE 0, O CHÃO IRÁ SE MOVIMANTER 10 PIXELS PARA A ESQUERDA:'''
        self.rect.x -= 10   

'''CONFIGURAÇÕES DA SPRITE CACTO:'''
class Planta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Sprite_Sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.Escolha = Escolha_Obstáculo
        '''DEFININDO A POSIÇÃO DO CACTO:'''
        self.rect.center = (Largura, Altura - 64)
        self.rect.x = Largura
    '''SE O NÚMERO SORTEADO NA LISTA "ESCOLHA_OBSTÁCULO" FOR IGUAL A ZERO, O CACTO IRÁ APARECER NA TELA:'''
    def update(self):
        if self.Escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = Largura 
            self.rect.x -= Dificuldade

'''PTEROSSAURO:'''
class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Imagens_Pterossauro = []
        for Contador in range(3,5):
            Img = Sprite_Sheet.subsurface((Contador * 32, 0), (32, 32))
            self.Escolha = Escolha_Obstáculo
            Img = pygame.transform.scale(Img, (32*3, 32*3))
            self.Imagens_Pterossauro.append(Img) 
        self.Index_Lista = 0
        self.image = self.Imagens_Pterossauro[self.Index_Lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (Largura, 300)
        self.rect.x = Largura
    '''SE O NÚMERO SORTEADO NA LISTA "ESCOLHA_OBSTÁCULO" FOR IGUAL A UM, O PTEROSSAURO IRÁ APARECER NA TELA:'''
    def update(self):
        if self.Escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = Largura
            self.rect.x -= Dificuldade
            if self.Index_Lista > 1:
                self.Index_Lista = 0
            self.Index_Lista += 0.25
            self.image = self.Imagens_Pterossauro[int(self.Index_Lista)]

Imagens = pygame.sprite.Group()
Tiranossauro = Dino()
Imagens.add(Tiranossauro)

for Contador in range(4):
    Nuvem = Nuvens()
    Imagens.add(Nuvem)

'''PARA PREENCHER COMPLETAMENTE O CHÃO NA TELA SERÁ NECESSÁRIO REALIZAR O CÁLCULO 640 (LARGURA) * 2 / 64 (PIXELS), 
O RESULTADO SERÁ 20. COM ISSO, IREMOS CRIAR UM LAÇO DE REPETIÇÃO COM ESSE RESULTADO PARA QUE O CHÃO SEJA FEITO.'''
for Contador in range(Largura*2 // 64):
    Chão = Superfície(Contador)
    Imagens.add(Chão)

Cacto = Planta()
Imagens.add(Cacto)

Pterossauro = DinoVoador()
Imagens.add(Pterossauro)

Obstáculos = pygame.sprite.Group()
Obstáculos.add(Cacto)
Obstáculos.add(Pterossauro)

while True: 
    '''DEFININDO VELOCIDADE DO JOGO:'''
    Velocidade_do_Jogo = pygame.time.Clock()
    Velocidade_do_Jogo.tick(Dificuldade)

    '''DEFININDO COR DE FUNDO:'''
    Tela.fill((255, 255, 255))
    Imagens.draw(Tela)

    '''DEFININDO QUAIS OBJETOS PODEM COLIDIR COM O DINOSSAURO. 
    OBSERVAÇÃO: "FALSE" FAZ COM QUE APÓS A COLISÃO O OBJETO NÃO DESAPAREÇA DA TELA.'''
    Colisões = pygame.sprite.spritecollide(Tiranossauro, Obstáculos, False, pygame.sprite.collide_mask)
    
    '''SE O CANTOR DIREITO FOR MENOR OU IGUAL A ZERO SERÁ REALIZADO UM NOVO SORTEIO DE OBSTÁCULOS:'''
    if Cacto.rect.topright[0] <= 0 or Pterossauro.rect.topright[0] <= 0:
        Escolha_Obstáculo = choice([0, 1])  
        '''REPOSICIONANDO OBSTÁCULOS NA TELA:'''
        Cacto.rect.x = Largura
        Pterossauro.rect.x = Largura
        Cacto.Escolha = Escolha_Obstáculo
        Pterossauro.Escolha = Escolha_Obstáculo

    if Colisões and Fim_de_Jogo == False:
        '''SE HOUVER COLISÃO, O JOGO IRÁ PARAR:'''
        Som_Colisão.play()
        Fim_de_Jogo = True
    
    if Fim_de_Jogo == True:
        '''SE HOUVER COLISÃO, SERÁ EXIBIDO UMA MENSAGEM DE FIM DE JOGO:'''
        Game_Over = Exibe_Mensagem('FIM DE JOGO', 40, (0, 0 ,0))
        Tela.blit(Game_Over, (Largura//2, Altura//2))
        Restart = Exibe_Mensagem('Pressione [R] para recomeçar', 20, (0, 0, 0))
        Tela.blit(Restart, (Largura//2, (Altura//2) + 40))

    else:
        '''SE NÃO HOUVER COLISÃO, CONTINUARÁ CONTANDO PONTUÇÃO:'''
        Pontos += 1
        Imagens.update()
        Texto_Pontos = Exibe_Mensagem(Pontos, 40, (0, 0, 0))
    
    '''SEMPRE QUE ATINGIR 100 PONTOS, UM SOM IRÁ TOCAR:'''
    if Pontos % 100 == 0:
        Dificuldade = Dificuldade + 1
        Som_Pontuação.play()
    Tela.blit(Texto_Pontos, (520, 30))
    pygame.display.flip()

    '''DEFININDO COMO O JOGO DEVERÁ RECOMEÇAR:'''
    def Reiniciar():
        global Pontos, Dificuldade, Fim_de_Jogo, Escolha_Obstáculo 
        Fim_de_Jogo = False
        Pontos = 0
        Dificuldade = 23
        Tiranossauro.rect.y = Altura - 64 - 96//2
        Tiranossauro.Pulo = False
        Pterossauro.rect.x = Largura
        Cacto.rect.x = Largura
        Escolha_Obstáculo = choice([0, 1]) 


    #CONTROLES
    '''CONFIGURAÇÕES DE CONTROLE DO JOGO:'''
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and Fim_de_Jogo == False:
                if Tiranossauro.rect.y != Tiranossauro.Y_Tiranossauro:
                    pass
                else:
                    Tiranossauro.pular()

            if event.key == K_r and Fim_de_Jogo == True: 
                Reiniciar()