import pygame, sys, random

from pygame.constants import K_SPACE

#funcao para criar canos
def criar_cano():
    cano_pos_aleatoria = random.choice(altura_canos)
    cano_alto = cano_superficie.get_rect(midbottom = (700,cano_pos_aleatoria - 400))# gera o cano de cima com um espaco entre ele e o de baixo
    cano_baixo = cano_superficie.get_rect(midtop = (700,cano_pos_aleatoria)) #gera o cano de baixo na esquerda(fora da tela)
    return cano_alto, cano_baixo

#funcao para desenhar o chao
def desenhar_chao():
    tela.blit(superficie_chao,(chao_pos_x,900))
    tela.blit(superficie_chao,(chao_pos_x + 576,900)) #segundo chao que vai ser desenhado para parecer que é um chao continuo andando

#funcao para desenhar canos
def desenhar_canos(canos):
    for cano in canos:
        if cano.bottom >= 1024: # se o cano está em baixo da tela (cano de baixo)
            tela.blit(cano_superficie, cano)
        else:
            cano_invertido = pygame.transform.flip(cano_superficie, False, True) # se é o cano de cima nós inveretemos ele para ficar certo
            tela.blit(cano_invertido, cano)

#funcao para mover os canos
def mover_canos(canos):
    for cano in canos:
        cano.centerx -= 5 # move os canos para esquerda
    return canos

#funcao para checar se houve uma colisao
def checar_colisao(canos):
    for cano in canos:
        if java_rect.colliderect(cano):
            som_erro.play()
            som_derrota.play()
            return False # retorna Falso para parar o jogo caso haja colisao
    if java_rect.top <= -100 or java_rect.bottom >= 900: # se o java foi mais para cima que o limite ou encostou no teto
        return False # retorna Falso para parar o jogo caso haja colisao

    return True # return true para o game continuar caso nao haja colisao

#funcao para placar de pontos
def placar_pontos(estado_jogo):
    if estado_jogo == 'jogo_principal': # se estivermos no jogo principal
        placar = fontePlacar.render(f"Pontos: {int(pontuacao)}", False, (255,255,255))
        placar_rect = placar.get_rect(center = (110, 50)) # cria um quadrado em volta do placar no canto da tela
        tela.blit(placar, placar_rect)
    if estado_jogo == 'game_over': # se estivermos na tela de game over, ele vai printar a pontuacao atual e o recorde na tela
        placar = fontePlacar.render(f"Pontos na Rodada :  {int(pontuacao)}", False, (255,255,255))
        placar_rect = placar.get_rect(center = (288, 800)) # cria um quadrado em volta do placar no canto da tela
        tela.blit(placar, placar_rect)

        placar_recorde = fontePlacar.render(f"Recorde: {int(recorde)}", False, (255,255,255))
        placar_recorde_rect = placar_recorde.get_rect(center = (288, 850)) # cria um quadrado em volta do placar no canto da tela
        tela.blit(placar_recorde, placar_recorde_rect)

#funcao para atualizar o placar de pontuacao do jogador
def atualizar_pontuacao(pontuacao, recorde):
    if pontuacao > recorde:
        recorde = pontuacao
    return recorde

pygame.init()
fontePlacar = pygame.font.Font('PressStart2P.ttf', 20)
tela = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

#variaveis
gravidade = 0.25
movimento = 0
pontuacao = 0
recorde = 0

telasobrefundo = pygame.image.load('telasobre.jpg').convert()

telacontrolesfundo = pygame.image.load('telacontroles.jpg').convert()

jogo_ativo = False # variavel que nos diz se o jogo esta ativo ou na tela inicial
tela_sobre = False # variavel que nos diz se o usuario foi para a tela de sobre
tela_controles = False # variavel que nos diz se o usuario foi para a tela de controles

tela_inicial = pygame.image.load('telainicial.jpg').convert()
tela_inicial_rect = tela_inicial.get_rect(center=(288,512))

planodefundo = pygame.image.load('fundojogo.jpeg').convert()

superficie_chao = pygame.image.load('chaoerror.png').convert_alpha()
chao_pos_x = 0 # posicao x do chao, usado pra fazer o chao mover

java = pygame.image.load('personagem.png')
java_rect = java.get_rect(center = (100, 512)) # cria um retangulo ao redor do java

