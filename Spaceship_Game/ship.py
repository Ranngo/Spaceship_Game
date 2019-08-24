#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		self.image =  pygame.image.load('images/spaceship.bmp')
		self.rect = self.image.get_rect()			# 飞船尺寸
		self.screen_rect = screen.get_rect()		# 屏幕尺寸

		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom		# 定位飞船位置

		self.center = float(self.rect.centerx)

		# 移动标志
		self.moving_right = False
		self.moving_left = False

	def update(self):
		# 飞船移动
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.center -= self.ai_settings.ship_speed_factor

		# 更新rect.centerx
		self.rect.centerx = self.center

	# 绘制飞船到指定位置
	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		# 让飞船居于屏幕底端中部
		self.center = self.screen_rect.centerx