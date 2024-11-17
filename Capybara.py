import pygame as pg
import time

class character(pg.sprite.Sprite):
    def __init__(self, scale_factor, character_type):
        super(character, self).__init__()

        # Initialize attributes
        self.scale_factor = scale_factor
        self.img_list = []
        self.is_jumping = False
        self.is_flying = False  # Track flying state
        self.is_shoot = False  # Track shooting state
        self.is_descending = False  # Track if character is descending
        self.velocity_y = 3
        self.gravity = 0.9
        self.hover_speed = -15
        self.jump_height = 19

        # Add a timer attribute
        self.fly_start_time = None  # Will be set when flying starts
        self.fly_duration = 15  # Duration in seconds
        self.descend_start_time = None  # Time to track descent

        # Load character images
        if character_type == 1:
            self.img_list.append(pg.transform.scale_by(pg.image.load("รูปภาพและไฟล์ประกอบ/ตัวละคร-1.png").convert_alpha(), scale_factor))
        elif character_type == 2:
            self.img_list.append(pg.transform.scale_by(pg.image.load("รูปภาพและไฟล์ประกอบ/ตัวละคร-3.png").convert_alpha(), scale_factor))
        elif character_type == 3:
            self.img_list.append(pg.transform.scale_by(pg.image.load("รูปภาพและไฟล์ประกอบ/ตัวละคร-2.png").convert_alpha(), scale_factor))        
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(200, 425))  # Initial position

        # Initialize bullet-related attributes
        self.scale_factor_bullet = 1  # Set the scale factor for the bullet
        self.cal_shoot = self.rect.x + self.rect.width  # Start the bullet slightly in front of the character

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_height

    # ฟังก์ชันในคลาส character
    def shoot_bullet(self, shoot):
        self.is_shoot = shoot  # Track shooting state
        return self.is_shoot 

    def fly(self):
        if not self.is_flying:  # Start flying if not already flying
            self.is_flying = True
            self.fly_start_time = time.time()  # Record the start time of flying
            self.rect = self.image.get_rect(center=(200, self.rect.y))  # Position at start of flying
            
    def update(self):
        # Update animation frame
        self.image_index += 0.1
        if self.image_index >= len(self.img_list):
            self.image_index = 0
        self.image = self.img_list[int(self.image_index)]

        # Handle jumping mechanics
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= 400:
                self.rect.y = 400
                self.is_jumping = False

        # Handle flying mechanics
        if self.is_flying and self.is_jumping == False:
            self.rect.y += self.hover_speed  # Gradual ascent while flying
            if self.rect.y <= 200:  # Stop flying when reaching the height limit
                self.rect.y = 200

            # Check if 5 seconds have passed since the flight started
            if time.time() - self.fly_start_time >= self.fly_duration:
                self.is_flying = False  # Stop flying after 5 seconds
                self.is_descending = True  # Start descending after flying
                self.descend_start_time = time.time()  # Record start of descent

        # Handle gradual descent after flight
        if self.is_descending:
            descent_speed = 3  # Speed of descent
            self.rect.y += descent_speed  # Gradually move down
            if self.rect.y >= 400:  # Stop descending once reaching ground level
                self.rect.y = 400
                self.is_descending = False  # End descending