cano_superficie = pygame.image.load('canoerro.png')
cano_superficie = pygame.transform.scale2x(cano_superficie)
lista_canos = [] # lista que armazenara os canos
GERARCANO = pygame.USEREVENT # evento para gerar cano
pygame.time.set_timer(GERARCANO, 1200) # gera um cano a cada 1200 ms, 1.2 segundos
altura_canos = [450, 500, 550, 600, 650, 700, 750, 800, 850] # vetor que armazena uma lista de possiveis alturas para o cano

MARCARPONTO = pygame.USEREVENT + 1 # evento para marcar um ponto a cada vez que um cano é gerado
pygame.time.set_timer(MARCARPONTO, 1200)

pygame.mixer.music.set_volume(0.2)
musica_de_fundo = pygame.mixer.music.load('musicadefundo.mp3')
som_derrota = pygame.mixer.Sound('somderrota.mp3')
som_ponto = pygame.mixer.Sound('somponto.mp3')
som_ponto.set_volume(0.2)
som_pulo = pygame.mixer.Sound('sompulo.mpeg')
som_pulo.set_volume(0.2)
som_batida = pygame.mixer.Sound('sombatida.mpeg')
som_batida.set_volume(0.05)
som_erro = pygame.mixer.Sound('somerro.mpeg')
som_erro.set_volume(0.6)
som_ponto_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # evento para checar se uma tecla foi acionada
            if event.key == pygame.K_SPACE and jogo_ativo: # evento que apenas acontece se o jogo estiver ativo
                movimento = 0
                movimento -= 12 # faz o passaro pular no espaco
                som_pulo.play()
                som_derrota.stop()

            if event.key == pygame.K_SPACE and jogo_ativo == False: # evento que apenas acontece se apertarmos espaço após o jogo ter terminado
                jogo_ativo = True
                lista_canos.clear() # limpa a lista de canos para nao causar bugs
                java_rect.center = (100, 512) # coloca o java na posicao inicial após a derrota
                movimento = 0 # resetamos o movimento do java após a derrota
                pontuacao = 0 # resetamos a pontuacao após a derrota

            if event.key == pygame.K_x and jogo_ativo == False: # evento que acontece se apertarmos X na tela inicial e nos leva para a tela de sobre
                tela_sobre = True

            if event.key == pygame.K_z and jogo_ativo == False:
                tela_controles = True

            if event.key == pygame.K_ESCAPE and tela_sobre == True: # evento que acontece se apertarmos ESC na tela de sobre e nos faz voltar para a tela inicial
                tela_sobre = False
            
            if event.key == pygame.K_ESCAPE and tela_controles == True: # evento que acontece se apertarmos ESC na tela de controle e nos faz voltar para a tela inicial
                tela_controles = False

        if event.type == GERARCANO:
            lista_canos.extend(criar_cano())

        if event.type == MARCARPONTO and jogo_ativo == True:
            som_ponto.play()
            pontuacao += 1

    tela.blit(planodefundo, (0,0))

    if jogo_ativo:  # se o jogo estiver ativo o movimento e os canos funcionam
        movimento += gravidade
        java_rect.centery += movimento
        tela.blit(java, java_rect)
        jogo_ativo = checar_colisao(lista_canos)

        lista_canos = mover_canos(lista_canos)
        desenhar_canos(lista_canos)

        placar_pontos('jogo_principal') # se estivermos no jogo o placar de pontos é do jogo principal
    else: # else: caso o jogo nao esteja ativo, significa que o jogador perdeu e iremos exibir o placar de game over
        pygame.mixer.music.play(-1)
        tela.blit(tela_inicial, tela_inicial_rect)
        recorde = atualizar_pontuacao(pontuacao, recorde) # atualiza o recorde para ser a sua maior pontuacao
        placar_pontos('game_over')

    if tela_sobre: # se a tela de sobre for ativada desenha ela na tela
        pygame.mixer.music.play(-1)
        tela.blit(telasobrefundo, (0,0))
    
    if tela_controles: # se a tela de controles for ativada desenha ela na tela
        pygame.mixer.music.play(-1)
        tela.blit(telacontrolesfundo, (0,0))

    chao_pos_x -= 1 # faz o chao andar para a esquerda
    desenhar_chao()
    if chao_pos_x <= -576: # if para fazer o loop do chao e ir criando chaos novos para ser um loop infinito
        chao_pos_x = 0

    pygame.display.update()
    clock.tick(120) # trava o jogo em 120 FPS
