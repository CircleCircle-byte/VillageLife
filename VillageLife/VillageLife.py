import pygame
from sys import exit
from pygame import mouse
import math
import time
import random

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('VillageLife')
clock = pygame.time.Clock()
text_font = pygame.font.Font('Pixel.ttf', 50)

class FishMiniGame:
    def __init__(self):
        self.bar = pygame.Rect(360, 80, 80, 240)
        self.cursor_y = self.bar.centery
        self.dir = 1
        self.speed = 5
        self.target = pygame.Rect(self.bar.x + 10, 0, self.bar.w - 20, 60)
        self.reset_target()

    def reset_target(self):
        self.target.y = random.randint(self.bar.top + 10, self.bar.bottom - 70)

    def update(self, keys):
        self.cursor_y += self.dir * self.speed
        if self.cursor_y < self.bar.top + 10:
            self.cursor_y = self.bar.top + 10
            self.dir = 1
        if self.cursor_y > self.bar.bottom - 10:
            self.cursor_y = self.bar.bottom - 10
            self.dir = -1

        if keys[pygame.K_SPACE]:
            cursor_rect = pygame.Rect(self.bar.centerx - 8, self.cursor_y - 8, 16, 16)
            return True, cursor_rect.colliderect(self.target)
        if keys[pygame.K_ESCAPE]:
            return True, False

        return False, None

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.bar, 3, border_radius=10)
        pygame.draw.rect(surface, (80, 200, 120), self.target, 0, border_radius=8)
        cursor_rect = pygame.Rect(self.bar.centerx - 8, self.cursor_y - 8, 16, 16)
        pygame.draw.rect(surface, (30, 30, 30), cursor_rect, 0, border_radius=4)

