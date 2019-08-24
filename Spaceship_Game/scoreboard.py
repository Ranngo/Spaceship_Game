#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import pygame.font
from ship import Ship
from pygame.sprite import Group

class Scoreboard:
	# 显示得分信息
	def __init__(self, ai_settings, screen, stats):
		''' 初始化得分相关属性 '''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		# 显示得分信息时使用的字体设置
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		# 准备初始得分图像
		self.prep_score()
		self.prep_highest_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

		# 确定位置
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_highest_score(self):
		highest_score = int(round(self.stats.highest_score, -1))
		highest_score_str = "{:}".format(highest_score)
		self.highest_score_image = self.font.render(highest_score_str, True, self.text_color, self.ai_settings.bg_color)

		# 确定位置
		self.highest_score_rect = self.highest_score_image.get_rect()
		self.highest_score_rect.centerx = self.screen_rect.centerx
		self.highest_score_rect.top = self.score_rect.top

	def prep_level(self):
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

		# 确定位置
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		# 显示还剩多少艘飞船
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		# 显示得分
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.highest_score_image, self.highest_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)