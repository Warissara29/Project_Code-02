import pygame as pg
import sys
from game import Game  # นำเข้าคลาส Game
from choose_character import ChooseCharacter  # นำเข้าคลาส ChooseCharacter

pg.init()

class HowToPlay:
    def __init__(self):
        # ตั้งค่าหน้าจอ
        self.width = 1200
        self.height = 555

        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")  # ชื่อหน้าต่างเกม

        self.ground_img = pg.transform.scale(pg.image.load("รูปภาพและไฟล์ประกอบ/วิธีการเล่น.png").convert(), (self.width, self.height))
        self.buttom_back = pg.image.load("homepage/กลับ.png")
        self.buttom_back = pg.transform.scale(self.buttom_back, (100, 50))

        # กำหนดตำแหน่งและขนาดของปุ่มกลับ
        self.buttom_back_rect = self.buttom_back.get_rect(topleft=(1000, 480))

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
                    
                    if self.buttom_back_rect.collidepoint(x, y):  # เช็คว่าคลิกที่ปุ่มกลับหรือไม่
                        self.go_back_to_choose_character()  # ไปยังหน้าจอ ChooseCharacter

                    if 900 <= x <= 1100 and 250 <= y <= 350:
                        from choose_character import ChooseCharacter  # นำเข้าคลาส ChooseCharacter
                        self.choose_chracter = ChooseCharacter()
                        self.choose_chracter.choose_character()

            self.update_game()  # เรียกฟังก์ชัน update_game()

    def update_game(self):
        # วาดพื้นหลัง
        self.win.blit(self.ground_img, (0, 0))
        self.win.blit(self.buttom_back, (1000, 480))

        # อัปเดตหน้าจอ
        pg.display.update()

    def go_back_to_choose_character(self):
        # ฟังก์ชันสำหรับกลับไปยัง ChooseCharacter
        from choose_character import ChooseCharacter  # นำเข้าคลาส ChooseCharacter
        self.choose_chracter = ChooseCharacter()
        self.choose_chracter.gameLoop()  # เรียกฟังก์ชัน gameLoop ของ ChooseCharacter

    def show(self):
        # เริ่มต้นเกม
        start = HowToPlay()

