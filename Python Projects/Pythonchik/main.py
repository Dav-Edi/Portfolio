import pygame as pg
import sys, operator, sqlite3, hashlib
from random import randrange

def G():
    pg.init()

    clock = pg.time.Clock()
    fps = 60

    pg.display.set_caption('Pythonchick')
    SIZE = 800
    sc = pg.display.set_mode([SIZE, SIZE])
    background = pg.image.load('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/background.png')
    background_rect = background.get_rect(bottomright=[SIZE, SIZE])

    font = pg.font.Font('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/gogono-cocoa-mochi-cyrillic.otf', 28)
    fontchat = pg.font.Font('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/gogono-cocoa-mochi-cyrillic.otf', 23)
    color1 = (150, 150, 150, 50)
    color2 = (0, 150, 0)
    color3 = (0, 250, 0)

    return clock, fps, SIZE, sc, background, background_rect, font, fontchat, color1, color2, color3

def registration():
    size = SIZE - 200

    registration_surface = pg.Surface([size, size], pg.SRCALPHA)
    registration_surface.fill(color1)

    tg = pg.image.load('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/tg.png')
    tg = pg.transform.scale(tg, (250, 250))
    registration_surface.blit(tg, tg.get_rect(center=(registration_surface.get_width()//2, 10+250//2)))

    able = 0
    active = 'black'

    nicknameLabel = 'Nickname: '
    nickname = ''
    input_nickname = font.render(nicknameLabel + nickname, 1, color2, active)
    rect_nickname = input_nickname.get_rect(center=[SIZE // 2, SIZE // 2])

    passwordLabel = 'Password: '
    password = ''
    input_password = font.render(passwordLabel, 1, color2, active)
    rect_password = input_nickname.get_rect(center=[SIZE // 2, SIZE // 2 + 50])

    while 1:
        sc.blit(background, background_rect)
        sc.blit(registration_surface, (100, 100))

        sc.blit(input_nickname, rect_nickname)
        sc.blit(input_password, rect_password)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if rect_nickname.collidepoint(event.pos):
                    able = 1
                elif rect_password.collidepoint(event.pos) or able == 2:
                    able = 2
                else:
                    able = 3
            if event.type == pg.KEYDOWN:
                if able == 1:
                    if event.key == pg.K_BACKSPACE or len(nickname) >= 10:
                        nickname = nickname[:-1]
                    elif event.key == pg.K_TAB or event.key == pg.K_RETURN:
                        able = 2
                    elif event.key != pg.K_BACKSPACE and event.key != pg.K_TAB and event.key != pg.K_RETURN:
                        nickname += event.unicode
                if able == 2:
                    if event.key == pg.K_BACKSPACE and password != '':
                        password = password[:-1]
                        passwordLabel = passwordLabel[:-1]
                    elif event.key == pg.K_RETURN and nickname != '' and password != '':
                        save_user(nickname, password, registration_surface)
                    elif event.key != pg.K_BACKSPACE and event.key != pg.K_TAB and event.key != pg.K_RETURN:
                        password += event.unicode
                        passwordLabel += '*'
        if able == 1:
            input_nickname = font.render(nicknameLabel + nickname, 1, active, color2)
            input_password = font.render(passwordLabel, 1, color2, active)
        elif able == 2:
            input_nickname = font.render(nicknameLabel + nickname, 1, color2, active)
            input_password = font.render(passwordLabel, 1, active, color2)
        else:
            input_nickname = font.render(nicknameLabel + nickname, 1, color2, active)
            input_password = font.render(passwordLabel, 1, color2, active)

        pg.display.flip()
        clock.tick(fps)

def sql():
    with sqlite3.connect("C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/data.db") as db:
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            nickname VARCHAR(10),
            password VARCHAR(10),
            score INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        db.commit()

def code(value):
    return hashlib.md5(value.encode()).hexdigest()

def start(nickname):
    size1 = SIZE - 200 - 150
    game_surface = pg.Surface([size1, size1], pg.SRCALPHA)
    game_surface.fill(color1)
    game(nickname, game_surface, size1)

def save_user(nickname, password, registration_surface):
    db = sqlite3.connect('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/data.db')
    cursor = db.cursor()

    db.create_function("code", 1, code)

    cursor.execute("SELECT nickname FROM users WHERE nickname = ?", [nickname])
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users(nickname, password) VALUES(?,code(?))", [nickname, password])
        db.commit()
        start(nickname)
    elif cursor.execute("SELECT password FROM users WHERE nickname = ?", [nickname]).fetchone()[0] != code(password):
        password_false = font.render('Password is not right!', 1, color2, 'black')
        password_false_rect = password_false.get_rect(center=[registration_surface.get_width() // 2, 400])
        registration_surface.blit(password_false, password_false_rect)
    else:
        start(nickname)

def save_score(nickname, score):
    with sqlite3.connect('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/data.db') as db:
        cursor = db.cursor()
        cursor.execute("UPDATE users SET score = ? WHERE nickname = ?", [max(score, cursor.execute("SELECT score FROM users WHERE nickname = ?", [nickname]).fetchone()[0]), nickname])
        db.commit()

def game(nickname, game_surface, size):
    size2w = SIZE - 450 - 150
    size2h = SIZE - 200 - 150
    size3w = SIZE - 100
    size3h = SIZE - 450 - 150

    top_surface = pg.Surface([size2w, size2h], pg.SRCALPHA)
    top_surface.fill(color1)
    chat_surface = pg.Surface([size3w, size3h], pg.SRCALPHA)
    chat_surface.fill(color1)

    db = sqlite3.connect('C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/data.db')
    cursor = db.cursor()

    score = 0
    best = font.render('ЛучшиЕ ИгрокИ', 1, color3)
    # ls = sorted(ls, key=operator.itemgetter(1), reverse=True)
    ls = cursor.execute("SELECT nickname, score FROM users").fetchall()
    ls = sorted(ls, key=operator.itemgetter(1), reverse=True)
    you = font.render('ТЫ', 1, color3)



    for i in range(len(ls)):
        if i <= 14:
            res = f"{i + 1}. {ls[i][0]} {ls[i][1]}"
            restext = font.render(res, 1, color2)
            top_surface.blit(restext, (5, 5 + i * 25))
        if ls[i][0] == nickname:
            res = f"{i + 1}. {ls[i][0]} {ls[i][1]}"
            restext = font.render(res, 1, color2)
            top_surface.blit(restext, (5, 410))
    top_surface.blit(you, you.get_rect(center=(200 // 2, 395)))

    donate = pg.image.load("C:/Users/edild/OneDrive/Рабочий стол/programs/Pythonchik/data/donate.png")
    donate = pg.transform.scale(donate, (200, 200))
    donate.set_colorkey('black')
    chat_surface.blit(donate, (2, 2))

    t1_1 = fontchat.render('Если тебе понравилась игра то,',1, color2)
    t1_2 = fontchat.render('ты можешь поддержать меня,',1, color2)
    t1_3 = fontchat.render('чтобы я мог и дальше создавать', 1, color2)
    t1_4 = fontchat.render('игры для тебя)',1, color2)
    t2_1 = fontchat.render('Этот QR-код переведет тебя на', 1, color2)
    t2_2 = fontchat.render('страницу, откуда ты',1, color2)
    t2_3 = fontchat.render('сможешь отправить мне чеканную монетку,', 1, color2)
    t2_4 = fontchat.render('чтобы я не умирал от голода ;)',1, color2)
    t = [t1_1, t1_2, t1_3, t1_4, t2_1, t2_2, t2_3, t2_4]
    for i in range(len(t)):
        chat_surface.blit(t[i], (205, 2 + i * 25))

    cellsize = 50
    x, y = randrange(50 + 200 + 50 + cellsize, SIZE - 50 - cellsize, cellsize), randrange(50 + cellsize,
                                                                                          50 + 450 - cellsize, cellsize)
    apple = randrange(50 + 200 + 50 + cellsize, SIZE - 50 - cellsize, cellsize), randrange(50 + cellsize,
                                                                                           50 + 450 - cellsize,
                                                                                           cellsize)
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    fps = 60
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    speed_count, snake_speed = 0, 7

    while 1:
        sc.blit(background, background_rect)
        sc.blit(top_surface, (50, 50))
        sc.blit(chat_surface, (50, 550))
        sc.blit(game_surface, [300, 50])

        sc.blit(best, best.get_rect(center=(50 + 200 // 2, 25)))

        score_label = font.render(f'score: {score}', 1, color3)
        score_rect = score_label.get_rect(topleft=[300, 10])
        sc.blit(score_label, score_rect)

        [pg.draw.rect(sc, color2, (i, j, cellsize - 1, cellsize - 1)) for i, j in snake]
        pg.draw.rect(sc, pg.Color('red'), (*apple, cellsize - 1, cellsize - 1))

        speed_count += 1
        if not speed_count % snake_speed:
            x += dx * cellsize
            y += dy * cellsize
            snake.append((x, y))
        snake = snake[-length:]

        if snake[-1] == apple:
            score += 1
            apple = randrange(50 + 200 + 50 + cellsize, SIZE - 50 - cellsize, cellsize), randrange(50 + cellsize,
                                                                                                   50 + 450 - cellsize,
                                                                                                   cellsize)
            length += 1
            snake_speed -= 1
            snake_speed = max(snake_speed, 4)

        if x > 700 or x < 300 or y > 450 or y < 50 or len(snake) != len(set(snake)):
            save_score(nickname, score)
            end = font.render('!GAME OVER?', 1, color3)
            end_rect = end.get_rect(center=(50 + 200 + 50 + 450 // 2, 50 + 450 // 2))
            restart = font.render("restart", 1, color3)
            restart_rect = restart.get_rect(center=(50 + 200 + 50 + 450 // 2, 50 + 450 // 2 + 50))
            sc.blit(end, end_rect)
            sc.blit(restart, restart_rect)
            pg.display.flip()
            while 1:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            game(nickname, game_surface, size)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if restart_rect.collidepoint(event.pos):
                            game(nickname, game_surface, size)


        pg.display.flip()
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        key = pg.key.get_pressed()
        if key[pg.K_w] or key[pg.K_UP]:
            if dirs['W']:
                dx, dy = 0, -1
                dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
        elif key[pg.K_s] or key[pg.K_DOWN]:
            if dirs['S']:
                dx, dy = 0, 1
                dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
        elif key[pg.K_a] or key[pg.K_LEFT]:
            if dirs['A']:
                dx, dy = -1, 0
                dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
        elif key[pg.K_d] or key[pg.K_RIGHT]:
            if dirs['D']:
                dx, dy = 1, 0
                dirs = {'W': True, 'S': True, 'A': False, 'D': True, }

if __name__ == '__main__':
    clock, fps, SIZE, sc, background, background_rect, font, fontchat, color1, color2, color3 = G()

    sql()
    registration()
