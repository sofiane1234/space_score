import unittest
import pygame
from graphic.bullets import Bullet

class TestBullet(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.img = pygame.Surface((10, 10))
        self.bullet = Bullet((100, 100), (0, -1), 5, self.img)

    def test_initial_position(self):
        self.assertEqual(self.bullet.pos, (100, 100))

    def test_update_position(self):
        self.bullet.update()
        self.assertNotEqual(self.bullet.pos, (100, 100))

    def tearDown(self):
        pygame.quit()
