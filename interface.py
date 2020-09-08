import pygame
import argparse
import os
from tkinter import *
from tkinter import messagebox
from extract_colors import extract_colors

colors = {1: (0, 255, 0),  # green
          2: (0, 0, 255),  # blue
          3: (255, 255, 0),  # yellow
          4: (255, 69, 0),  # orange
          5: (255, 0, 0),  # red
          6: (255, 255, 255),  # white
          }

# construct parser
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to images of kubik rubik")
ap.add_argument("-s", "--size", type=int, required=True)
ap.add_argument("-d", "--debug", type=int, default=-1)
args = vars(ap.parse_args())

flag = args['debug'] > 0

pygame.font.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Cube:
    kubik_rubik = extract_colors(path=args['path'], size=args['size'], flag=flag)

    def __init__(self, channels, rows, cols, width, height, size):
        self.current = 0
        self.channels = channels
        self.size = size
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.edges = [
            [[Cell(colors[self.kubik_rubik[c, i, j]], i, j, width, height, size) for j in range(cols)] for i in
             range(rows)] for c in range(channels)]

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                self.edges[self.current][i][j].draw(win)

    def set_current(self, val):
        self.current = val

    def check_cube(self):
        if self.edges:
            return True
        else:
            return False


class Cell:
    margin = 10

    def __init__(self, color, row, col, width, height, size):
        self.color = color
        self.size = size
        self.row = row
        self.col = col
        self.width = width - (size + 1) * self.margin
        self.height = height - (size +1) * self.margin

    def draw(self, win):
        gap = self.width // self.size
        startX = self.col * gap + (self.col + 1) * self.margin
        startY = self.row * gap + (self.row + 1) * self.margin

        pygame.draw.rect(win, self.color, (startX, startY, gap, gap))


def redraw_win(win, kubik_rubik):
    win.fill((0, 0, 0))

    kubik_rubik.draw(win)


if __name__ == "__main__":
    kubik_rubik = Cube(6, args['size'], args['size'], 450, 450, args['size'])

    if not kubik_rubik.check_cube():
        window = Tk()
        window.wm_withdraw()
        messagebox.showerror("Error", "There are not all edges")
        window.destroy()
        window.quit()

    else:
        win = pygame.display.set_mode((450, 450))
        pygame.display.set_caption("Rubik")
        run = True
        value = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        value += 1
                        if value > 5:
                            value = 0
                        kubik_rubik.set_current(value)
                    if event.key == pygame.K_LEFT:
                        value -= 1
                        if value < 0:
                            value = 5

                        kubik_rubik.set_current(value)

            redraw_win(win, kubik_rubik)
            pygame.display.update()
