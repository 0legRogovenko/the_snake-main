from random import randint

import pygame

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
SPEED = 20

# Инициализация PyGame:
pygame.init()

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов, таких как змейка и яблоко."""

    def __init__(self):
        self.body_color = (0, 0, 0)  # Цвет тела объекта
        self.position = (0, 0)  # Позиция объекта на игровом поле

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        # Метод для отрисовки объекта, должен быть переопределен
        # в наследниках
        pass


class Apple(GameObject):
    """Класс для яблока, которое змейка будет собирать."""

    def __init__(self):
        """
        Инициализирует объект, устанавливая цвет тела в APPLE_COLOR и начальную
        позицию (0, 0). Вызывает инициализатор суперкласса.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (0, 0)

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Рисует яблоко на игровом экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, которая будет двигаться по игровому полю."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки в начальное."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет направление движения змейки, если было задано новое
        направление.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Двигает змейку в текущем направлении, обновляя ее позицию.
        """
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (cur_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions = [new_head] + self.positions[:-1]

    def draw(self):
        """Отрисовывает змейку на игровом экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления игровым объектом (змейкой).
    """
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
    """Главная функция для запуска игры 'Змейка'."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()  # Создание змейки
    apple = Apple()  # Создание яблока
    apple.randomize_position()  # Установка случайной позиции для яблока

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)  # Обработка нажатий клавиш для управления змейкой
        snake.update_direction()  # Обновление направления движения змейки
        snake.move()  # Движение змейки

        # Проверка столкновения змейки с яблоком
        if snake.get_head_position() == apple.position:
            # Добавление нового сегмента к змейке
            snake.positions.append(snake.positions[-1])
            apple.randomize_position()  # Случайная позиция для нового яблока

        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана

        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки
        pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
