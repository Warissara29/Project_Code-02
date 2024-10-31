import pygame as pg

class character(pg.sprite.Sprite):
    def __init__(self, scale_factor, character_type):
        super(character, self).__init__()

        self.scale_factor = scale_factor
        self.img_list = []
        self.is_jumping = False  # ตัวแปรตรวจสอบว่าตัวละครกำลังกระโดดอยู่หรือไม่
        self.velocity_y = 3  # ความเร็วในแนว Y
        self.gravity = 0.9  # ค่าแรงโน้มถ่วง
        self.jump_height = 20   # ความสูงที่ตัวละครจะกระโดด

        # โหลดภาพตัวละครและปรับขนาดตาม scale factor
        if character_type == 1:
            self.img_list.append(pg.transform.scale_by(pg.image.load("game-Project/ตัวละคร-1.png").convert_alpha(), scale_factor))
        elif character_type == 2:
            self.img_list.append(pg.transform.scale_by(pg.image.load("game-Project/ตัวละคร-3.png").convert_alpha(), scale_factor))
        elif character_type == 3:
            self.img_list.append(pg.transform.scale_by(pg.image.load("game-Project/ตัวละคร-2.png").convert_alpha(), scale_factor))

        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(200, 425))  # กำหนดตำแหน่งของตัวละคร

    def jump(self):
        if not self.is_jumping:  # ตรวจสอบว่าตัวละครไม่ได้กระโดดอยู่แล้ว
            self.is_jumping = True
            self.velocity_y = -self.jump_height  # เริ่มต้นความเร็ว Y เพื่อกระโดดขึ้น

    def update(self):
        # ฟังก์ชันสำหรับอัปเดตตัวละคร หากมีการเปลี่ยนแปลง (เช่นการเคลื่อนไหว)
        self.image_index += 0.1
        if self.image_index >= len(self.img_list):
            self.image_index = 0

        self.image = self.img_list[int(self.image_index)]

        # การจัดการการกระโดด
        if self.is_jumping:
            self.velocity_y += self.gravity  # ใช้แรงโน้มถ่วง
            self.rect.y += self.velocity_y  # อัปเดตตำแหน่ง Y ของตัวละคร

            # ตรวจสอบว่ากลับมาที่พื้นหรือไม่
            if self.rect.y >= 335:  # สมมติว่า 335 คือระดับพื้น
                self.rect.y = 335  # กลับไปที่ระดับพื้น
                self.is_jumping = False  # เปลี่ยนสถานะการกระโดดกลับมาเป็น False
