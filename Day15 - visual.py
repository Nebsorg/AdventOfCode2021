import os
import sys

import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict
import pygame


g_windowsWidth = 1440
g_windowsHeight = 960
g_grey_color = (127,127,127)
g_openNode = (55,55,55)
g_closeNode = (175, 175, 175)
g_currentNode = (255,0,0)
g_otherNode = (255,255,255)
g_boardScreenSize = 960


def print_maze(maze, x_sep, y_sep):
    width = len(maze[0])

    for y,line in enumerate(maze):
        prtLine = ''
        if y%y_sep == 0:
            print('-'*width)
        for x,val in enumerate(line):
            if x%x_sep == 0:
                prtLine += '|'
            prtLine += str(val)
        print(prtLine)

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


def isPositionInNodeListe(position, nodeListe):
    for node in nodeListe:
        if (node.position[0] == position[0]) and (node.position[1] == position[1]):
            return(True)
    return(False)

def print_maze_with_path(maze, path):
    for y in range(len(maze)):
        line = ''
        for x in range(len(maze[0])):
            if (x,y) in path:
                line += '#'
            else:
                line += str(maze[x][y])
        print(line)

def path_cost(path, maze):
    cost = 0
    for v in path[1:]:
        cost += maze[v[0]][v[1]]
    return(cost)

def astar(start, end, maze):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = set()
    closed_list = set()

    # Add the start node
    open_list.add(start_node)

    # Loop until you find the end or you explore all the open node
    while len(open_list) > 0:
        # Get the best node (with lower f)
        current_node = next(iter(open_list))
        for item in open_list:
            if item.f < current_node.f:
                current_node = item

        # Pop current off open list, add to closed list
        open_list.discard(current_node)
        closed_list.add(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate new open node
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure position is not already in a list
            if isPositionInNodeListe(node_position, open_list) or isPositionInNodeListe(node_position, closed_list):
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            ## g is the cost of the path since the start
            new_node.g = current_node.g + maze[node_position[0]][node_position[1]]
            ## h is the heuristique : it the supposed cost from this position to the end : take the minimum step : cost of 1
            new_node.h = 0
            ## f is the total cost for comparison
            new_node.f = new_node.g + new_node.h

            # Append
            open_list.add(new_node)
            #print("astar - adding {0} to open list - len Open list = {1} - len closed list = {2}".format(new_node.position, len(open_list), len(closed_list)))

            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            render(path, [], [], [])
    return ([])



def render(path, openNode, closeNode, currentNode):

    ## draw background
    color = g_grey_color
    pygame.draw.rect(g_screen, color, (0, 0, g_windowsWidth, g_windowsHeight))

    x_shift = int(g_boardScreenSize / g_width)
    y_shift = int(g_boardScreenSize / g_height)

    color = (0, 255, 0)
    # for i in range(g_width + 1):
    #     pygame.draw.line(g_screen, color, (i * x_shift, 0), (i * x_shift, g_boardScreenSize))
    # for i in range(g_height + 1):
    #     pygame.draw.line(g_screen, color, (0, i * y_shift), (g_boardScreenSize, i * y_shift))

    color = (0,0,0)
    pygame.draw.rect(g_screen, color, (0,0, x_shift, y_shift))
    pygame.draw.rect(g_screen, color, (g_width, g_height, x_shift, y_shift))

    for node in path:
        color = g_otherNode
        pygame.draw.rect(g_screen, color, (node[0] * x_shift, node[1] * y_shift, x_shift, y_shift))




    # ## Draw element:
    # for y in range(g_gridSize):
    #     for x in range(g_gridSize):
    #         if g_board[x][y] != 0:
    #             if g_board[x][y] == g_white_id:
    #                 color = g_white_color
    #                 whiteScore += 1
    #             else:
    #                 color = g_black_color
    #                 blackScore += 1
    #             pygame.draw.circle(g_screen, color, ((x+1)*shift-shift/2, (y+1)*shift-shift/2) , shift/2)
    #
    # ## Write current player :
    # if not g_must_skip:
    #     if g_currentPlayer == g_white_id:
    #         textsurface = myfont.render(f"A vous de jouer joueur Blanc !", False, g_white_color)
    #     else:
    #         textsurface = myfont.render(f"A vous de jouer joueur Noir !", False, g_black_color)
    # else:
    #     if g_currentPlayer == g_white_id:
    #         textsurface = myfont.render(f"Passez donc votre tour joueur Blanc !", False, g_white_color)
    #     else:
    #         textsurface = myfont.render(f"Passez donc votre tour joueur Noir !", False, g_black_color)
    #     g_screen.blit(g_skip_sprite, g_skipStart)
    # g_screen.blit(textsurface, g_turnCaptionStart)
    #
    # ## draw score :
    # textsurface = myfont.render(f"Blanc : {whiteScore}", False, g_white_color)
    # g_screen.blit(textsurface, g_whiteScoreStart)
    #
    # textsurface = myfont.render(f"Noir : {blackScore}", False, g_black_color)
    # g_screen.blit(textsurface, g_blackScoreStart)
    #
    #
    # ## Draw possible plays:
    # if len(g_possiblePlays) > 1:
    #     if g_possiblePlays[0] == g_white_id:
    #         color = (255,255,255)
    #     else:
    #         color = (0, 0, 0)
    #     for pos in g_possiblePlays[1:]:
    #         x = pos[0]
    #         y = pos[1]
    #         pygame.draw.circle(g_screen, color, ((x+1)*shift-shift/2, (y+1)*shift-shift/2) , shift/4)

    pygame.display.flip()
    pygame.event.pump()


def extendMaze(maze):
    ## extend existing column:
    for y in range(len(maze)):
        line = maze[y]
        lineSize = len(line)
        for i in range(1, 5):
            for x in range(lineSize):
                newVal = line[x] + i
                if newVal > 9:
                    newVal = newVal % 10 + 1
                line.append(newVal)
    # print_maze(maze,x_sep, y_sep)

    initialHeight = len(maze)
    ## extending line:
    for i in range(initialHeight * 4):
        line = maze[i]
        lineToAdd = []
        for x in range(len(line)):
            newVal = line[x] + 1
            if newVal > 9:
                newVal = newVal % 10 + 1
            lineToAdd.append(newVal)
        maze.append(lineToAdd)

def main():
    global g_screen
    global g_maze
    global g_height
    global g_width

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("--- Day 15: Chiton ---")

    # create a surface on screen
    g_screen = pygame.display.set_mode((g_windowsWidth, g_windowsHeight))
    pygame.font.init()
    global myfont
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    g_maze = []
    f = open(".\Day15.txt", "r")
    i = 0
    for line in f:
        l = [int(v) for v in line.rstrip()]
        g_maze.append(l)
    f.close()
    x_sep = len(g_maze[0])
    y_sep = len(g_maze)

    extendMaze(g_maze)
    print_maze(g_maze, x_sep, y_sep)

    g_height = len(g_maze)
    g_width = len(g_maze[0])

    render([], [], [], [])

    running = True
    # main loop
    path = []
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    print(f"Start Resolution")
                    path = astar((0, 0), (len(g_maze[0]) - 1, len(g_maze) - 1), g_maze)
                    cost = path_cost(path, g_maze)
                    end_time = datetime.now()

                    print(f"** First Star = {cost} - {(end_time - start_time)}")
                    pygame.event.clear()
                if event.key == pygame.K_DOWN:
                    pygame.event.clear()
        render(path, [], [], [])


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    print("--- Day 15: Chiton ---")
    #### Main
    start_time = datetime.now()

    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    main()

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

