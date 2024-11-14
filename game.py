import pygame as pg
import pygame
import sys
from gameover import gameover  # Import character gameover
from Capybara import character  # Import character class
from obstacle import OB  # Import OB class for obstacles
from coin import Coin  # Import Coin class for coins
from Item import Item  # Import Coin class for coins
import random  # Import random for generating random obstacle heights
import time

pg.init()

class Game:
    def __init__(self, character_type, pipe_spacing=1700):
        self.width = 1200
        self.height = 555
        self.scale_factor = 1.15
        self.scale_factor_ob = 0.4
        self.scale_factor_coin = 0.1  # เพิ่มขนาดของเหรียญ
        self.scale_factor_item = 0.2  # เพิ่มขนาดของไอเท้ม
        self.scroll_speed = 5

        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")

        # โหลดภาพพื้นหลัง
        self.ground1_img = pg.transform.scale_by(pg.image.load("./รูปภาพและไฟล์ประกอบ/พื้นหลังเกม-1.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("./รูปภาพและไฟล์ประกอบ/พื้นหลังเกม-2.png").convert(), self.scale_factor)
        self.bullet_img = pg.transform.scale_by(pg.image.load("./รูปภาพและไฟล์ประกอบ/กระสุน.png").convert_alpha(), 0.15)
        
        # ตั้งค่าพื้นหลัง
        self.set_background()

        # สร้างตัวละคร
        self.Image_size_character = 0.30
        self.character = character(self.Image_size_character, character_type)
        self.character_type = character_type
        self.character_life =  5

        self.clock = pg.time.Clock()

        self.ob = []  # เก็บอุปสรรค (เสา)
        self.coins = []  # เก็บเหรียญ
        self.item = []  # เก็บไอเท็ม
        self.ob_time_counter = 0  # ตัวนับเวลาสำหรับสร้างเสาใหม่
        self.coin_time_counter = 0  # ตัวนับเวลาสำหรับสร้างเหรียญใหม่
        self.item_time_counter = 0  # ตัวนับเวลาสำหรับสร้างไอเท็มใหม่
        self.move_speed = 250
        self.pipe_spacing = pipe_spacing  # ระยะห่างระหว่างเสา

        self.speed_multiplier = 1 
        self.time_counter = 0

        self.disappear = False  # ตัวแปรบอกว่าตัวละครหายตัวหรือไม่
        self.disappear_time = 0  # ตัวแปรเก็บเวลาเริ่มต้นที่หายตัว
        self.disappear_duration = 15  # ระยะเวลาที่ตัวละครจะหายตัว (15 วินาที)
        self.time_counter = 0  # ตัวนับเวลา
        self.item_duration =0

        self.is_flying = False  # Track flying state
        self.is_bullet = False 

        self.message_time = 0  # ตัวแปรสำหรับจับเวลาการแสดงข้อความ
        self.message_duration = 15  # ระยะเวลาที่ข้อความจะแสดง (15 วินาที)

        # เพิ่มตัวแปรนับคะแนน
        self.coin_count = 0  # ตัวนับเหรียญ
        self.item_count = 0  # ตัวนับไอเท็ม

        self.bulletY = 0
        self.bulletX = 0
        self.i =0

        # ตั้งค่าฟอนต์
        self.font = pg.font.SysFont('Arial', 30)

    def gameLoop(self):
        while True:
            dt = self.clock.tick(60) / 1000  # คำนวณ delta time เป็นวินาที

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_SPACE, pg.K_UP, pg.K_RETURN):
                        self.character.jump()
        
            self.update_game(dt)
            self.draw_game()
            pg.display.update()

    def set_background(self):
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = self.ground2_rect.y = -250

    def update_game(self, dt):
        self.time_counter += dt  # Accumulate elapsed time

        # Check if 60 seconds (1 minute) has passed
        if self.time_counter >= 60:
            self.speed_multiplier *= 1.1  # Increase speed by 10%
            self.time_counter = 0  # Reset the counter for the next minute

        self.move_speed = 370 * self.speed_multiplier  # Update obstacle speed with multiplier

        self.ground1_rect.x -= self.scroll_speed
        self.ground2_rect.x -= self.scroll_speed

        if self.ground1_rect.right <= 0:
            self.ground1_rect.x = self.ground2_rect.right
        if self.ground2_rect.right <= 0:
            self.ground2_rect.x = self.ground1_rect.right
        

        # อัปเดตตัวนับเวลาสำหรับอุปสรรค
        self.ob_time_counter += dt
        if self.ob_time_counter >= 0.8:  # ทุกๆ 0.8 วินาที
            self.ob.append(OB(self.scale_factor_ob, self.move_speed, self.pipe_spacing))
            self.ob_time_counter = 0

        # อัปเดตตัวนับเวลาสำหรับเหรียญ
        self.coin_time_counter += dt
        if self.coin_time_counter >= 2:  # ทุกๆ 3 วินาที (หรือช่วงเวลาที่ต้องการ)
            self.coins.append(Coin(self.scale_factor_coin, self.move_speed, self.pipe_spacing))
            self.coin_time_counter = 0

        # อัปเดตตัวนับเวลาสำหรับไอเท็ม
        self.item_time_counter += dt
        if self.item_time_counter >= 5:  # ทุกๆ 5 วินาที (หรือช่วงเวลาที่ต้องการ)
            self.item.append(Item(self.scale_factor_item, self.move_speed, self.pipe_spacing))  # เพิ่มไอเท็มลงใน self.item
            self.item_time_counter = 0

        # ตรวจสอบว่าได้ไอเท็มครบ 5 หรือไม่
        if self.item_count == 5 and self.character_type == 3:  # ถ้าตัวละครประเภท 3 และมีไอเท็มครบ 5
            self.disappear = True  # ให้ตัวละครหายตัว
            self.item_start_time_dis = time.time()  # บันทึกเวลาที่เริ่มใช้งานไอเท็ม
            self.disappear_time = 0  # รีเซ็ตเวลา
            self.item_count = 0  # รีเซ็ตไอเท็ม

         # อัปเดตการเคลื่อนที่ของอุปสรรค
        if self.character_type == 2 and self.item_count == 5:
            self.is_bullet = True
            self.item_count = 0

        for pipe in self.ob:
            pipe.update(dt)

            # # ตรวจสอบการชนกับเสา
            # if self.character.rect.colliderect(pipe.rect_down.inflate(-20, 0)):
            #     if not self.disappear:  # ถ้าตัวละครไม่หายตัว
            #         self.character_life -= 1  # ลดชีวิต 1 ครั้งเมื่อชนเสา
            #         self.ob.remove(pipe)  # ลบเสาที่ถูกชนออกจากหน้าจอ
            #         if self.character_life == 0:
            #             self.out_game(False)  # ถ้าชีวิตหมดให้จบเกม

            if self.character.shoot_bullet(self.is_bullet):
                self.bulletX = 280  # ปรับให้กระสุนเคลื่อนที่ไปข้างหน้า (10 คือความเร็วของกระสุน)
                self.bulletY = 425  # ตำแหน่ง Y ของกระสุนคงที่

                if self.bulletX >= pipe.rect_down.left and self.bulletX <= pipe.rect_down.right:
                    self.i += 1
                    self.ob.remove(pipe)  # ลบเสาที่ถูกชน

                    # ทำลายเสาได้ 10 ต้น
                    if self.i >= 10:
                        self.is_bullet = False  # หยุดยิงกระสุน
                        self.i = 0  # รีเซ็ตตัวนับการทำลายเสา

        # อัปเดตการหายตัว
        if self.disappear:
            self.time_counter += dt  # เพิ่มค่าเวลา
            
            if self.disappear_time >= self.disappear_duration:  # ถ้าเวลาที่เหลือหมดลง
                self.disappear = False  # ยกเลิกการหายตัว
                        
        # อัปเดตการเคลื่อนที่ของเหรียญ
        for coin in self.coins:
            coin.update(dt)

            # ตรวจสอบการชนกับตัวละคร
            if self.character.rect.colliderect(coin.rect):
                self.coins.remove(coin)  # ลบเหรียญที่ถูกเก็บ
                self.coin_count += 1  # เพิ่มคะแนนเหรียญ 

        # อัปเดตการเคลื่อนที่ของไอเท็ม
        for item in self.item:
            item.update(dt)

            # ตรวจสอบการชนกับตัวละคร
            if self.character.rect.colliderect(item.rect):
                self.item.remove(item)  # ลบไอเท็มที่ถูกเก็บ
                self.item_count += 1  # เพิ่มคะแนนไอเท็ม

        # ลบอุปสรรคและเหรียญที่หลุดออกจากหน้าจอ
        self.ob = [pipe for pipe in self.ob if pipe.rect_down.right > 0]
        self.coins = [coin for coin in self.coins if coin.rect.right > 0]
        self.item = [item for item in self.item if item.rect.right > 0]

        # อัปเดตตัวละคร
        self.character.update()

    def draw_game(self):
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)

        # วาดอุปสรรค
        for pipe in self.ob:
            pipe.draw_pipe(self.win)

        # วาดเหรียญ
        for coin in self.coins:
            coin.draw_coin(self.win)

        # วาดไอเท็ม
        for item in self.item:
            item.draw_coin(self.win)  # ไอเท็มและเหรียญใช้ฟังก์ชันเดียวกัน

        # วาดตัวละคร
        self.win.blit(self.character.image, self.character.rect)

        # วาดคะแนน
        coin_text = self.font.render(f'  Coins: {self.coin_count}', True, (0, 0, 0))
        coin_bg = pygame.Surface((coin_text.get_width() + 10, coin_text.get_height() + 10))  # ขนาดพื้นหลัง
        coin_bg.fill((255, 255, 255))  # สีพื้นหลัง (สีขาว)
        self.win.blit(coin_bg, (20 - 5, 10 - 5))  # วางพื้นหลังให้เหมาะสม
        self.win.blit(coin_text, (10, 10))  # วางข้อความ

        # วาดจำนวนไอเท็ม
        item_text = self.font.render(f'  Item: {self.item_count}/5', True, (0, 0, 0))
        item_bg = pygame.Surface((item_text.get_width() + 10, item_text.get_height() + 10))  # ขนาดพื้นหลัง
        item_bg.fill((255, 255, 255))  # สีพื้นหลัง (สีขาว)
        self.win.blit(item_bg, (20 - 5, 50 - 5))  # วางพื้นหลังให้เหมาะสม
        self.win.blit(item_text, (10, 50))  # วางข้อความ

        # วาดจำนวนชีวิต
        lie_text = self.font.render(f'  Character life: {self.character_life}/5', True, (0, 0, 0))
        lie_bg = pygame.Surface((lie_text.get_width() + 10, lie_text.get_height() + 10))  # ขนาดพื้นหลัง
        lie_bg.fill((255, 255, 255))  # สีพื้นหลัง (สีขาว)
        self.win.blit(lie_bg, (20 - 5, 90 - 5))  # วางพื้นหลังให้เหมาะสม
        self.win.blit(lie_text, (10, 90))  # วางข้อความ

        if self.character_type == 1 and self.is_flying and self.item_count == 0:
            self.is_flying = False
            self.item_start_time = time.time()  # บันทึกเวลาที่เริ่มใช้งานไอเท็ม
            self.item_duration = 15  # กำหนดเวลาให้ไอเท็มหมดอายุใน 15 วินาที

        # คำนวณเวลาที่เหลือและแสดงผลจนกว่าจะหมดเวลา
        if hasattr(self, 'item_start_time') and self.item_duration > 0:
            elapsed_time = time.time() - self.item_start_time  # คำนวณเวลาที่ผ่านไป
            remaining_time = max(0, self.item_duration - int(elapsed_time))  # คำนวณเวลาที่เหลือ

            # ถ้ามีเวลาที่เหลืออยู่ให้แสดงผลนับถอยหลัง
            if remaining_time > 0 and self.character_type == 1:
                text = self.font.render(f'You can use Flying item {remaining_time} seconds!', True, (0, 0, 0))
                self.win.blit(text, (425, 140))

        if self.character_type == 1 and self.is_flying == False and self.item_count == 0 and not hasattr(self, 'item_start_time'):
            text = self.font.render(f'  The item is collected for use.. !', True, (0, 0, 0))
            self.win.blit(text, (425, 120))

        if self.character_type==2 and self.is_bullet == True and self.item_count >= 0:
            self.is_bullet == False
            text = self.font.render(f' You can use items to shoot and destroy 10 obstacles !', True, (0, 0, 0))
            self.win.blit(text, (325, 120))

        if self.character_type==2 and self.is_bullet == False and self.item_count == 0:
            text = self.font.render(f'  The item is collected for use.. !', True, (0, 0, 0))
            self.win.blit(text, (425, 120))
        
        if self.character_type == 3 and self.disappear and self.item_count == 0:
            self.disappear == False
           
        # คำนวณเวลาที่เหลือและแสดงผลจนกว่าจะหมดเวลา
        if hasattr(self, 'item_start_time_dis') and self.disappear_duration > 0:
            elapsed_time_dis = time.time() - self.item_start_time_dis  # คำนวณเวลาที่ผ่านไป
            remaining_time_dis = max(0, self.disappear_duration - int(elapsed_time_dis))  # คำนวณเวลาที่เหลือ

            # ถ้ามีเวลาที่เหลืออยู่ให้แสดงผลนับถอยหลัง
            if remaining_time_dis > 0 and self.character_type == 3:
                text = self.font.render(f'You can use the invisibility item {remaining_time_dis} seconds!', True, (0, 0, 0))
                self.win.blit(text, (425, 140))
            else:
                self.disappear = False  # รีเซ็ตการหายตัวเมื่อหมดเวลา

        if self.character_type == 3 and self.disappear == False and self.item_count >= 0 and not hasattr(self, 'item_start_time_dis'):
            text = self.font.render(f'  The item is collected for use.. !', True, (0, 0, 0))
            self.win.blit(text, (425, 120))

        if not self.is_bullet and self.character_type == 2:
            self.win.blit(self.bullet_img, (30, 150))
        if  self.is_bullet and self.character_type == 2:
            self.win.blit(self.bullet_img, (self.bulletX, self.bulletY))
        
        while self.character_type == 1 and self.item_count == 5:
            self.character.fly()
            self.is_flying  = True
            self.item_count = 0
                
    def start_game(self, character_type, pipe_spacing=600):
        game = Game(character_type, pipe_spacing)
        game.gameLoop()

    def out_game(self,disappear):
        if disappear == True:
            pass
        else:
            score = self.coin_count  # For example, using coin_count as the score
            self.game_over_screen = gameover(score, self.character_type)
            self.game_over_screen.game_over()