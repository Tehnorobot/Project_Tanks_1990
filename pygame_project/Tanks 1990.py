import pygame
import sys
import os
import time
import sqlite3
import datetime

FPS = 100
# Функции

def game_creation():
    return size, screen, clock

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        terminate()
    image = pygame.image.load(fullname)
    return image

def music(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        terminate()
    pygame.mixer.music.load('data/' + name)
    pygame.mixer.music.play(0)

def music_start(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        terminate()
    pygame.mixer.music.load('data/' + name)
    pygame.mixer.music.play(-1)

def move_pictire(name):
    size = [754, 550]
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    count = -550
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if count < 0:
            screen.blit(name, (0, count))
        else:
            running = False
        pygame.display.flip()
        clock.tick(10)
        count += 10

def get_level(font, fon2, fname):
    maps = {'Уровень 1': 'map1.txt', 'Уровень 2': 'map2.txt', 
            'Уровень 3': 'map3.txt', 'Уровень 4': 'map4.txt', 'Уровень 5': 'map5.txt', 
            'Назад': ''}
    button = {}
    screen.blit(fon2, (0, 0))
    font = pygame.font.SysFont('serif', 48)
    text_coord = 200
    for j, (line, name_map) in enumerate(maps.items()):
        string_rendered = font.render(line, 4, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        button.update({line: intro_rect})
        intro_rect.top = text_coord
        text_coord += 60
        intro_rect.x = 200
        if j == len(maps) - 1:
            intro_rect.x = 600
            intro_rect.top = 200
        screen.blit(string_rendered, intro_rect) 
    func = False
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, k in button.items():
                    if k.collidepoint(pos):
                        now_button = (i, k)
                        func = True
                        running = False
                        
            for i, k in button.items():
                if k.collidepoint(pos):
                    text_rendered = font.render(i, 5, pygame.Color('Black'))
                    screen.blit(text_rendered, k) 
                    text_rendered = font.render(i, 4, pygame.Color('Red'))
                    screen.blit(text_rendered, k) 
                else:
                    text_rendered = font.render(i, 4, pygame.Color('White'))
                    screen.blit(text_rendered, k) 
        pygame.display.flip()
        clock.tick(FPS)
                
    if func:
        if now_button[0] != 'Назад':
            level_map = maps[now_button[0]]
            if now_button[0] == 'Уровень 1':
                level_map = maps[now_button[0]]
            if now_button[0] == 'Уровень 2':
                level_map = maps[now_button[0]]
            if now_button[0] == 'Уровень 3':
                level_map = maps[now_button[0]]
            if now_button[0] == 'Уровень 4':
                level_map = maps[now_button[0]]
            if now_button[0] == 'Уровень 5':
                level_map = maps[now_button[0]]
            difficulty_level = now_button[0]
            return level_map, difficulty_level
        else:
            return 'cancel'
        
def start_screen(screen, width, height, fname, clock):
    pygame.mixer.music.stop()
    music_start('sound_menu.mp3')
    button = {}
    fon = pygame.transform.scale(load_image('fon3.jpg'), (width, height))
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    move_pictire(fon)
    intro_text = ["Старт",
                  "Статистика",
                  'Правила',
                  "Выход"]
    screen.blit(fon2, (0, 0))
    font = pygame.font.SysFont('serif', 48)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 4, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        button.update({line: intro_rect})
        intro_rect.top = text_coord
        text_coord += 60
        intro_rect.x = 200
        screen.blit(string_rendered, intro_rect)
        
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, k in button.items():
                    if k.collidepoint(pos):
                        now_button = (i, k)
                        running = False
                        
            for i, k in button.items():
                if k.collidepoint(pos):
                    text_rendered = font.render(i, 5, pygame.Color('Black'))
                    screen.blit(text_rendered, k) 
                    text_rendered = font.render(i, 4, pygame.Color('Red'))
                    screen.blit(text_rendered, k) 
                else:
                    text_rendered = font.render(i, 4, pygame.Color('White'))
                    screen.blit(text_rendered, k) 
        pygame.display.flip()
        clock.tick(FPS)
    if now_button[0] == 'Старт':
        level_map, difficulty_level = get_level(font, fon2, fname)
        t_start = time.time()
        music('start_game.mp3')
        return level_map, difficulty_level, t_start
    if now_button[0] == 'Статистика':
        statistic(screen, width, height, fname, clock)
    if now_button[0] == 'Правила':
        rules(screen, width, height, fname, clock)
    if now_button[0] == 'Выход':
        terminate()

def statistic(screen, width, height, fname, clock):
    button = {}
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    
    intro_text = ["Назад"]
    head_list = ['Результат игры', 'Продолжительность игры(в секундах)', 'Дата игры']
    screen.blit(fon2, (0, 0))
    font = pygame.font.SysFont('serif', 48)
    font_2 = pygame.font.SysFont('serif', 20)
    
    connection = sqlite3.connect("data/data.db")
    cur = connection.cursor()
    statistic = cur.execute('SELECT * FROM info').fetchall()
    color = ['Yellow', 'Green', 'Red']
    num = 0
    list_len = []
    
    for line in intro_text:
        string_rendered = font.render(line, 4, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        button.update({line: intro_rect})
        intro_rect.x = 600
        intro_rect.top = 160
        screen.blit(string_rendered, intro_rect)
    text_coords = 20
    for c, i in enumerate(head_list):
        string_rendered = font_2.render(i, 2, pygame.Color(color[c]))
        text = string_rendered.get_rect()
        list_len.append(text_coords)
        text.x = text_coords
        text.y = 210
        text_coords += len(str(i)) * 10
        screen.blit(string_rendered, text) 
    
    text_coord = 230
    count = 16
    if len(statistic) > count:
        cur.execute('DELETE FROM info')
        connection.commit()
    
    for c, i in enumerate(statistic):
        for h, j in enumerate(i[1::]):
            string_rendered = font_2.render(str(j), 2, pygame.Color(color[num]))
            text = string_rendered.get_rect()
            text.x = list_len[num]
            text.y = text_coord + (20 * c)
            screen.blit(string_rendered, text) 
            num += 1
            if num == 3:
                num = 0
    connection.close()
        
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, k in button.items():
                    if k.collidepoint(pos):
                        now_button = (i, k)
                        running = False
                        
            for i, k in button.items():
                if k.collidepoint(pos):
                    text_rendered = font.render(i, 5, pygame.Color('Black'))
                    screen.blit(text_rendered, k) 
                    text_rendered = font.render(i, 4, pygame.Color('Red'))
                    screen.blit(text_rendered, k) 
                else:
                    text_rendered = font.render(i, 4, pygame.Color('White'))
                    screen.blit(text_rendered, k) 
        pygame.display.flip()
        clock.tick(FPS)
    if now_button[0] == 'Назад':
        val = (screen, width, height, fname, clock)
        return val
    
def rules(screen, width, height, fname, clock):
    button = {}
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    
    intro_text = ["Назад"]
    screen.blit(fon2, (0, 0))
    font = pygame.font.SysFont('serif', 48)
    font_2 = pygame.font.SysFont('serif', 20)
    rules = ['Цель игры:', 'Выстрелить в танк и уничтожить врага.', '',
             'Управление танком:', 'Клавиша "[↑]" - движение вперёд', 
             'Клавиша "[↓]" - движение назад', 'Клавиша "[←]" - движение влево', 
             'Клавиша "[→]" - движение вправо', 'Клавиша "space" - выстрелить']
    
    for line in intro_text:
        string_rendered = font.render(line, 4, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        button.update({line: intro_rect})
        intro_rect.x = 600
        intro_rect.top = 200
        screen.blit(string_rendered, intro_rect)
    text_coord = 180   
    
    for i in rules:
        string_rendered = font_2.render(i, 2, pygame.Color('Green'))
        text = string_rendered.get_rect()
        text.x = 20
        text.y = text_coord
        text_coord += 40
        screen.blit(string_rendered, text) 
        
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, k in button.items():
                    if k.collidepoint(pos):
                        now_button = (i, k)
                        running = False
                        
            for i, k in button.items():
                if k.collidepoint(pos):
                    text_rendered = font.render(i, 5, pygame.Color('Black'))
                    screen.blit(text_rendered, k) 
                    text_rendered = font.render(i, 4, pygame.Color('Red'))
                    screen.blit(text_rendered, k) 
                else:
                    text_rendered = font.render(i, 4, pygame.Color('White'))
                    screen.blit(text_rendered, k) 
        pygame.display.flip()
        clock.tick(FPS)
    if now_button[0] == 'Назад':
        val = (screen, width, height, fname, clock)
        return val

def end_screen(screen, width, height, fname, clock, game_res):
    button = {}
    fon = pygame.transform.scale(load_image('fon3.jpg'), (width, height))
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    
    move_pictire(fon)
    if game_res == 'win':
        res = 'Победа! Вы уничтожили врага.'
    if game_res == 'lose':
        res = 'Поражение! Ваш танк уничтожен.'
    intro_text = ["Выход"]
    screen.blit(fon2, (0, 0))
    font = pygame.font.SysFont('serif', 48)
    text_coord = 400
    for line in intro_text:
        string_rendered = font.render(line, 4, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        button.update({line: intro_rect})
        intro_rect.top = text_coord
        intro_rect.x = 20
        screen.blit(string_rendered, intro_rect) 
    
    if res == 'Победа! Вы уничтожили врага.':
        music('win.mp3')
        string_rendered = font.render(res, 4, pygame.Color('Yellow'))
        text = string_rendered.get_rect()
        text.y = 230
        text.x = 20       
        screen.blit(string_rendered, text) 
        
    if res == 'Поражение! Ваш танк уничтожен.':
        music('lose.mp3')
        string_rendered = font.render(res, 4, pygame.Color('Red'))
        text = string_rendered.get_rect()
        text.y = 230
        text.x = 20
        screen.blit(string_rendered, text) 
        
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, k in button.items():
                    if k.collidepoint(pos):
                        now_button = (i, k)
                        running = False
                        
            for i, k in button.items():
                if k.collidepoint(pos):
                    text_rendered = font.render(i, 5, pygame.Color('Black'))
                    screen.blit(text_rendered, k) 
                    text_rendered = font.render(i, 4, pygame.Color('Red'))
                    screen.blit(text_rendered, k) 
                else:
                    text_rendered = font.render(i, 4, pygame.Color('White'))
                    screen.blit(text_rendered, k) 
        pygame.display.flip()
        clock.tick(FPS)
    if now_button[0] == 'Выход':
        return

# Классы
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, tiles_group, all_sprites,
                 tile_images, tile_width, tile_height,
                 pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
            

    def update(self, game, x, y):
        tile_images = game.tile_images
        if self.x == x and self.y == y:
            self.image = tile_images['empty']


class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, player_image,
                         tile_width, tile_height,
                         pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        
    def update(self, event, game, rotates):
        direct = ''
        tile_width = game.tile_width
        level_x, level_y = game.x, game.y
        level = game.level.copy()
        if event.key == pygame.K_RIGHT and (level[self.y%(level_y + 1)][(self.x + 1)%(level_x + 1)] != '#'):
            rotates.append('right')
            direct += 'right'
            if rotates[-2] == 'left':
                angle = -180
            if rotates[-2] == 'up':
                angle = -90
            if rotates[-2] == 'down':
                angle = 90
            if rotates[-2] != 'right':
                self.image = pygame.transform.rotate(self.image, angle)
                self.image.get_rect(center=self.rect.center)
            self.rect.x += tile_width
            self.x = (self.x + 1) % (level_x + 1)
        elif event.key == pygame.K_LEFT and (level[self.y%(level_y + 1)][(self.x - 1)%(level_x + 1)] != '#'):
            rotates.append('left')
            direct += 'left'
            if rotates[-2] == 'right':
                angle = 180
            if rotates[-2] == 'up':
                angle = 90
            if rotates[-2] == 'down':
                angle = -90
            if rotates[-2] != 'left':
                self.image = pygame.transform.rotate(self.image, angle)
                self.image.get_rect(center=self.rect.center)
            self.rect.x -= tile_width
            self.x = (self.x - 1) %(level_x + 1)
        elif event.key == pygame.K_UP and (level[(self.y - 1)%(level_y + 1)][self.x%(level_x + 1)] != '#'):
            rotates.append('up')
            direct += 'up'
            if rotates[-2] == 'right':
                angle = 90
            if rotates[-2] == 'down':
                angle = 180
            if rotates[-2] == 'left':
                angle = -90
            if rotates[-2] != 'up':
                self.image = pygame.transform.rotate(self.image, angle)
                self.image.get_rect(center=self.rect.center)
            self.rect.y -= tile_width
            self.y = (self.y - 1) % (level_y + 1) 
        elif event.key == pygame.K_DOWN and (level[(self.y + 1)%(level_y + 1)][self.x%(level_x + 1)] != '#'):
            rotates.append('down')
            direct += 'down'
            if rotates[-2] == 'right':
                angle = -90
            if rotates[-2] == 'up':
                angle = -180
            if rotates[-2] == 'left':
                angle = 90
            if rotates[-2] != 'down':
                self.image = pygame.transform.rotate(self.image, angle)
                self.image.get_rect(center=self.rect.center)
            self.y = (self.y + 1) % (level_y + 1)
            self.rect.y += tile_width
        self.direct = direct
        return self.x, self.y, self.direct
    
    def shoot(self, player_direct=None):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.rect.bottom, 
                        self.rect.left, self.rect.right, player_direct)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
# создание игры
class Game:
    def __init__(self, width, height, tile_size, tile_type, player_image, enemies_tanks):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.tile_width = tile_size
        self.tile_height = tile_size
        self.tile_images = tile_type
                
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.tile_wall = pygame.sprite.Group()
        self.bullets_enemie = pygame.sprite.Group()

        self.player = None
        self.player_image = player_image
        self.enemies_image = enemies_tanks
        self.x = 0
        self.y = 0
        self.level = None

    def get_screen(self):
        return self.screen
    
    def sprites_creation(self):
        return (self.all_sprites, self.tiles_group, self.player_group, self.bullets, 
                self.tanks, self.bullets_enemie, self.tile_wall)

    def load_level(self, filename):
        if filename:
            filename = "data/" + filename
        else:
            terminate()

        # читаем уровень, убирая символы перевода строки
        try:
            with open(filename, 'r') as mapFile:
                if mapFile:
                    level_map = [line.strip() for line in mapFile]
        except (FileNotFoundError, IOError):
            pass

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        level_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))

        return level_map
  
    def generate_level(self, level, tile_wall):
        new_player, x, y = None, None, None
                
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', self.tiles_group, self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                    
                elif level[y][x] == '#':
                    wall = Tile('wall', self.tiles_group,  self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                    all_sprites.add(wall)
                    tile_wall.add(wall)
                    
                elif level[y][x] == '$':
                    Tile('bushes', self.tiles_group,  self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                elif level[y][x] == '%':
                    Tile('grass', self.tiles_group,  self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                elif level[y][x] == '?':
                    Tile('empty', self.tiles_group,  self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                    tanks_enemies = Tanks(self.tanks, self.all_sprites,
                                        self.enemies_image,
                                        self.tile_width, self.tile_height,
                                        x, y, level)
                    
                elif level[y][x] == '@':
                    Tile('empty', self.tiles_group, self.all_sprites,
                         self.tile_images, self.tile_width, self.tile_height,
                         x, y)
                    new_player = Player(self.player_group, self.all_sprites,
                                        self.player_image,
                                        self.tile_width, self.tile_height,
                                        x, y)
                    
        #вернем игрока (размер поля в клетках в объекте game)
        self.x = x
        self.y = y
        self.player = new_player
        self.enemies = tanks_enemies
        self.level = level.copy()
        return new_player, tanks_enemies


class Bullet(pygame.sprite.Sprite):
    def __init__(self, centre, up, down, left, right, direct=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.image = tile_images['bullet']
        self.rect = self.image.get_rect()
        self.rect.bottom = down
        self.rect.top = up
        self.rect.left = left
        self.rect.right = right
        self.rect.centerx = centre
        self.direction = direction
        self.speedy = 10
        self.direct = direct

    def update(self):
        if self.direct == 'up':
            self.rect.y -= self.speedy
        if self.direct == 'down':
            self.rect.y += self.speedy
        if self.direct == 'left':
            self.rect.x -= self.speedy
        if self.direct == 'right':
            self.rect.x += self.speedy
        

class Bullet_enemie(pygame.sprite.Sprite):
    def __init__(self, centre, up, down, left, right, direct=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.image = tile_images['bullet']
        self.rect = self.image.get_rect()
        self.rect.bottom = down
        self.rect.top = up
        self.rect.left = left
        self.rect.right = right
        self.rect.centerx = centre
        self.speedy = 30
        for i in direct:
            if i:
                self.direct = i

    def update(self):
        try:
            if self.direct == 'up':
                self.image
                self.rect.y -= self.speedy
            if self.direct == 'down':
                self.rect.y += self.speedy
            if self.direct == 'left':
                self.rect.x -= self.speedy
            if self.direct == 'right':
                self.rect.x += self.speedy
        except AttributeError:
            pass


class Tanks(pygame.sprite.Sprite):
    def __init__(self, tanks, all_sprites, player_image,
                         tile_width, tile_height,
                         pos_x, pos_y, level):
        super().__init__(tanks, all_sprites)
        self.image = player_image
        self.level = level
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        
    def has_path(self, x1, y1, coords_player, game, rotates_enemies):
        self.level_x, self.level_y = game.x, game.y
        self.rotates_enemies = rotates_enemies
        self.result = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = coords_player[0][0]
        self.y2 = coords_player[0][1]
        
        
        def found(pathArr, finPoint):
            weight = 1
            for i in range(len(pathArr)*len(pathArr[0])):
                weight += 1 
                for y in range(len(pathArr)):          
                    for x in range(len(pathArr[y])):                   
                        if pathArr[y][x] == (weight - 1):            
                            if y > 0 and pathArr[y - 1][x] == 0:
                                pathArr[y - 1][x] = weight
                            if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                                pathArr[y + 1][x] = weight
                            if x > 0 and pathArr[y][x - 1] == 0:
                                pathArr[y][x - 1] = weight
                            if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                                pathArr[y][x + 1] = weight
                                    
                            if (abs(y-finPoint[0]) + abs(x-finPoint[1])) == 1:
                                pathArr[finPoint[0]][finPoint[1]] = weight
                                return True
            return False      
         
        def printPath(pathArr, finPoint):      
            y = finPoint[0]
            x = finPoint[1]
            weight = pathArr[y][x]
            result = list(range(weight))
            while (weight):
                weight -=1
                if y > 0 and pathArr[y - 1][x] == weight:
                    y -= 1
                    result[weight] = 'down' 
                elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
                    result[weight] = 'up' 
                    y += 1
                elif x > 0 and pathArr[y][x - 1] == weight:
                    result[weight] = 'right' 
                    x -= 1
                elif x < (len(pathArr[y]) - 1) and pathArr[y][x+1] == weight:
                    result[weight] = 'left' 
                    x += 1      
            return result[1:]
            
        def main():
            if coords_player:
                # Выход из лабиринта .Волновой алгоритм
                labirint = self.level_in_map(self.level)
                # 1 - это стена, 0 - это путь.
                # координаты входа
                pozIn =(y1, x1)
                pozOut=(self.y2, self.x2)
             
                path = [[x if x == 0 else -1 for x in y] for y in labirint]
                path[pozIn[0]][pozIn[1]] = 1; 
             
                if not found(path, pozOut):
                    return    
                self.result = printPath(path,pozOut)
                return self.result
            
            
        return main()
        
    def func(self, func=None, new_player=None, game=None, rotates_enemies=None):
        if func:
            return (self.has_path(self.x, self.y, new_player, game, rotates_enemies))
        
    def update(self, list_paths=None):
        if list_paths:
            if list_paths == 'right':
                self.x = (self.x + 1) % (self.level_x + 1)
            if list_paths == 'left':
                self.x = (self.x - 1) % (self.level_x + 1)
            if list_paths == 'up':
                self.y = (self.y - 1) % (self.level_y + 1) 
            if list_paths == 'down':
                self.y = (self.y + 1) % (self.level_y + 1)
                
    def update_move(self, list_paths):
        direct = ''
        if list_paths:
            if list_paths == 'right':
                direct += 'right'
                rotates_enemies.append('right')
                if rotates_enemies[-2] == 'left':
                    angle = -180
                if rotates_enemies[-2] == 'up':
                    angle = -90
                if rotates_enemies[-2] == 'down':
                    angle = 90
                if rotates_enemies[-2] != 'right':
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.image.get_rect(center=self.rect.center)
                self.rect.x += tile_width / 5

            if list_paths == 'left':
                direct += 'left'
                rotates_enemies.append('left')
                if rotates_enemies[-2] == 'right':
                    angle = 180
                if rotates_enemies[-2] == 'up':
                    angle = 90
                if rotates_enemies[-2] == 'down':
                    angle = -90
                if rotates_enemies[-2] != 'left':
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.image.get_rect(center=self.rect.center)
                self.rect.x -= tile_width / 5
            
            if list_paths == 'up':
                rotates_enemies.append('up')
                direct += 'up'
                if rotates_enemies[-2] == 'right':
                    angle = 90
                if rotates_enemies[-2] == 'down':
                    angle = 180
                if rotates_enemies[-2] == 'left':
                    angle = -90
                if rotates_enemies[-2] != 'up':
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.image.get_rect(center=self.rect.center)
                self.rect.y -= tile_width / 5
            
            if list_paths == 'down':
                rotates_enemies.append('down')
                direct += 'down'
                if rotates_enemies[-2] == 'right':
                    angle = -90
                if rotates_enemies[-2] == 'up':
                    angle = -180
                if rotates_enemies[-2] == 'left':
                    angle = 90
                if rotates_enemies[-2] != 'down':
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.image.get_rect(center=self.rect.center)
                self.rect.y += tile_width / 5
            return direct
        
    def level_in_map(self, level):
        list_map = []
        for i in self.level:
            list_map.append(i)
        for i in range(len(list_map)):
            try:
                list_map[i] = list_map[i].replace('#', '1')
                list_map[i] = list_map[i].replace('.', '0')
                list_map[i] = list_map[i].replace('?', '0')
                list_map[i] = list_map[i].replace('@', '0')
                list_map[i] = list_map[i].replace('$', '1')
                list_map[i] = list_map[i].replace('%', '0')
            except ValueError:
                pass
        list_map = [list(map(int, x)) for x in list_map]
        return list_map
    
    def shoot(self, player_direct=None):
        bullet = Bullet_enemie(self.rect.centerx, self.rect.top, self.rect.bottom, 
                        self.rect.left, self.rect.right, player_direct)
        all_sprites.add(bullet)
        bullets_enemie.add(bullet)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, game):
        tile_width = game.tile_width
        level_x, level_y = game.x, game.y
        obj.rect.x = (obj.rect.x + self.dx) % ((level_x + 1) * tile_width)
        obj.rect.y = (obj.rect.y + self.dy) % ((level_y + 1) * tile_width)

    # позиционировать камеру на объекте target
    def update(self, target, width, height):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

class Sprite_collision:
    def __init__(self, image, t_start):
        global run, game_res
        run = True
        game_res = 'is game'
        for j in image[3]:
            for i in image[4]:
                if j.rect.collidepoint(i.rect.center):
                    music('collide.mp3')
                    i.kill()
                    j.kill()
                    run = False
                    game_res = 'win'
                    list_info = [game_res, str(datetime.datetime.now()).split('.')[0], str(int(time.time() - t_start))]
                    cur.execute("INSERT INTO info (game, time, duration) VALUES (?, ?, ?)", list_info)
                    connection.commit()
                    connection.close()
                    
        for i in image[5]:
            for k in image[2]:
                if i.rect.collidepoint(k.rect.center):
                    music('collide.mp3')
                    i.kill()
                    k.kill()
                    run = False
                    game_res = 'lose'
                    list_info = [game_res, str(datetime.datetime.now()).split('.')[0], str(int(time.time() - t_start))]
                    cur.execute("INSERT INTO info (game, time, duration) VALUES (?, ?, ?)", list_info)
                    connection.commit()
                    connection.close()
                    
        for i in image[3]:
            for j in image[5]:
                if j.rect.collidepoint(i.rect.center):
                    music('wall.mp3')
                    i.kill()
                    j.kill()
                    
        for i in image[3]:
            for j in image[6]:
                if i.rect.collidepoint(j.rect.center):
                    music('wall.mp3')
                    i.kill()
        
        for i in image[5]:
            for j in image[6]:
                if i.rect.collidepoint(j.rect.center):
                    music('wall.mp3')
                    i.kill()
        if not run:
            self.stop_game(run, game_res)
            
    def stop_game(self, run, game_res):
        run, game_res
# Программа
# Создаем игру
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
size = width, height = 754, 550
tile_width = tile_height = 50
pygame.display.set_caption('Танчики 1990')

tile_images = {
    'wall': load_image('wall2.png'),
    'empty': load_image('earth.png'),
    'bullet': load_image('core.png'),
    'grass': load_image('grass.jpg'),
    'bushes': load_image('bushes.png')
}
player_image = load_image('tank.png')
enemies_tanks = load_image('tank.png')

game = Game(width, height, tile_width, tile_images, player_image, enemies_tanks)
screen = game.get_screen()
# Создаем спрайты и группы спрайтов
all_sprites, tiles_group, player_group, bullets, tanks_enemies, bullets_enemie, tile_wall = game.sprites_creation()

fon = 'fon.jpg'
func3 = True
while func3:
    try:
        level_map, difficulty_level, t_start = start_screen(game.screen, width, height, fon, clock)
        func3 = False
    except TypeError:
        pass
    except ValueError:
        pass

player, enemies = game.generate_level(game.load_level(level_map), tile_wall)

# Загружаем заставку

camera = Camera()

FPS = 100
running = True
direction = 'up'
direct_2 = ''
direct_enemie = ['up']
list_rotates = ['up', 'up']
rotates_enemies = ['up', 'up']
coords = []
path = 0
count = 0
num = 0
num2 = 0
func = True
direct_player = ['up']


def details_return():
    global game, screen, all_sprites, tiles_group, player_group, bullets, difficulty_level, t_start
    global tanks_enemies, bullets_enemie, tile_wall, level_map, player, enemies
    global running, direction, direct_2, direct_enemie
    global list_rotates, rotates_enemies, coords, path, count, num, num2, func, direct_player, FPS
    game = Game(width, height, tile_width, tile_images, player_image, enemies_tanks)
    func3 = True
    while func3:
        try:
            level_map, difficulty_level, t_start = start_screen(game.screen, width, height, fon, clock)
            func3 = False
        except ValueError:
            func3 = True
        except TypeError:
            func3 = True
    screen = game.get_screen()
    # Создаем спрайты и группы спрайтов
    all_sprites, tiles_group, player_group, bullets, tanks_enemies, bullets_enemie, tile_wall = game.sprites_creation()
    
    player, enemies = game.generate_level(game.load_level(level_map), tile_wall)
    FPS = 100
    running = True
    direction = 'up'
    direct_2 = ''
    direct_enemie = ['up']
    list_rotates = ['up', 'up']
    rotates_enemies = ['up', 'up']
    coords = []
    path = 0
    count = 0
    num = 0
    num2 = 0
    func = True
    direct_player = ['up']
    return (game, screen, all_sprites, tiles_group, player_group, level_map, bullets, difficulty_level, t_start,
            tanks_enemies, bullets_enemie, tile_wall, player, enemies, running, direction, direct_2, 
               direct_enemie, list_rotates, coords, path, count, num, num2, func, direct_player, FPS)

def start_game(running, direction, direct_2, 
               direct_enemie, list_rotates, coords, path, count, num, num2, func, direct_player, FPS,
               clock, size, width, height, tile_width, tile_height, tile_images, player_image, enemies_tanks, 
               game, screen, all_sprites, tiles_group, player_group, bullets, tanks_enemies, bullets_enemie, 
               tile_wall, level_map, difficulty_level, t_start, player, enemies):
    while running:
        if difficulty_level == 'Уровень 1':
            speed_shoot_player = 5
        if difficulty_level == 'Уровень 2':
            speed_shoot_player = 10
        if difficulty_level == 'Уровень 3':
            speed_shoot_player = 15
        if difficulty_level == 'Уровень 4':
            speed_shoot_player = 20
        if difficulty_level == 'Уровень 5':
            speed_shoot_player = 25
        if num2 % speed_shoot_player == 0:
            func_shoot = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                for player in player_group:
                    coords.clear()
                    x, y, direct = player.update(event, game, list_rotates)
                    direct_player.append(direct)
                    coords.append((x, y))
                    try:
                        if func:
                            path = enemies.func(running, coords, game, rotates_enemies)[0:-1]
                            count = 0
                            num = 0
                    except TypeError:
                        pass
                if event.key == pygame.K_SPACE:
                    for i in direct_player:
                        if i:
                            direct = i
                    if func_shoot:
                        player.shoot(direct)
                        func_shoot = False
        
        camera.update(player, width, height)
         
        for sprite in all_sprites:
            camera.apply(sprite, game)  
            
        try:
            if difficulty_level == 'Уровень 1':
                speed_shoot = 10
                speed_move = 0.05
            if difficulty_level == 'Уровень 2':
                speed_shoot = 10
                speed_move = 0.04
            if difficulty_level == 'Уровень 3':
                speed_shoot = 10
                speed_move = 0.03
            if difficulty_level == 'Уровень 4':
                speed_shoot = 10
                speed_move = 0.02
            if difficulty_level == 'Уровень 5':
                speed_shoot = 9
                speed_move = 0.01
            if count % speed_shoot == 0:
                direct_enemie.append(direct_2)
                if direct_2:
                    enemies.shoot(direct_enemie)
                direct_enemie.clear()
            if path:
                if count % 5 == 0:
                    if count != 0:
                        num += 1
                    enemies.update(path[num])
                if len(path) > num:
                    func = False
                    direct_2 = enemies.update_move(path[num])
                else:
                    func = True
                time.sleep(speed_move)
                
        except IndexError:
            pass
        
        Sprite_collision(game.sprites_creation(), t_start)
        screen.fill(pygame.Color("black"))
        tiles_group.draw(screen)
        tanks_enemies.draw(screen)
        player_group.draw(screen)
        bullets.draw(screen)
        bullets_enemie.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        bullets.update()
        bullets_enemie.update()
        if path:
            count += 1
            num2 += 1
        if not run:
            running = False         
            
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
    connection = sqlite3.connect("data/data.db")
    cur = connection.cursor()
    start_game(running, direction, direct_2, 
                   direct_enemie, list_rotates, coords, path, count, num, num2, func, direct_player, FPS, 
                   clock, size, width, height, tile_width, tile_height, tile_images, player_image, enemies_tanks, 
                   game, screen, all_sprites, tiles_group, player_group, bullets, tanks_enemies, bullets_enemie, 
                   tile_wall, level_map, difficulty_level, t_start, player, enemies)
    
    end_screen(game.screen, width, height, fon, clock, game_res)
    
    details_return()