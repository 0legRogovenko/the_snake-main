from random import choice

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
ORIGIN = (0, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (200, 200, 200)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BLACK = (0, 0, 0)

# Центр поля
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Все ячейки игрового поля
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

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
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов, таких как змейка и яблоко."""

    def __init__(self, position=ORIGIN, body_color=BLACK):
        self.body_color = body_color
        self.position = position

    def draw_cell(self, position, color=None):
        """Рисует одну ячейку на экране по заданной позиции и цвету."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Рисует объект на экране. Должен быть переопределён в подклассах."""
        raise NotImplementedError(
            f'Класс {self.__class__.__name__} должен реализовать метод draw().'
        )


class Apple(GameObject):
    """Класс для яблока, которое собирает змейка."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока, избегая занятых ячеек."""
        self.position = choice(list(ALL_CELLS - set(occupied_positions)))

    def draw(self):
        """Рисует яблоко на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки, движущейся по игровому полю."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.length = 1
        self._ate_apple = False
        self._last_tail = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, если оно допустимо."""
        if (new_direction
                and new_direction != OPPOSITE_DIRECTIONS[self.direction]):
            self.direction = new_direction

    def move(self):
        """
        Двигает змейку на одну ячейку вперёд.
        Если съедено яблоко, хвост не удаляется.
        """
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if not self._ate_apple:
            self._last_tail = self.positions.pop()
        else:
            self._last_tail = None
        self._ate_apple = False

    def draw(self):
        """Рисует только голову и стирает хвост, если нужно."""
        self.draw_cell(self.positions[0])
        if self._last_tail:
            self.draw_cell(self._last_tail, color=BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """
    Обрабатывает события pygame и изменяет направление
    змейки по нажатию клавиш.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            if event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            if event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            if event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция запускает игровой цикл змейки."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        # Двигаем змейку
        snake.move()
        head = snake.get_head_position()
        # Проверка самоукуса
        if head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif head == apple.position:
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
