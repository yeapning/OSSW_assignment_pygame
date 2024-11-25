import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None: #surface에 블록 생성
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        self.alive = False #alive를 False로 바꾼다!

class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface): #surface에 패들 생성
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface): #surface에 공 생성
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list): #공이 블록과 부딪혓을 때의 공의 이벤트 처리
        # ============================================
        # TODO: Implement an event when the ball hits a block
        for block in blocks: #blocks리스트에 있는 블록 중
            if(block.alive and self.rect.colliderect(block.rect)):
                # 어떤 블록이 alive가 true이면서 공이 블록과 겹치면..
                block.collide() # 블록 삭제 (블록의 collide()함수 호출)
                blocks.remove(block) #blocks 리스트에서 부딪힌 블록 삭제
                self.dir = -self.dir #블록에 부딪힌 반대 방향으로 공 반사

    def collide_paddle(self, paddle: Paddle) -> None: #공이 패들과 부딪혔을 때
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self): #공과 벽이 충돌했을 때 공의 이벤트 처리
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        #display_dimension = (600, 800)
        # 좌우 벽 충돌
        if self.rect.left < 0 or self.rect.right > config.display_dimension[0]:
            #게임화면보다 왼쪽,오른쪽이면...
            self.dir = 180 -self.dir
        # 상단 벽 충돌
        elif self.rect.top < 0:
            self.dir = 360-self.dir
    
    def alive(self): #공이 살아 있는지의 여부를 확인하는 함수
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        if self.rect.bottom > config.display_dimension[1]:
            config.life = config.life - 1
            return False