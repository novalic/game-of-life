import pygame
import random
import time


SCREEN_SQUARE_SIZE = 800
BLOCK_SIZE = 8
NUMBER_OF_BLOCKS = int(SCREEN_SQUARE_SIZE / BLOCK_SIZE)
MAX_NUMBER_OF_CELLS = int(NUMBER_OF_BLOCKS / random.choice([5, 6, 7, 8, 9, 10]))

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def initial_conditions():
    state = list()

    for position in range(0, NUMBER_OF_BLOCKS):
        max_number_of_cells = random.randint(0, MAX_NUMBER_OF_CELLS)
        row = [1] * max_number_of_cells + [0] * (NUMBER_OF_BLOCKS - max_number_of_cells)
        random.shuffle(row)
        state.insert(position, row)

    return state


def draw_state(current_state, display_screen):
    for row in range(0, NUMBER_OF_BLOCKS):
        matrix_i = row * BLOCK_SIZE

        for column in range(0, NUMBER_OF_BLOCKS):
            if current_state[row][column] == 0:
                color = BLACK
            else:
                color = (random.choice(range(0, 255)), random.choice(range(0, 255)), random.choice(range(0, 255)))

            matrix_j = column * BLOCK_SIZE
            pygame.draw.rect(display_screen, color, (matrix_i, matrix_j, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()


def calculate_next_state(old_state):
    def _neighbour_cell_count(_state, cell_row, cell_column):
        count = 0

        if cell_row - 1 >= 0:

            if _state[cell_row - 1][cell_column] == 1:
                count += 1

            if cell_column - 1 >= 0 and _state[cell_row - 1][cell_column - 1] == 1:
                count += 1

            if cell_column + 1 < NUMBER_OF_BLOCKS and _state[cell_row - 1][cell_column + 1] == 1:
                count += 1

        if cell_column - 1 >= 0 and _state[cell_row][cell_column - 1] == 1:
            count += 1

        if cell_column + 1 < NUMBER_OF_BLOCKS and _state[cell_row][cell_column + 1] == 1:
            count += 1

        if cell_row + 1 < NUMBER_OF_BLOCKS:

            if cell_column - 1 >= 0 and _state[cell_row + 1][cell_column - 1] == 1:
                count += 1

            if _state[cell_row + 1][cell_column] == 1:
                count += 1

            if cell_column + 1 < NUMBER_OF_BLOCKS and _state[cell_row + 1][cell_column + 1] == 1:
                count += 1

        return count

    new_state = list()

    for old_state_row_number in range(0, NUMBER_OF_BLOCKS):
        old_state_row = old_state[old_state_row_number]
        for old_state_column_number in range(0, NUMBER_OF_BLOCKS):
            alive_neighbour_cell_number = _neighbour_cell_count(
                old_state, old_state_row_number, old_state_column_number
            )
            if old_state_row[old_state_column_number] == 0 and alive_neighbour_cell_number == 3:
                _ = old_state_row.pop(old_state_column_number)
                old_state_row.insert(old_state_column_number, 1)

            if old_state_row[old_state_column_number] == 1:
                if alive_neighbour_cell_number not in (2, 3):
                    _ = old_state_row.pop(old_state_column_number)
                    old_state_row.insert(old_state_column_number, 0)

        new_state.append(old_state_row)

    return new_state


def main():
    screen = pygame.display.set_mode((SCREEN_SQUARE_SIZE, SCREEN_SQUARE_SIZE))
    screen.fill(BLACK)

    state = initial_conditions()

    game_on = True

    while game_on:
        draw_state(state, screen)
        state = calculate_next_state(state)
        time.sleep(0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

    pygame.quit()


if __name__ == '__main__':
    main()
