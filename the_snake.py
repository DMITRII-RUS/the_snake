# Код файла the_snake.py
import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Координаты центра:
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Словарь для направления и клавиш:
DIRECTIONS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}


class GameObject:
    """Класс, который описывает все объекты."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        """Инициализирующий метод."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, который отрисовывает объекты."""
        raise NotImplementedError('Проверьте. Метод draw не реализован.')

    def draw_one_cell(self, position, color=None):
        """Метод отрисовывает одну ячейку на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color if color else self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывает яблоко и операции над ним."""

    def __init__(self,
                 position=SCREEN_CENTER,
                 body_color=APPLE_COLOR,
                 grid_busy=None):
        super().__init__(position, body_color)
        self.randomize_position(grid_busy)

    def randomize_position(self, grid_busy=None):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            # Проверяем условие, что рандомная ячейка не в ячейке со змейкой.
            if grid_busy is None or self.position not in grid_busy:
                break

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_one_cell(self.position)


class Snake(GameObject):
    """Класс описывает змейку и операции над ней."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(position, body_color)
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_snake_x, head_snake_y = self.get_head_position()
        dx, dy = self.direction  # Добавляются к текущим координатам головы.
        head_updated = ((head_snake_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                        (head_snake_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, head_updated)
        self.last = self.positions.pop()

    def growing(self):
        """Добавляет последний удалённый сегмент обратно в змейку."""
        if self.last:
            self.positions.append(self.last)
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след (последний сегмент)."""
        for position in self.positions:
            self.draw_one_cell(position)

        if self.last:  # Затирание последнего сегмента
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.last = None
        self.next_direction = None
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:  # Выходим из игры по нажатию Escape
                pg.quit()
                sys.exit()
            game_object.next_direction = DIRECTIONS.get(
                (game_object.direction, event.key), game_object.direction)


def main():
    """Основной метод. Описывает логику игры Змейка"""
    pg.init()
    snake = Snake()
    apple = Apple(grid_busy=snake.positions)

    while True:
        clock.tick(SPEED)  # Установим скорость игры.
        handle_keys(snake)
        snake.update_direction()  # Обновляем директорию змейки.
        snake.move()  # Запускаем движение замейки.
        # Цикл ниже проверяет столкновение змейки с яблоком.
        if snake.get_head_position() == apple.position:
            snake.growing()   # Возвращаем последний сегмент.
            apple.randomize_position(snake.positions)
        # Цикл ниже проверяет столкновение змейки с собой.
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)  # Заполним фоновым цветом.
            apple.randomize_position(snake.positions)
        apple.draw()  # Отрисовываем яблоко.
        snake.draw()  # Отрисовываем змейку.
        pg.display.update()    # Обновляем экран.


if __name__ == '__main__':
    main()
