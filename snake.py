"""Игра «Змейка» на Pygame.

Змейка проходит сквозь границы поля, растёт при поедании яблок
и сбрасывается в исходное состояние при столкновении с собой.
"""

from random import choice

import pygame

# Размеры игрового поля и ячеек.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета игровых объектов.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 20

# Настройка игрового окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=None):
        """Задаёт начальную позицию и цвет объекта."""
        self.position = (
            SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
            SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE,
        )
        self.body_color = body_color

    def draw(self):
        """Определяет интерфейс отрисовки объекта."""
        pass

    def draw_cell(self, position, color):
        """Рисует ячейку заданного цвета с границей."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое поедает змейка."""

    def __init__(self):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """Выбирает позицию, не занятую телом змейки."""
        occupied = set(snake_positions or ())
        free_cells = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied
        ]
        self.position = choice(free_cells) if free_cells else None

    def draw(self):
        """Рисует яблоко, если на поле есть свободная ячейка."""
        if self.position is not None:
            self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка, управляемая игроком."""

    def __init__(self):
        """Создаёт змейку с начальным направлением движения."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Применяет выбранное направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну ячейку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Рисует все сегменты змейки."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в исходное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает закрытие окна и нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP
            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() == apple.position:
            snake.length += 1

            if snake.last is not None:
                snake.positions.append(snake.last)
                snake.last = None

            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
