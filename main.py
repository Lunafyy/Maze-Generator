import pygame
import random
import time

class Maze(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.visited_cells = []

        pygame.init()
        self.screen = pygame.display.set_mode((self.width*20, self.height*20))
        pygame.display.flip()
        # self.screen = pygame.display.set_mode((800, 800))
        # pygame.draw.rect(self.screen, (0,255,0), (loc[0], loc[1], self.width, self.width))
        self.pygame_mainloop()

    def draw_gridlines(self):
        for y in range(self.height+1):     
            for x in range(self.width+1):
                pygame.draw.line(self.screen, (255,255,255), (0, y*20), (x*20, y*20))
                pygame.draw.line(self.screen, (255,255,255), (x*20, 0), (x*20, y*20))
        pygame.display.flip()

    def coord_to_block(self, x, y):
        return ((x-1)*20,(y-1)*20)

    def valid_neighbours(self, x, y):
        potential_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        potential_neighbours = list(filter(lambda x: x not in self.visited_cells, potential_neighbours))
        potential_neighbours = list(filter(lambda x: x[0] > 0 and x[0] <= self.width and x[1] > 0 and x[1] <= self.height, potential_neighbours))

        return potential_neighbours

    def find_orientation(self, aX, aY, bX, bY):
        if aX > bX:
            return 'left'
        elif aX < bX:
            return 'right'
        elif aY > bY:
            return 'up'
        elif aY < bY:
            return 'down'

    def block(self, cX, cY, orientation):
        x = 20
        y = 20
        if orientation == 'down':
            pygame.draw.rect(self.screen, (0,0,0), (cX+1, cY+1, x-1, y))
        elif orientation == 'right':
            pygame.draw.rect(self.screen, (0,0,0), (cX+1, cY+1, x, y-1))
        elif orientation == 'left':
            pygame.draw.rect(self.screen, (0,0,0), (cX, cY+1, x, y-1))
        elif orientation == 'up':
            pygame.draw.rect(self.screen, (0,0,0), (cX+1, cY-1, x-1, y))
        pygame.display.flip()

    def generate(self):
        t1 = time.time()
        current = (1, 1)
        stack = [current]
        self.visited_cells.append(current)
        while stack != []:
            neighbours = self.valid_neighbours(current[0], current[1])
            if neighbours == []:
                stack.pop()
                if stack == []:
                    break
                current = stack[-1]
            else:
                visiting = random.choice(neighbours)
                coord = self.coord_to_block(current[0], current[1])
                self.block(coord[0], coord[1], self.find_orientation(current[0], current[1], visiting[0], visiting[1]))
                current = visiting
                stack.append(visiting)
                self.visited_cells.append(visiting)
        self.visited_cells.clear()
        print(f"DONE! Took {round(time.time()-t1,2)}s")

    def pygame_mainloop(self):
        running = True
        self.draw_gridlines()
        # loc = self.coord_to_block(2, 2)
        # print(loc)
        # self.block(loc[0], loc[1], 'up')
        self.generate()
        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.draw_gridlines()
                        self.generate()
                    if event.key == pygame.K_s:
                        pygame.image.save(self.screen, "maze.png")

Maze(50, 50)