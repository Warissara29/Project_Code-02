import pygame as pg
from random import randint  # เพิ่มการสุ่มความสูง

class Item:
    def __init__(self, scale_factor, move_speed, pipe_spacing):
        # โหลดภาพเหรียญและปรับขนาดตามขนาดที่ต้องการ (width, height)
        self.img_item = pg.transform.scale_by(pg.image.load("รูปภาพและไฟล์ประกอบ/ไอเท็ม.png").convert_alpha(), scale_factor)
        
        self.pipe_spacing = pipe_spacing  # ระยะห่างระหว่างเหรียญ

        # กำหนด rect ของเหรียญ
        self.rect = self.img_item.get_rect()
        
        # กำหนดตำแหน่ง y ของเหรียญให้อยู่ในช่วงที่กำหนด
        self.rect.y = randint(285, 360)  # ตำแหน่ง y ของเหรียญในช่วง 285 ถึง 360
        
        # ตำแหน่ง x ของเหรียญเริ่มต้น
        self.rect.x = pipe_spacing  
        
        self.move_speed = move_speed  # ความเร็วในการเคลื่อนที่ของเหรียญ

    def draw_item(self, win):
        # วาดเหรียญลงบนหน้าจอ
        win.blit(self.img_item, self.rect)

    def update(self, dt):
        # อัปเดตตำแหน่งของเหรียญ (เลื่อนไปทางซ้าย)
        self.rect.x -= int(self.move_speed * dt)
