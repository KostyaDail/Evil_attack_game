# Нападение нечисти
# Игрок должен ловить падающую нечисть, пока она не достигла земли

from superwires import games, color
import random

games.init(screen_width=1920, screen_height=1080, fps=50)


class Hero(games.Sprite):
    """
    Герой, который будет ловить нечисть.
    """
    image = games.load_image("images/hero.png")

    def __init__(self):
        """ Инициализирует объект Hero. И создает объект Text для отображения счета. """
        super(Hero, self).__init__(image=Hero.image,
                                   x=games.mouse.x,
                                   bottom=games.screen.height - 20)

        self.score = games.Text(value=0, size=100, color=color.white,
                                top=10, right=games.screen.width - 10)
        games.screen.add(self.score)

    def update(self):
        """ Передвигает объект по горизонтали в точку с абсциссой, как у указателя мыши. """
        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0

        if self.right > games.screen.width:
            self.right = games.screen.width

        self.check_catch()

    def check_catch(self):
        """ Проверяет, поймал ли игрок нечисть. """
        for ghost in self.overlapping_sprites:
            self.score.value += 10
            self.score.right = games.screen.width - 10
            ghost.handle_caught()


class Ghost(games.Sprite):
    """
    Нечисть, падающая на землю.
    """

    image = games.load_image("images/ghost.png")

    speed = 3

    def __init__(self, x, y=180):
        """ Инициализация объекта Ghost. """
        super(Ghost, self).__init__(image=Ghost.image,
                                    x=x, y=y,
                                    dy=Ghost.speed)

    def update(self):
        """ Проверяет, не коснулась ли нижняя кромка спрайта нижней границы экрана. """
        if self.bottom > games.screen.height:
            Ghost.dy = 0
            games.screen.clear()
            self.end_game()
            self.destroy()

    def handle_caught(self):
        """ Разрушает объект, пойманный игроком. """
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        self.destroy()

    def end_game(self):
        """ Завершает игру. """
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=10 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)
        sound = games.load_sound("sounds/Game_over.mp3")
        sound.play()


class Monster(games.Sprite):
    """
    Монстр, который, двигаясь влево-право, разбрасывает нечисть.
    """
    image = games.load_image("images/monster.png")
    VELOCITY_STEP = 1.05

    def __init__(self, y=160, speed=5, odds_change=100):
        """ Инициализирует объект Monster. """
        super(Monster, self).__init__(image=Monster.image,
                                      x=games.screen.width / 2,
                                      y=y,
                                      dx=speed)

        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        """ Определяет, надо ли сменить направление. """
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
            # увеличивает скорость нечисти
            self.dx *= Monster.VELOCITY_STEP
            Ghost.speed *= Monster.VELOCITY_STEP
        self.check_drop()

    def check_drop(self):
        """ Уменьшает интервал ожидания на единицу или сбрасывает очередную нечисть. """
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_ghost = Ghost(x=self.x)
            games.screen.add(new_ghost)

            # вне зависимость от скорости падения нечисти "зазор" между падающими объектами
            # принимается равным 30% каждого из них по высоте
            self.time_til_drop = int(new_ghost.height * 1.3 / Ghost.speed) + 1



class Explosion(games.Animation):
    """ Анимированный взрыв. """
    # загрузка звука взрыва
    sound = games.load_sound("sounds/explosion.mp3")
    # список картинок - имен файлов, последовательность которых образует анимированный взрыв
    images = ["images/explosion1.bmp",
              "images/explosion2.bmp",
              "images/explosion3.bmp",
              "images/explosion4.bmp",
              "images/explosion5.bmp",
              "images/explosion6.bmp",
              "images/explosion7.bmp",
              "images/explosion8.bmp",
              "images/explosion9.bmp"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x, y=y,
                                        repeat_interval=4, n_repeats=1,
                                        is_collideable=False)
        Explosion.sound.play()


def main():
    """ Игровой процесс. """
    wall_image = games.load_image("images/background.jpg", transparent=False)
    games.screen.background = wall_image

    sound = games.load_sound("sounds/sound_theme.mp3")
    sound.play(-1)

    the_monster = Monster()
    games.screen.add(the_monster)

    the_hero = Hero()
    games.screen.add(the_hero)

    games.mouse.is_visible = False

    games.screen.event_grab = True
    games.screen.mainloop()


# старт!
main()
