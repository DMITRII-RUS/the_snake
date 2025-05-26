# Код файла the_snake.py
from random import choice, randint

import pygame

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 10

# Настройка игрового окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля.
pygame.display.set_caption('Змейка')

# Настройка времени.
clock = pygame.time.Clock()


class GameObject:
    """Класс, который описывает все объекты."""

    def __init__(self) -> None:
        """Инициализирующий метод."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод, который отрисовывает объекты."""
        pass


class Apple(GameObject):
    """Класс описывает яблоко и операции над ним."""

    def __init__(self, grid_busy=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(grid_busy)

    def randomize_position(self, grid_busy=None):
        """Метод устанавливает случайное положение яблока на игровом поле."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            # Проверяем условие, что рандомная ячейка не в ячейке со змейкой.
            if grid_busy is None or position not in grid_busy:
                return position

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает змейку и операции над ней."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.last = None
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
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
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след (последний сегмент)."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:  # Затирание последнего сегмента
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.last = None
        self.next_direction = None
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной метод. Описывает логику игры Змейка"""
    pygame.init()
    snake = Snake()
    apple = Apple(grid_busy=snake.positions)

    while True:
        clock.tick(SPEED)  # Установим скорость игры.
        screen.fill(BOARD_BACKGROUND_COLOR)  # Заполним фоновым цветом.
        handle_keys(snake)
        snake.update_direction()  # Обновляем директорию змейки.
        snake.move()  # Запускаем движение замейки.
        # Цикл ниже проверяет столкновение змейки с яблоком.
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Змейка прирастает на +1.
            apple.position = apple.randomize_position(snake.positions)
        # Цикл ниже проверяет столкновение змейки с собой.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)
        apple.draw()  # Отрисовываем яблоко.
        snake.draw()  # Отрисовываем змейку.
        pygame.display.update()    # Обновляем экран.


if __name__ == '__main__':
    main()
