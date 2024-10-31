import pygame as pg
import sys
from Capybara import character  # Import character class
from obstacle import OB
from Item import Item
from coin import coin
import random  # เพิ่มการสุ่มความสูง

pg.init()

class Game:
    def __init__(self, character_type):
        # ตั้งค่าขนาดหน้าต่างเกม
        self.width = 1200
        self.height = 555
        self.scale_factor = 1.15
        self.scroll_speed = 0.6  # ความเร็วการเลื่อนพื้นหลัง
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Capybara Journey")  # ชื่อหน้าต่างเกม

        # โหลดภาพพื้นหลัง
        self.ground1_img = pg.transform.scale_by(pg.image.load("game-Project/พื้นหลังเกม-1.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("game-Project/พื้นหลังเกม-2.png").convert(), self.scale_factor)

        # ตั้งค่าพื้นหลัง
        self.set_background()

        # สร้างตัวละคร
        self.Image_size_character = 0.38
        self.character = character(self.Image_size_character, character_type)

        # สร้างเสาหลายต้น (OB)
        self.obstacle_speed = 10  # ความเร็วของเสา
        self.obstacle_list = []  # รายการสำหรับเก็บเสาหลายต้น
        self.create_obstacles(100)  # สร้างเสา 3 ต้น

        # ตัวแปรเพื่อเก็บจำนวนเหรียญและไอเท็มที่เก็บได้
        self.coin_collected = 0
        self.items_collected = 0

        # สร้างรายการและจับเวลาเหรียญ
        self.coins = []
        self.coin_timer = 0
        self.coin_spawn_time = 3  # เวลาในการสุ่มสร้างเหรียญเป็น 5 วินาที

        # สร้างรายการและจับเวลาไอเท็ม
        self.items = []
        self.item_timer = 0
        self.item_spawn_time = 10  # เวลาในการสุ่มสร้างไอเท็มเป็น 10 วินาที

        # ฟอนต์สำหรับแสดงข้อความ
        self.font = pg.font.Font(None, 36)

        self.clock = pg.time.Clock()  # นาฬิกาสำหรับควบคุมเฟรมเรต

    def create_obstacles(self, num_obstacles):
        for i in range(num_obstacles):
            initial_height = 335  
            new_obstacle = OB(self.obstacle_speed, 1200 + i * 350, initial_height)
            self.obstacle_list.append(new_obstacle)

    def create_item(self):
        # กำหนดตำแหน่ง X และ Y ของไอเท็มให้เป็นค่าคงที่
        item_x = 500  # ตำแหน่ง X ที่ต้องการ
        item_y = 230  # ตำแหน่ง Y ที่ต้องการ
        
        new_item = Item(item_x, item_y)  # สร้างไอเท็มที่ตำแหน่งใหม่
        new_item.rect = pg.Rect(item_x + 10, item_y + 10, 60, 60)  # ปรับ `rect` ให้ตรงกับขนาด
        self.items.append(new_item)  # เพิ่มไอเท็มในรายการ

    def create_coin(self):
        # กำหนดตำแหน่ง X และ Y ของเหรียญให้เป็นค่าคงที่
        coin_x = random.randint(500, 1200)  # เริ่มต้นที่ขอบขวาของหน้าจอ
        coin_y = random.randint(182, 300)  # สุ่มตำแหน่ง Y
        
        new_coin = coin(coin_x, coin_y)  # สร้างเหรียญที่ตำแหน่งใหม่
        new_coin.rect = pg.Rect(coin_x + 10, coin_y + 10, 60, 60)  # ปรับ `rect` ให้ตรงกับขนาด
        self.coins.append(new_coin)  # เพิ่มเหรียญในรายการ

    def gameLoop(self):
        while True:
            dt = self.clock.tick(60) / 1000  # คำนวณ delta time เป็นวินาที

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_SPACE, pg.K_RETURN, pg.K_UP):
                        self.character.jump()

            self.update_game(dt)

    def set_background(self):
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = self.ground2_rect.y = -250  # ตั้งค่า y ของพื้นหลัง

    def update_game(self, dt):
        # อัปเดตพื้นหลัง
        self.ground1_rect.x -= self.scroll_speed
        self.ground2_rect.x -= self.scroll_speed

        if self.ground1_rect.right <= 0:
            self.ground1_rect.x = self.ground2_rect.right
        if self.ground2_rect.right <= 0:
            self.ground2_rect.x = self.ground1_rect.right

        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)

        # วาดจำนวนเหรียญและไอเท็มที่เก็บได้
        coin_text = self.font.render(f"Coins Collected: {self.coin_collected}", True, (0, 0, 0))
        self.win.blit(coin_text, (10, 10))
        item_text = self.font.render(f"Items Collected: {self.items_collected}", True, (0, 0, 0))
        self.win.blit(item_text, (10, 40))

        # อัปเดตและวาดเหรียญ
        for coin in self.coins:
            coin.rect.x -= self.scroll_speed * dt * 50
            coin.draw(self.win)

            if self.character.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.coin_collected += 1

            elif coin.rect.x < -coin.rect.width:
                self.coins.remove(coin)

        # อัปเดตและวาดไอเท็ม
        for item in self.items:
            item.rect.x -= self.scroll_speed * dt * 50
            item.draw(self.win)

            if self.character.rect.colliderect(item.rect):
                self.items.remove(item)
                self.items_collected += 1

            elif item.rect.x < -item.rect.width:
                self.items.remove(item)

        # ตรวจสอบการจับเวลาเพื่อสร้างเหรียญและไอเท็มใหม่
        self.coin_timer += dt
        if self.coin_timer >= self.coin_spawn_time:
            self.create_coin()
            self.coin_timer = 0

        self.item_timer += dt
        if self.item_timer >= self.item_spawn_time:
            self.create_item()
            self.item_timer = 0
            # อัปเดตและวาดเสา

        for obstacle in self.obstacle_list:
            obstacle.update(dt)  # อัปเดตตำแหน่งเสา
            obstacle.draw_pipe(self.win)  # วาดเสา
            # อัปเดตตัวละคร
        
         # ตรวจสอบการชนกับเสา
        if self.character.rect.colliderect(obstacle.rect_down):
            pg.quit()
            sys.exit()

        self.character.update()
        self.win.blit(self.character.image, self.character.rect)

        pg.display.update()


def start_game(character_type):
    game = Game(character_type)
    game.gameLoop()
