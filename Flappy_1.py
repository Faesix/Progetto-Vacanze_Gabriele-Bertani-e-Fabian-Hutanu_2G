#Importo le Librerie
import pygame
import random

#Inizializzo Pygame
pygame.init()

#Carico le immagini
sfondo = pygame.image.load('sfondo.png')
uccello = pygame.image.load('flappy_iron.png')
base = pygame.image.load('base.png')
gameover = pygame.image.load('gameover.png')
grattacielo_giu = pygame.image.load('grattacielo_giu.png')

#giro l'immagine del grattacielo per avere il tetto arancione
#sempre verso il centro dello schermo
grattacielo_su = pygame.transform.flip(grattacielo_giu, False, True)

#Costanti Globali
#definisco le dimensioni dello schermo di gioco e i FPS (Frame per Second)
SCHERMO = pygame.display.set_mode((300, 459))
FPS = 50
# definisco una variabile per la velocità di avanzamento:
VEL_AVANZ = 4
#definisco il font del punteggio:
FONT = pygame.font.SysFont('Segoe UI', 50, bold=True)
#definisco la classe "grattacieli_classe" che conterrà 3 diversi metodi:
    # __init__(self) per derinire la posizione in x e Y del grattacielo
    # avanza_e_disegna: per creare i diversi grattacieli con un certa velocità e posizione
    # collisione: per definire gli attributi da utilizzare per definire una collisione e la formula che gestisce la collisione stessa
class grattacieli_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint (-300,-30)
    def avanza_e_disegna(self):
        self.x -= VEL_AVANZ
        SCHERMO.blit(grattacielo_giu, (self.x,self.y+420))
        SCHERMO.blit(grattacielo_su, (self.x,self.y-20))
    def collisione(self, uccello, uccellox, uccelloy):
        tolleranza = 5
        uccello_lato_dx = uccellox+uccello.get_width()-tolleranza
        uccello_lato_sx = uccellox+tolleranza
        grattacieli_lato_dx = self.x + grattacielo_giu.get_width()
        grattacieli_lato_sx = self.x
        uccello_lato_su = uccelloy+tolleranza
        uccello_lato_giu = uccelloy+uccello.get_height()-tolleranza
        grattacieli_lato_su = self.y+grattacielo_su.get_height()-20
        grattacieli_lato_giu = self.y+420
        if uccello_lato_dx > grattacieli_lato_sx and uccello_lato_sx < grattacieli_lato_dx:
            if uccello_lato_su < grattacieli_lato_su or uccello_lato_giu > grattacieli_lato_giu:
                hai_perso()
    def fra_i_grattacieli (self, uccello, uccellox):
        tolleranza = 5
        uccello_lato_dx = uccellox+uccello.get_width()-tolleranza
        uccello_lato_sx = uccellox+tolleranza
        grattacieli_lato_dx = self.x + grattacielo_giu.get_width()
        grattacieli_lato_sx = self.x
        if uccello_lato_dx > grattacieli_lato_sx and uccello_lato_sx < grattacieli_lato_dx:
            return True

        
#inserisce sullo schermo lo sfondo, i grattacieli, l'uccellino e la base
def disegna_oggetti():
    SCHERMO.blit(sfondo, (0,0))
    for g in grattacieli:
        g.avanza_e_disegna()
    SCHERMO.blit(uccello, (uccellox,uccelloy))
    SCHERMO.blit(base, (basex,400))
    punti_render = FONT.render(str(punti), 1, (255,255,255))
    SCHERMO.blit(punti_render, (144,0))
    
def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    
def inizializza():
    global uccellox, uccelloy, uccello_vely
    global basex
    global grattacieli
    global punti
    global fra_i_grattacieli
    uccellox, uccelloy = 60, 150
    uccello_vely = 0
    basex = 0
    punti = 0
    grattacieli = []
    grattacieli.append(grattacieli_classe())
    fra_i_grattacieli = False

def hai_perso():
    SCHERMO.blit(gameover, (50,80))
    aggiorna()
    ricomincia = False
    while not ricomincia:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                ricomincia = True
            if event.type == pygame.QUIT:
                pygame.quit()


inizializza()

###Ciclo Principale###
while True:
    #Avanzamento Base
    basex -= VEL_AVANZ
    if basex < -37: basex = 0
    #Gravità
    uccello_vely += 1
    uccelloy += uccello_vely
    #Comandi
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN
             and event.key == pygame.K_UP ):
            uccello_vely = -9
        if event.type == pygame.QUIT:
            pygame.quit()
    #Gestione Grattacieli
    if grattacieli[-1].x < 100: grattacieli.append(grattacieli_classe())
    #Collissione Uccello-Grattacielo
    for g in grattacieli:
        g.collisione(uccello,uccellox,uccelloy)
    if not fra_i_grattacieli:
        for g in grattacieli:
            if g.fra_i_grattacieli(uccello, uccellox):
                fra_i_grattacieli = True
                break
    if fra_i_grattacieli:
        fra_i_grattacieli = False
        for g in grattacieli:
            if g.fra_i_grattacieli(uccello, uccellox):
                fra_i_grattacieli = True
                break
        if not fra_i_grattacieli:
            punti += 1
    #Collisione con Base
    if uccelloy > 380:
        hai_perso()
    #Aggiornamento schermo
    disegna_oggetti()
    aggiorna()
