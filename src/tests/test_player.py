import unittest
import pygame
from game.player_class import Player
from graphic.bullets import Bullet

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.img = pygame.Surface((50, 50))
        self.bullet_img = pygame.Surface((10, 10))
        self.player = Player((100, 100), 5, self.img, self.bullet_img)

    def test_initialisation(self):
        self.assertEqual(self.player.pos, (100, 100))
        self.assertEqual(self.player.vies, 5)

    def test_tirer(self):
        bullet = self.player.tirer()
        self.assertIsInstance(bullet, Bullet)
        self.assertEqual(bullet.pos, (100, 100))

    def test_bouger(self):
        original_pos = self.player.pos
        self.player.bouger(1, 1)
        self.assertNotEqual(self.player.pos, original_pos)

    def tearDown(self):
        pygame.quit()
