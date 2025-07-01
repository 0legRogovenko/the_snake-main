import pygame as pg
import random

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

# Цвета
BOARD_BACKGROUND_COLOR = (200, 200, 200)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость
SPEED = 20

# Настройка PyGame
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption(f'Для выхода нажмите Cmd + Q')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""
    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта (переопределяется в подклассах)."""
        pass


class Apple(GameObject):
    """Яблоко на игровом поле."""
    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка с логикой движения и роста."""
    def __init__(self):
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну ячейку вперёд."""
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x * GRID_SIZE) % SCREEN_WIDTH,
               (cur[1] + y * GRID_SIZE) % SCREEN_HEIGHT)

        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.__init__()

    def draw(self):
        """Отрисовывает змейку на экране."""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for pos in self.positions:
            rect = pg.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главная функция запуска игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
