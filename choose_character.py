import pygame as pg
import sys
from game import Game  # นำเข้าคลาส Game

pg.init()

class ChooseCharacter:
    def __init__(self):
        self.width = 1200
        self.height = 555
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")
        self.ground_img = pg.transform.scale(pg.image.load("game-Project/หน้าหลักเกม/เลือกตัวละคร.png").convert(), (self.width, self.height))
        self.character1 = pg.image.load("game-Project/ตัวละคร-1.png")
        self.character2 = pg.image.load("game-Project/ตัวละคร-2.png")
        self.character3 = pg.image.load("game-Project/ตัวละคร-3.png")
        self.back = pg.image.load("game-Project/หน้าหลักเกม/กลับ.png")

        self.selected_character = None
        self.setsize_character()  # เรียกเพื่อปรับขนาดของตัวละคร

    def setsize_character(self):
        self.character1 = pg.transform.scale(self.character1, (330, 270))
        self.character2 = pg.transform.scale(self.character2, (700, 460))
        self.character3 = pg.transform.scale(self.character3, (700, 460))
        self.back = pg.transform.scale(self.back, (110, 50))

    def gameLoop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  # เช็คว่ามีการคลิกเมาส์หรือไม่
                    mouse_pos = pg.mouse.get_pos()  # คืนค่าพิกัดของตำแหน่งเมาส์เมื่อคลิก
                    x, y = mouse_pos

                    # print(f"Mouse clicked at {mouse_pos}")  # แสดงพิกัดตำแหน่งเมาส์เมื่อคลิก

                    if 239 <= x <= 389 and 402 <= y <= 452:
                        # เลือกตัวละครตัวแรก
                        self.start_game = Game(1)
                        self.start_game.gameLoop()
                        return

                    if 520 <= x <= 677 and 405 <= y <= 455:
                        # เลือกตัวละครตัวที่สอง
                        self.start_game = Game(2)
                        self.start_game.gameLoop()
                        return
                    if 778 <= x <= 928 and 408 <= y <= 453:
                        # เลือกตัวละครตัวที่สาม
                        self.start_game = Game(3)
                        self.start_game.gameLoop()
                        return
                    if 35 <= x <= 136 and 487 <= y <= 524:
                        # รหัสสำหรับการกดปุ่มกลับ
                        self.back_Home()

            self.update_game()

    def update_game(self):
        self.win.blit(self.ground_img, (0, 0))
        self.win.blit(self.character1, (155, 215))  # ปรับพิกัดให้อยู่บนหน้าจอ
        self.win.blit(self.character2, (515, 103))
        self.win.blit(self.character3, (265, 108))
        self.win.blit(self.back, (30, 480))

        pg.display.update()
    
    def choose_character(self):
        # เริ่มต้นเกม
        start = ChooseCharacter()  # สร้างวัตถุของคลาส
        start.gameLoop()  # เรียกใช้งานฟังก์ชัน gameLoop เพื่อแสดงหน้าจอเกม
    
    def back_Home(self):
        from Homegame import Homegame  # นำเข้าคลาส ChooseCharacter
        self.Home = Homegame()