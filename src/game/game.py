import sys, os
import time
import pygame
from pygame.locals import *
from game.player_class import Player
from game.second_player_class import SecondPlayer
from graphic.affichage import *
from graphic.menu import Menu
from supervision.supervisor import Supervisor

def chemin_fichier(relatif):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relatif)
    return os.path.join(os.path.abspath("."), relatif)

class Game:
    def __init__(self, reso):
        self.reso = reso
        
        #Bordures de l'ecran
        self.bord = [ [-50, self.reso[0] + 50], 
                    [-50, self.reso[1] + 50] ]
        #Bordures de vaisseau
        self.ship_bord = [ [40, self.reso[0] - 50], 
                        [40, self.reso[1] - 50] ]
        
        self.titre = "Space Scoring : Battle"
        self.is_running = True
        self.is_playing = False
        self.j1_score = 0
        self.j2_score = 0
        self.score_font_size = 13
        self.txt_font_size = 11
        self.title_font_size = 26
        self.score_pos_j1 = (self.reso[0] - self.reso[0] + 100, 30)
        self.win_pos = (self.reso[0]/2, self.reso[1]/2)
        self.vies_pos_j1 = (self.reso[0] - self.reso[0] + 300, 30)
        self.score_pos_j2 = (self.reso[0] - 100, 30)
        self.vies_pos_j2 = (self.reso[0] - 300, 30) 
        self.clock = pygame.time.Clock()
        self.superviseur = Supervisor()
        self.fin_partie_timer = 3
       
        self.first_player = pygame.image.load(chemin_fichier("assets/first_ship.png"))
        self.second_player = pygame.image.load(chemin_fichier("assets/second_ship.png"))
        self.img_bullet = pygame.image.load(chemin_fichier("assets/bullet.png"))
        self.ico = pygame.image.load(chemin_fichier("assets/icon.png"))

        self.p1 = Player((200, 200), 5, self.first_player, self.img_bullet)
        self.p2 = SecondPlayer((700, 200), 5, self.second_player, self.img_bullet)
        self.all_bullets = pygame.sprite.Group()
        self.all_bullets_p2 = pygame.sprite.Group()

        self.fin_partie_start = 0
        self.start()

    #Initialisation de la fenetre et de son titre
    def start(self):
        pygame.init()
        
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode(self.reso, flags)
        pygame.display.set_caption(self.titre)
        pygame.display.set_icon(self.ico)

        while self.is_running:
            text_screen("SPACE SCORING : BATTLE ", self.title_font_size, pygame.Color(10,255,0), self.screen, (self.reso[0]/2, self.reso[1]/2 - 70))
            text_screen(" J1 : Z avancer, D pivoter droite, Q pivoter gauche, S reculer, Alt tirer ", self.txt_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 - 20, self.reso[1]/2 + 70))
            text_screen(" J2 : O avancer, M pivoter droite, J pivoter gauche, L reculer, AltGr tirer ", self.txt_font_size, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 - 20, self.reso[1]/2 + 150))
            text_screen("Appuyez sur Espace pour lancer la partie !", self.txt_font_size + 3, pygame.Color(255,255,255), self.screen, self.win_pos)
            
            pygame.display.update()
            self.screen.fill('blue')            
            for evt in pygame.event.get():
                self.get_events(evt)
                self.run()
            
    def run(self):
        while self.is_playing:
            screen_width, screen_height = self.screen.get_size()

            # Bordures

            ship_bord_x = [40, screen_width - 50]
            ship_bord_y = [40, screen_height - 50]

            for evt in pygame.event.get():
                self.get_events(evt)
                 
              # limites bord angle x joueur 1
            if self.p1.pos[0] < ship_bord_x[0]:
                self.p1.pos = (ship_bord_x[0], self.p1.pos[1])
            elif self.p1.pos[0] > ship_bord_x[1]:
                self.p1.pos = (ship_bord_x[1], self.p1.pos[1])
            
           # limites bord angle y joueur 1
            if self.p1.pos[1] < ship_bord_y[0] + 60:
                self.p1.pos = (self.p1.pos[0], ship_bord_y[0] + 59)
            elif self.p1.pos[1] > ship_bord_y[1]:
                self.p1.pos = (self.p1.pos[0], ship_bord_y[1])

             # limites bord angle x joueur 2
            if self.p2.pos[0] < ship_bord_x[0]:
                self.p2.pos = (ship_bord_x[0], self.p2.pos[1])
            elif self.p2.pos[0] > ship_bord_x[1]:
                self.p2.pos = (ship_bord_x[1], self.p2.pos[1])
            
            # limites bord angle y joueur 2
            if self.p2.pos[1] < ship_bord_y[0] + 60:
                self.p2.pos = (self.p2.pos[0], ship_bord_y[0] + 59)
            elif self.p2.pos[1] > ship_bord_y[1]:
                self.p2.pos = (self.p2.pos[0], ship_bord_y[1])

            self.p1.get_inputs()
            self.p2.get_inputs()
            self.update()
            
    
    #Fonction permettant de gerer les events
    def get_events(self, evt):
        if evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE):
            self.is_running, self.is_playing = False, False
        if evt.type == KEYDOWN:
            if evt.key == K_LALT and self.is_playing == True:
                bullet = self.p1.tirer()
                if bullet:
                    self.all_bullets.add(bullet)
            elif evt.key == K_RALT and self.is_playing == True:
                bullet = self.p2.tirer()
                if bullet:
                    self.all_bullets_p2.add(bullet)
            elif evt.key == K_SPACE:
                self.is_playing = True

    #Dessin des surfaces etc (affichage)
    def draw(self):
        self.screen.blit(self.p1.image, self.p1.rect)
        self.screen.blit(self.p2.image, self.p2.rect)
        self.all_bullets.draw(self.screen)
        self.all_bullets_p2.draw(self.screen)

    #Affichage du score
    def draw_score(self):
        text_screen("J1 Score : " + str(self.j1_score), self.score_font_size, pygame.Color(255,255,0), self.screen, self.score_pos_j1)
        text_screen("J2 Score : " + str(self.j2_score), self.score_font_size, pygame.Color(255,255,0), self.screen, self.score_pos_j2)
    
    def draw_vies(self):
        text_screen("J1 Vies : " + str(self.p1.vies), self.score_font_size, pygame.Color(255,255,0), self.screen, self.vies_pos_j1)
        text_screen("J2 Vies : " + str(self.p2.vies), self.score_font_size, pygame.Color(255,255,0), self.screen, self.vies_pos_j2)
    
    def draw_victoire_j2(self):
        self.fin_partie_start = time.time()
        restart = False
        
        
        while not restart:
            for evt in pygame.event.get():
                if evt.type == QUIT or evt.type == KEYDOWN and evt.key == K_ESCAPE:
                    sys.exit()
                elif evt.type == KEYDOWN and evt.key == K_SPACE:
                    restart = True
                
            self.screen.fill(pygame.Color(155,0,0))
            text_screen("Joueur 2 Gagne !", self.txt_font_size + 15, pygame.Color(255,255,0), self.screen, self.win_pos)
            text_screen("Avec un score de : " + str(self.j2_score), self.txt_font_size + 5, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 - 10, self.reso[1] /2 + 40))
            text_screen("Appuyez sur ESPACE pour reprendre et augmenter votre score", self.txt_font_size + 3, pygame.Color(255,0,255), self.screen, (self.reso[0] /2, self.reso[1]/2 + 90))
            text_screen("!ATTENTION! vous perdrez votre score si vous perdez", self.txt_font_size + 5, pygame.Color(255,255,255), self.screen, (self.reso[0] /2, self.reso[1]/2 + 125))

            pygame.display.update()
            self.p1.vies = 5
            self.p2.vies = 5
            self.j2_score = self.j2_score
            self.j1_score = 0
            self.superviseur.reset_alertes()
           

    def draw_victoire_j1(self):
        self.fin_partie_start = time.time()
        restart = False
        while not restart:

            for evt in pygame.event.get():
                if evt.type == QUIT:
                    sys.exit()
                elif evt.type == KEYDOWN and evt.key == K_SPACE:
                    restart = True

            self.screen.fill(pygame.Color(155,0,0))
            text_screen("Joueur 1 Gagne !", self.txt_font_size + 15, pygame.Color(255,255,0), self.screen, self.win_pos)
            text_screen("Avec un score de : " + str(self.j1_score), self.txt_font_size + 5, pygame.Color(255,255,0), self.screen, (self.reso[0]/2 + - 10, self.reso[1] /2 + 40))
            text_screen("Appuyez sur ESPACE pour reprendre et augmenter votre score", self.txt_font_size + 3, pygame.Color(255,0,255), self.screen, (self.reso[0] /2, self.reso[1]/2 + 90))
            text_screen("!ATTENTION! vous perdrez votre score si vous perdez", self.txt_font_size + 5, pygame.Color(255,255,255), self.screen, (self.reso[0] /2, self.reso[1]/2 + 125))

            pygame.display.update()
            self.p2.vies = 5
            self.p1.vies = 5
            self.j2_score = 0
            self.superviseur.reset_alertes()
           

    #Gestion des collisions
    def gerer_collision(self):

        #Joueur 1
        for bullet in pygame.sprite.spritecollide(self.p1, self.all_bullets_p2, False):
            print("Joueur 1 touche")
            bullet.kill()
            del bullet
            self.p1.vies -= 1
            self.j2_score += 5
            while self.p1.vies < 0:
                self.p1.vies = 0
                self.draw_victoire_j2()
            print("J1 perd une vie") 
            

        
        #Joueur 2
        for bullet in pygame.sprite.spritecollide(self.p2, self.all_bullets, False):
            print("Joueur 2 touche")
            bullet.kill()
            del bullet
            self.p2.vies -= 1
            self.j1_score += 5
            while self.p2.vies < 0:
                self.p2.vies = 0
                self.draw_victoire_j1()
            print('J2 perd une vie')
            


    #Suppression des projectiles
    def clear_bullets(self, group):

        for bullet in group.sprites():
            if bullet.rect.centerx < self.bord[0][0] or bullet.rect.centerx > self.bord[0][1]:
                self.all_bullets.remove(bullet)
            if bullet.rect.centery < self.bord[1][0] or bullet.rect.centery > self.bord[1][1]:
                self.all_bullets.remove(bullet) 
            if bullet not in self.all_bullets.sprites():
                del bullet

    #Update des methodes en les appelant
    def update(self):
        self.screen.fill(178)
        self.clear_bullets(self.all_bullets)
        self.clear_bullets(self.all_bullets_p2)
        self.p1.update()
        self.all_bullets.update()
        self.all_bullets_p2.update()
        self.p2.update()
        self.draw()
        self.draw_score() 
        self.draw_vies()
        self.gerer_collision()
        self.superviseur.check_vie(self.p1, "J1")
        self.superviseur.check_vie(self.p2, "J2")
        self.superviseur.draw_alertes(self.screen, self.reso, text_screen)
        self.clock.tick(60)
        pygame.display.flip()
    
    #Mise en arret du programme
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self