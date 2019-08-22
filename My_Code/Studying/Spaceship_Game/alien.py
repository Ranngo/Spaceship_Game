#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		super(Alien, self).__init__()
		self.ai_settings = ai_settings
		self.screen = screen

		# 加载Alien的图像，并试着其rect属性
		self.image = pygame.image.load('images/alien_ship.bmp')
		self.rect = self.image.get_rect()

		# 设置初始坐标，使每个外星人初始状态都在左上角
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# 存储外星人的准确位置
		self.x = float(self.rect.x)

	def blitme(self):
		# 在指定位置绘制外星人
		self.screen.blit(self.image, self.rect)

	def check_edge(self):
		# 如果外星人位于屏幕边缘，则返回True
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= screen_rect.left:
			return True

	def update(self):
		# 向左或者向右移动外星人
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x
