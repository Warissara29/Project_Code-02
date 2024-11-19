import pygame as pg
from random import randint  # เพิ่มการสุ่มความสูง

class OB:
    def __init__(self, scale_factor, move_speed, pipe_spacing):
        # โหลดภาพเสาด้านล่างและปรับขนาดตามขนาดที่ต้องการ (width, height)
        self.img_down = pg.transform.scale_by(pg.image.load("รูปภาพและไฟล์ประกอบ/เสา.png").convert_alpha(), scale_factor)
        # ระยะห่างระหว่างเสาด้านล่างแต่ละอัน

        self.pipe_spacing = pipe_spacing

        # กำหนด rect ของเสาด้านล่าง
        self.rect_down = self.img_down.get_rect()
        
        # กำหนดตำแหน่ง y ของเสาด้านล่างให้อยู่ในช่วงที่กำหนด
        self.rect_down.y = randint(295, 430)  # ตำแหน่ง y ของเสาด้านล่างในช่วง 285 ถึง 460
        # ตำแหน่ง x ของเสาด้านล่างเริ่มต้น
        self.rect_down.x = pipe_spacing  
        
        self.move_speed = move_speed

    def draw_pipe(self, win):
        win.blit(self.img_down, self.rect_down)  # วาดเสาลงบนหน้าจอ

    def update(self, dt):
        # Update the position of the bottom pipe
        self.rect_down.x -= int(self.move_speed * dt)