#!/usr/bin/env python
# -*- codinng:utf-8 -*-
import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_event(ai_settings, screen, ship, bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
	screen.fill(ai_settings.bg_color)  # 每次循环重新绘制屏幕

	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	pygame.display.flip()  # 使最近绘制的屏幕可见

def update_bullets(bullets):
	# 更新子弹的位置
	bullets.update()
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)


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
	ai_settings.fleet_direction = ~ai_settings.fleet_direction


def update_aliens(ai_settings, aliens):
	# 检查是否有外星人位于屏幕边缘，并更新所有外星人的位置
	check_fleet_edges(ai_settings, aliens)
	aliens.update()