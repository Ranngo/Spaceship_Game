#!/usr/bin/env python
# -*- codinng:utf-8 -*-


class GameStats:
	# 跟踪游戏的统计信息
	def __init__(self, ai_settings):
		# 初始化统计信息
		self.ai_settings = ai_settings
		self.game_active = False
		self.reset_stats()
		# 在任何情况下都不能重置最高得分
		self.highest_score = 0

	def reset_stats(self):
		# 初始化游戏运行期间可能发生变化的统计信息
		self.level = 1
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0