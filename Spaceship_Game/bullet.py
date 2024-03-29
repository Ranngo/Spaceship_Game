#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	def __init__(self, ai_settings, screen, ship):
		super(Bullet, self).__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		# 用self.y 存储用小数表示的子弹位置
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor


	def update(self):
		self.y -= self.speed_factor
		# 重定位新的子弹位置
		self.rect.y = self.y


	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)