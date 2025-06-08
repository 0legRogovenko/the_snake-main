from random import choice

import pygame as pg

# Константы размеров окна и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ORIGIN = (0, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (200, 200, 200)  # Светло-серый фон
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BLACK = (0, 0, 0)

# Все ячейки игрового поля
ALL_CELLS = (set((x * GRID_SIZE, y * GRID_SIZE)
                 for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)))

# Противоположные направления
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

# Скорость змейки
SPEED = 20

# Настройка окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка - Нажмите ESC для выхода')

# Настройка времени
clock = pg.time.Clock()

# Словарь для обработки направления
TURNS = {
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
}


class GameObject:
    """Базовый класс для игровых объектов, таких как змейка и яблоко."""

    def __init__(self, body_color=BLACK):  # Добавлен параметр body_color
        self.body_color = body_color
        self.position = ORIGIN

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку с заданной позицией
        и опциональным цветом.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для переопределения в подклассах."""


class Apple(GameObject):
    """Класс для яблока, которое собирает змейка."""

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока, избегая занятых ячеек."""
        self.position = choice(list(ALL_CELLS - set(occupied_positions)))

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки, движущейся по игровому полю."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление змейки, если оно допустимо."""
        if new_direction:
            if new_direction != OPPOSITE_DIRECTIONS[self.direction]:
                self.direction = new_direction

    def move(self, ate_apple=False):
        """Перемещает змейку в текущем направлении."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = self.positions.pop() if not ate_apple else None

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            self.draw_cell(position)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            snake.update_direction(
                TURNS.get((snake.direction, event.key), snake.direction))


def main():
    """Основная функция для запуска игры 'Змейка'."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        next_head = (
            (snake.get_head_position()[
             0] + snake.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (snake.get_head_position()[
             1] + snake.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

        ate_apple = next_head == apple.position

        snake.move(ate_apple=ate_apple)

        if ate_apple:
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