class Button(object):
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def check_click(self, position):
        return (self.x < position[0] < self.x + self.width) and (self.y < position[1] < self.y + self.height)

    def draw(self, surface, font, base_color='black', hover_color='green', rect_color=None):
        mouse_pos = pygame.mouse.get_pos()
        if self.check_click(mouse_pos):
            color = hover_color
        else:
            color = base_color
        if rect_color:
            pygame.draw.rect(surface, rect_color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        surface.blit(text_surface, text_rect)

inventory = {
    'fish': 0,
    'crop': 0
}


home_surface = pygame.image.load('pictures/home.png').convert()
text_surface = text_font.render('Village  Life', True, 'Black')
farm_surface = pygame.image.load('pictures/farm.png').convert()
house_surface = pygame.image.load('pictures/house.png').convert()
lake_surface = pygame.image.load('pictures/lake.png').convert()
rob_surface = pygame.image.load('pictures/rob.png').convert_alpha()


bird_surface = pygame.image.load('pictures/bird.png').convert_alpha()
bird_rect = bird_surface.get_rect(bottomleft=(0,100))

player_surface = pygame.image.load('pictures/man.png').convert_alpha()
player_rect = player_surface.get_rect(bottomleft=(200,350))

field_rect = pygame.Rect(80, 210, 225, 165)

chest_surface = pygame.image.load('pictures/chest.png').convert_alpha()
chest_rect = chest_surface.get_rect(topleft=(500, 200))
chest_inventory = {'fish': 0, 'crop': 0}


selected_item = 'fish'



begin_button = Button(300, 200, 200, 50,'Begin')
exit_button = Button(300, 280, 200, 50,'Exit')
exit2_button = Button(600, 20, 200, 50,'Exit')
door_out_button = Button(500, 300, 200, 50,'Open door')
lake_button = Button(500, 300, 200, 50,'Fish')
door_in_button = Button(500, 300, 200, 50,'Open door')
fish_button = Button(500, 300, 200, 50,'Got a bite!')

put_button = Button(500,300, 200, 50, 'Put item')
get_button = Button(500, 350, 200, 50, 'Get item')


mouse_pos = pygame.mouse.get_pos()

speed = 1

crop_planted = False
crop_ready = False
crop_plant_time = 0


game_started = False
in_house = False
fishing = False
fish_mini = None

space_locked = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pygame.key.set_repeat(50, 80)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_rect.y -= 10 * speed
            if event.key == pygame.K_s:
                player_rect.y += 10 * speed
            if event.key == pygame.K_a:
                player_rect.x -= 10 * speed
            if event.key == pygame.K_d:
                player_rect.x += 10 * speed

            if event.key == pygame.K_SPACE:
                if game_started and (not in_house) and (not fishing) and player_rect.colliderect(field_rect):
                    if not crop_planted:
                        crop_planted = True
                        crop_ready = False
                        crop_plant_time = pygame.time.get_ticks()
                        space_locked = True
                    elif crop_ready:
                        inventory["crop"] += 1
                        crop_planted = False
                        crop_ready = False
                        crop_plant_time = 0
                        space_locked = True
                space_locked = False

            mouse_pos = pygame.mouse.get_pos()
    print(mouse_pos)


    if not game_started:

        screen.blit(home_surface, (0, 0))
        screen.blit(text_surface, (250, 100))
        bird_rect.x += 2
        bird_rect.y = 20 + int(10 * math.sin(pygame.time.get_ticks() * 0.01) + 5)
        if bird_rect.x > 800:
            bird_rect.x = -10
        screen.blit(bird_surface, bird_rect)
        begin_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
        exit_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if begin_button.check_click(event.pos) :
                game_started = True
            if exit_button.check_click(event.pos) :
                pygame.quit()
                exit()

    else:

        screen.blit(farm_surface,(0,0))
        inventory_text = f"Fish: {inventory['fish']} Crop: {inventory['crop']}"
        inv_surface = text_font.render(inventory_text, True, 'black')
        screen.blit(inv_surface, (10,10))

        exit2_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit2_button.check_click(event.pos) :
                pygame.quit()
                exit()

        if not crop_planted:
            field_color = (150, 100, 50)
        elif crop_planted and not crop_ready:
            field_color = (50, 180, 50)
        else:
            field_color = (220, 200, 50)

        pygame.draw.rect(screen, field_color, field_rect)
        pygame.draw.rect(screen, 'SaddleBrown', field_rect, 10)

        if crop_planted and (not crop_ready):
            if pygame.time.get_ticks() - crop_plant_time >= 5000:  # 5 秒成熟
                crop_ready = True

        if player_rect.colliderect(field_rect):
            if not crop_planted:
                msg = "plant: SPACE"
            elif not crop_ready:
                msg = "Growing..."
            else:
                msg = "Harvest: SPACE"
            tip = text_font.render(msg, True, 'black')
            screen.blit(tip, (400,300))

        screen.blit(player_surface, player_rect)

        if player_rect.colliderect(325,170,20,10) and (not player_rect.colliderect(field_rect)):
            door_out_button.draw(screen, text_font, base_color='black',hover_color='green', rect_color=None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if door_out_button.check_click(event.pos):
                    in_house = True

        if player_rect.colliderect(500, 100, 200, 100):
            lake_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lake_button.check_click(event.pos):
                    fishing = True

        if in_house:
            screen.blit(house_surface, (0, 0))
            screen.blit(chest_surface, chest_rect)
            screen.blit(player_surface, player_rect)
            inventory_text = f"Fish: {inventory['fish']} Crop: {inventory['crop']}"
            inv_surface = text_font.render(inventory_text, True, 'black')
            screen.blit(inv_surface, (10, 10))
            exit2_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit2_button.check_click(event.pos):
                    pygame.quit()
                    exit()

            if player_rect.colliderect(chest_rect.inflate(40, 40)):
                tip_text = text_font.render(f"selected: {selected_item}", True, 'black')
                tip2_text = text_font.render(f"Fish: {chest_inventory['fish']} Crop: {chest_inventory['crop']}", True, 'black')
                screen.blit(tip_text, (250, 220))
                screen.blit(tip2_text, (250, 265))
                put_button.draw(screen, text_font, base_color='black', hover_color='green')
                get_button.draw(screen, text_font, base_color='black', hover_color='green')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not space_locked:
                        if selected_item == 'fish':
                            selected_item = 'crop'
                        else:
                            selected_item = 'fish'
                        space_locked = True
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    space_locked = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if put_button.check_click(event.pos):
                        if inventory[selected_item] > 0:
                            inventory[selected_item] -= 1
                            chest_inventory[selected_item] += 1
                        else:
                            pass

                    if get_button.check_click(event.pos):
                        if chest_inventory[selected_item] > 0:
                            chest_inventory[selected_item] -= 1
                            inventory[selected_item] += 1
                        else:
                            pass

            if player_rect.colliderect(380, 380, 50, 20):
                door_in_button.draw(screen, text_font, base_color='black', hover_color='green', rect_color=None)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if door_in_button.check_click(event.pos):
                        in_house = False

        if (not in_house) and fishing:
            screen.blit(lake_surface, (0, 0))
            screen.blit(rob_surface,(380,300))
            if fish_mini is None:
                fish_mini = FishMiniGame()

            fish_mini.draw(screen)
            tip = text_font.render('SPACE: hook | ESC: back', True, 'black')
            screen.blit(tip, tip.get_rect(center=(400, 40)))

            done, success = fish_mini.update(pygame.key.get_pressed())
            if done:
                if success:
                    inventory['fish'] += 1
                    success = text_font.render(f'You caught a fish! Total fish: {inventory['fish']}',True, 'black')
                    screen.blit(success, (20, 300))
                    pygame.display.update()
                    pygame.time.delay(2000)

                else:
                    false = text_font.render('The fish got away...',True,'black')
                    screen.blit(false, (100, 300))
                    pygame.display.update()
                    pygame.time.delay(2000)

                fishing = False
                fish_mini = None

        else:
            fishing = False


    pygame.display.update()
    clock.tick(60)