import pygame as pg
import sys
from game import Game  # นำเข้าคลาส Game
from choose_character import ChooseCharacter  # นำเข้าคลาส ChooseCharacter

pg.init()

class Homegame:
    def __init__(self):
        # ตั้งค่าหน้าจอ
        self.width = 1200
        self.height = 555

        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")  # ชื่อหน้าต่างเกม

        self.ground_img = pg.transform.scale(pg.image.load("game-Project/หน้าหลักเกม/หน้าหลักเกม.png").convert(), (self.width, self.height))
        self.buttom_start = pg.image.load("game-Project/หน้าหลักเกม/เริ่มเกม.png")
        self.buttom_out = pg.image.load("game-Project/หน้าหลักเกม/ออกเกม.png")

        self.buttom_start = pg.transform.scale(self.buttom_start, (180, 120))
        self.buttom_out = pg.transform.scale(self.buttom_out, (120, 90))

        self.choose_chracter = ChooseCharacter()

        # เริ่ม loop ของเกม
        self.gameLoop()

    def gameLoop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # หากมีการปิดหน้าต่าง
                    pg.quit()  # ปิด Pygame
                    sys.exit()  # ออกจากโปรแกรม

                if event.type == pg.MOUSEBUTTONDOWN:  # เช็คว่ามีการคลิกเมาส์หรือไม่
                    mouse_pos = pg.mouse.get_pos()  # คืนค่าพิกัดของตำแหน่งเมาส์เมื่อคลิก
                    x, y = mouse_pos
                    
                    # print(f"Mouse clicked at {mouse_pos}")  # แสดงพิกัดตำแหน่งเมาส์เมื่อคลิก

                    if 900 <= x <= 1100 and 250 <= y <= 350:
                        # self.start_game.sart_game()
                        self.choose_chracter.choose_character()

                    if 1000 <= x <= 1100 and 300 <= y <= 400:
                        pg.quit()  # ปิด Pygame
                        sys.exit()  # ออกจากโปรแกรม

            self.update_game()  # เรียกฟังก์ชัน update_game()

    def update_game(self):
        # วาดพื้นหลัง
        self.win.blit(self.ground_img, (0, 0))
        self.win.blit(self.buttom_start, (925,235))  # กำหนดตำแหน่งปุ่มบนหน้าจอ
        self.win.blit(self.buttom_out, (955,335))  # กำหนดตำแหน่งปุ่มบนหน้าจอ

        # อัปเดตหน้าจอ
        pg.display.update()

# เริ่มต้นเกม
start = Homegame()
