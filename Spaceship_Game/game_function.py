#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep



def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:			# 右移
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:		# 左移
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:		# 射击
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:			# 退出
		sys.exit()


def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_event(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y):
	# 单击Play按钮开始游戏
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# 重置游戏动态设置
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏的统计信息
		stats.reset_stats()
		stats.game_active = True

		# 重置游戏记分牌信息
		sb.prep_score()
		sb.prep_highest_score()
		sb.prep_level()
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人,并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	# 每次循环重新绘制屏幕
	screen.fill(ai_settings.bg_color)

	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# 显示得分
	sb.show_score()

	# 如果游戏处于非活动状态， 绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()

	pygame.display.flip()  # 使最近绘制的屏幕可见


def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
	# 更新子弹的位置
	bullets.update()
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens)


def check_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens):
	# 检查是否有子弹击中外星人，如有，子弹和外星人删除
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	# 检查外星人数量，为0则再次生成外星人群
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)
		# 提高等级
		stats.level += 1
		sb.prep_level()


def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一颗子弹，并将其加入编组中
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
	# 计算每行可以容纳多少个外星人
	available_space_x = ai_settings.screen_width - (2 * alien_width)
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height ):
	# 计算纵向一共能容纳多少行的外星人
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	# 创建一个外星人并将其放在当前行
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	# 定位外星人的位置
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
	# 创建一群外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	# 从行开始，逐行添加外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# 创建一个外星人，并将其加入当前行
			create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
	# 有外星人到达边缘时执行换行
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	# 将所有外星人下移一行，并改变移动方向
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction = ai_settings.fleet_direction * (-1)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# 记录剩余飞船数量
	if stats.ships_left > 0:
		stats.ships_left -= 1

		# 更新记分牌
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一批新的外星人，并将飞船放到屏幕底端中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# 检查是否有外星人到达屏幕底端
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样进行处理
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			sb.prep_ships()
			break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# 检查是否有外星人位于屏幕边缘，并更新所有外星人的位置
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# 检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

	# 检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
	# 检查是否诞生了新的最高分
	if stats.score > stats.highest_score:
		stats.highest_score = stats.score
		sb.prep_highest_score()
