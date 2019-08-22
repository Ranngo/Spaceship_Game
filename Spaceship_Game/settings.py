#!/usr/bin/env python
# -*- codinng:utf-8 -*-


class Settings():
	def __init__(self):
		# 屏幕和飞船属性设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		self.ship_speed_factor = 1.5
		self.ship_limit = 3
		# 子弹属性设置
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullet_allowed = 3
		# 外星人属性设置
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 50
		# fleet_direction为1表示右移，-1表示左移
		self.fleet_direction = 1

