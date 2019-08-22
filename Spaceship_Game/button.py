#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import pygame.font

class Button():
	def __init__(self, screen):
		# 初始化按钮的属性
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# 设置按钮的尺寸和其他属性
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
