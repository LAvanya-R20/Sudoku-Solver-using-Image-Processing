import matplotlib.pyplot as plt

def sudoku(grid):
    def print_grid(g):
        for row_idx, row in enumerate(g):
            for col_idx, cell in enumerate(row):
                print(str(cell).replace("0", "."), end="")
                if col_idx in {2, 5}:
                    print("+", end="")
            print()
            if row_idx in {2, 5}:
                print("+" * 11)

    def candidates(position, grid):
        row = set(grid[position[0]])
        row |= {grid[i][position[1]] for i in range(9)}
        block = position[0] // 3, position[1] // 3
        for i in range(3):
            row |= set(grid[block[0] * 3 + i][block[1] * 3:(block[1] + 1) * 3])
        return set(range(1, 10)) - row

    def has_conflicts(line):
        elements = set(line) - {0}
        for elem in elements:
            if line.count(elem) != 1:
                return True
        return False

    def save_solution_as_image(solution, filename='sudoku_solution.png'):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis('off')

        for i in range(10):
            ax.plot([i, i], [0, 9], color='black', linewidth=2 if i % 3 == 0 else 1)
            ax.plot([0, 9], [i, i], color='black', linewidth=2 if i % 3 == 0 else 1)

        for row in range(9):
            for col in range(9):
                if solution[row][col] != 0:
                    ax.text(col + 0.5, 8.5 - row, str(solution[row][col]),
                            va='center', ha='center', fontsize=16)
        
        plt.savefig(filename)
        plt.close()
        print(f"Solution saved as {filename}")

    print_func = print
    print_grid(grid)

    grid_int = []
    empty_cells = []
    for row_idx, row in enumerate(grid):
        try:
            num_row = list(map(int, row))
        except:
            print_func("Row " + str(row_idx + 1) + " contains something other than a digit.")
            return
        if len(num_row) != 9:
            print_func("Row " + str(row_idx + 1) + " does not contain 9 digits.")
            return
        empty_cells += [[row_idx, i] for i in range(9) if num_row[i] == 0]
        grid_int.append(num_row)
    if row_idx != 8:
        print_func("The game contains " + str(row_idx + 1) + " rows instead of 9.")
        return

    for row in range(9):
        if has_conflicts(grid_int[row]):
            print_func("Row " + str(row + 1) + " is contradictory.")
            return
    for col in range(9):
        column = [grid_int[row][col] for row in range(9)]
        if has_conflicts(column):
            print_func("Column " + str(col + 1) + " is contradictory.")
            return
    for block_row in range(3):
        for block_col in range(3):
            block = []
            for i in range(3):
                block += grid_int[block_row * 3 + i][block_col * 3:(block_col + 1) * 3]
            if has_conflicts(block):
                print_func("Block (" + str(block_row + 1) + ";" + str(block_col + 1) + ") is contradictory.")
                return

    possible_values = [[] for i in empty_cells]
    current_cell = 0

    while current_cell < len(empty_cells):
        possible_values[current_cell] = candidates(empty_cells[current_cell], grid_int)
        try:
            while not possible_values[current_cell]:
                grid_int[empty_cells[current_cell][0]][empty_cells[current_cell][1]] = 0
                current_cell -= 1
        except:
            print_func("The sudoku has no solution.")
            return
        grid_int[empty_cells[current_cell][0]][empty_cells[current_cell][1]] = possible_values[current_cell].pop()
        current_cell += 1

    print_grid(grid_int)
    save_solution_as_image(grid_int)
    return grid_int
