import pygame as pg
import random  # เพิ่มการสุ่มความสูง


class OB:
    def __init__(self, move_speed, start_x, start_y):
        self.img_down = pg.transform.scale_by(pg.image.load("game-Project/เสา.png").convert_alpha(), 0.4)
        self.rect_down = self.img_down.get_rect()

        self.width = 1200
        self.height = 555
        
        self.rect_down.x = start_x  # เริ่มต้นที่ขอบขวาของหน้าจอ
        self.rect_down.y = start_y  # ตั้งให้ใกล้ขอบล่างของหน้าจอ
        
        self.move_speed = move_speed

    def draw_pipe(self, win):
        win.blit(self.img_down, self.rect_down)  # วาดเสาลงบนหน้าจอ
    
    def update(self, dt):
        self.rect_down.x -= int(self.move_speed * dt * 50)  # เคลื่อนที่เสาไปทางซ้าย