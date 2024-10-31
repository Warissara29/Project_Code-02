import pygame as pg

# ไอเท็มคลาส
class Item:
    def __init__(self, x, y):
        self.image = pg.transform.scale(pg.image.load("game-Project/ไอเท็ม.png").convert_alpha(), (80, 80))  # โหลดและปรับขนาดไอเท็ม
        self.rect = self.image.get_rect(topleft=(x, y))  # ตั้งค่า rect ตามตำแหน่ง X และ Y

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)  # ใช้ rect.topleft เป็นตำแหน่งในการวาด