import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        list = [[0 for i in range(self.cols)] for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    list[i][j] = random.randint(0, 1)
        return list

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        y, x = cell
        neig = [(x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y),
                (x + 1, y - 1)]
        spsos = []
        for x, y in neig:
            if 0 <= x < self.cols and 0 <= y < self.rows:
                spsos.append((x, y))
        return [self.curr_generation[yy][xx] for xx, yy in spsos]

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                if self.curr_generation[y][x] == 0:
                    if self.get_neighbours((y, x)).count(1) == 3:
                        next[y][x] = 1
                else:
                    if self.get_neighbours((y, x)).count(1) in [2, 3]:
                        next[y][x] = 1
                    else:
                        next[y][x] = 0
        return next

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            grid = [[int(i) for i in list(j)] for j in f.readlines()]
        rows = len(grid)
        cols = len(grid[0])
        game = GameOfLife((rows, cols))
        game.curr_generation = grid
        return game

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as f:
            for row in self.curr_generation:
                f.writelines([''.join([str(sim) for sim in row]), '\n'])