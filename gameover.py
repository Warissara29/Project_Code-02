import pygame as pg
import sys
pg.init()

class gameover:
    def __init__(self, score, character_type):
        # ตั้งค่าหน้าจอ
        self.width = 1200
        self.height = 555
        self.score = score
        self.character_type = character_type

        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")  # ชื่อหน้าต่างเกม

        # เช็ค character_type และแสดงข้อมูลต่างๆ
        if self.character_type == 1:
           self.ground_img = pg.transform.scale(pg.image.load("./จบเกม/จบเกม1.png").convert(), (self.width, self.height))
        elif self.character_type == 2:
           self.ground_img = pg.transform.scale(pg.image.load("./จบเกม/จบเกม2.png").convert(), (self.width, self.height))
        elif self.character_type == 3:
          self.ground_img = pg.transform.scale(pg.image.load("./จบเกม/จบเกม3.png").convert(), (self.width, self.height))

        self.buttom_back = pg.image.load("./รูปภาพและไฟล์ประกอบ/เริ่มเกมใหม่.png")
        self.buttom_back = pg.transform.scale(self.buttom_back, (170, 80))

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
                    
                    if 957 <= x <= 1118 and 461 <= y <= 526:
                        self.back_Home()

                    if 1000 <= x <= 1100 and 300 <= y <= 400:
                        pg.quit()  # ปิด Pygame
                        sys.exit()  # ออกจากโปรแกรม

            self.update_game()  # เรียกฟังก์ชัน update_game()

    def update_game(self):

        # สร้างฟอนต์
        font = pg.font.Font(None, 100)  # ใช้ฟอนต์ขนาด 36

        # แสดงคะแนน
        character_ability_score = font.render(f"{self.score}", True, (0, 0, 0))  # ข้อความสีดำ

        # กำหนดตำแหน่งของข้อความ (ตรงกลางแนวนอน)
        score_rect = character_ability_score.get_rect(centerx=830, centery=325)  # วางที่กลางหน้าจอ (ค่าห่างจากกลาง)

        # วาดหน้าจอ
        self.win.blit(self.ground_img, (0, 0))
        self.win.blit(self.buttom_back, (955, 455))  # กำหนดตำแหน่งปุ่มบนหน้าจอ
        self.win.blit(character_ability_score, score_rect)

        # อัปเดตหน้าจอ
        pg.display.update()

    def game_over(self):
        self.end_game = gameover()
    
    def back_Home(self):
        from Homegame import Homegame  # นำเข้าคลาส Homegame
        self.Home = Homegame()

        

