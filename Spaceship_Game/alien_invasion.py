#!/usr/bin/env python
# -*- codinng:utf-8 -*-

import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
	pygame.init()

	ai_settings = Settings()		# 引入默认设置

	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')

	# 创建一艘飞船
	ship = Ship(ai_settings, screen)
	# 创建一个用于存储子弹的编组
	bullets = Group()
	aliens = Group()

	# 创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)

	while True:
		gf.check_event(ai_settings, screen, ship, bullets)
		ship.update()
		gf.update_bullets(bullets)
		gf.update_aliens(ai_settings, aliens)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()