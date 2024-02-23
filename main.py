import tkinter as tk
from copy import deepcopy


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Wave Alg")

        self.size_in_cells = 18
        self.grid_size = 40

        self.size = self.size_in_cells * self.grid_size
        self.cells = None
        self.bg_color = "white"
        self.wall_color = "black"
        self.exit_color = "orange"
        self.enter_color = "blue"
        self.path_color = "lightgreen"
        self.wall_symb = "#"
        self.space_symb = " "
        self.exit_symb = "X"
        self.enter_symb = 0



        self.enter_coords = (0, 0)
        self.exit_coords = None
        self.canvas = tk.Canvas(root, width=self.size_in_cells*self.grid_size, height=self.size_in_cells*self.grid_size, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid()
        self.draw_enter()
        self.set_empty_cells()

        self.canvas.bind("<B1-Motion>", self.draw_wall)
        self.canvas.bind("<Button-3>", self.draw_exit)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.alg_button = tk.Button(root, text="Find a way", command=self.wave_algorithm)
        self.alg_button.pack(side=tk.BOTTOM)
        self.clear_button.pack(side=tk.BOTTOM)

    def set_empty_cells(self):
        self.cells = [[self.space_symb for x in range(self.size_in_cells)] for y in range(self.size_in_cells)]
        self.cells[self.enter_coords[1]][self.enter_coords[0]] = self.enter_symb
        self.exit_coords = None

    def draw_grid(self):
        for i in range(0, self.size, self.grid_size):
            self.canvas.create_line(i, 0, i, self.size, fill=self.wall_color)
            self.canvas.create_line(0, i, self.size, i, fill=self.wall_color)


    def draw_enter(self):
        x, y = self.enter_coords
        self.draw_rectangular(x, y, self.enter_color)


    def get_coords(self, x, y):
        x_index = int(x//self.grid_size)
        y_index = int(y//self.grid_size)

        if 0 > x_index or x_index > self.size_in_cells - 1:
            return None

        if 0 > y_index or y_index > self.size_in_cells - 1:
            return None

        if (x_index, y_index) == self.enter_coords:
            return None

        return x_index, y_index

    def draw_rectangular(self, x, y, color):
        self.canvas.create_rectangle(x * self.grid_size,
                                     y * self.grid_size,
                                     (x + 1) * self.grid_size,
                                     (y + 1) * self.grid_size,
                                     fill=color)

    def draw_wall(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        try:
            x, y = self.get_coords(x, y)
        except TypeError:
            return

        if (x, y) == self.exit_coords:
            self.exit_coords = None

        self.cells[y][x] = self.wall_symb
        self.draw_rectangular(x, y, self.wall_color)

    def draw_exit(self, event):
        if event.num != 3:
            return


        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        try:
            x, y = self.get_coords(x, y)
        except TypeError:
            return

        if not self.exit_coords is None:
            self.draw_rectangular(*self.exit_coords, self.bg_color)
            self.cells[self.exit_coords[1]][self.exit_coords[0]] = self.space_symb

        self.exit_coords = (x, y)
        self.cells[y][x] = self.exit_symb
        self.draw_rectangular(x, y, self.exit_color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_enter()
        self.set_empty_cells()


    def check_coords(self, x, y):
        return  (0 <= y < self.size_in_cells) and (0 <= x < self.size_in_cells)


    def draw_way_out(self, cells, step):
        exit_coords = self.exit_coords
        cur_x, cur_y = exit_coords
        while True:
            if step == 1:
                break
            x = cur_x
            y = cur_y - 1
            if self.check_coords(x, y):
                if cells[y][x] == step - 1:
                    self.draw_rectangular(x, y, self.path_color)
                    step -= 1
                    cur_x = x
                    cur_y = y
                    continue

            x = cur_x - 1
            y = cur_y
            if self.check_coords(x, y):
                if cells[y][x] == step - 1:
                    self.draw_rectangular(x, y, self.path_color)
                    step -= 1
                    cur_x = x
                    cur_y = y
                    continue

            x = cur_x
            y = cur_y + 1
            if self.check_coords(x, y):
                if cells[y][x] == step - 1:
                    self.draw_rectangular(x, y, self.path_color)
                    step -= 1
                    cur_x = x
                    cur_y = y
                    continue

            x = cur_x + 1
            y = cur_y
            if self.check_coords(x, y):
                if cells[y][x] == step - 1:
                    self.draw_rectangular(x, y, self.path_color)
                    step -= 1
                    cur_x = x
                    cur_y = y
                    continue




    def wave_algorithm_step(self, cells, step):
        changed = False
        for line_num in range(len(cells)):
            line = cells[line_num]
            for cell_num in range(len(line)):
                cell = line[cell_num]
                if cell == step:
                    # y = line_num
                    # x = cell_num

                    y = line_num + 1
                    x = cell_num
                    if self.check_coords(x, y):
                        if cells[y][x] == self.exit_symb:
                            cells[y][x] = step + 1
                            return step + 1


                    y = line_num - 1
                    x = cell_num
                    if self.check_coords(x, y):
                        if cells[y][x] == self.exit_symb:
                            cells[y][x] = step + 1
                            return step + 1

                    y = line_num
                    x = cell_num - 1
                    if self.check_coords(x, y):
                        if cells[y][x] == self.exit_symb:
                            cells[y][x] = step + 1
                            return step + 1

                    y = line_num
                    x = cell_num + 1
                    if self.check_coords(x, y):
                        if cells[y][x] == self.exit_symb:
                            cells[y][x] = step + 1
                            return step + 1



                    y = line_num - 1
                    x = cell_num
                    if self.check_coords(x, y):
                        if cells[y][x] == self.space_symb:
                            cells[y][x] = step + 1
                            changed = True

                    y = line_num + 1
                    x = cell_num
                    if self.check_coords(x, y):
                        if cells[y][x] == self.space_symb:
                            cells[y][x] = step + 1
                            changed = True

                    y = line_num
                    x = cell_num + 1
                    if self.check_coords(x, y):
                        if cells[y][x] == self.space_symb:
                            cells[y][x] = step + 1
                            changed = True
                    y = line_num
                    x = cell_num - 1
                    if self.check_coords(x, y):
                        if cells[y][x] == self.space_symb:
                            cells[y][x] = step + 1
                            changed = True

        return changed

    def wave_algorithm(self):
        cells = deepcopy(self.cells)
        exit_coords = self.exit_coords

        if exit_coords == None:
            return

        step = 0
        while True:
            result = self.wave_algorithm_step(cells, step)
            if result is True:
                step += 1
                continue
            elif result is False:
                return

            self.draw_way_out(cells, result)
            break







def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
