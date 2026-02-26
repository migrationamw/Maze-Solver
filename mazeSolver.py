import csv, os, time, random, heapq, math
from collections import deque

class Maze:

    def __init__(self, mazeChoice: int):
        self.maze = self.getMaze(os.path.join("mazes", f"maze{mazeChoice}.csv"))
        self.mazeCopy = []
        for row in self.maze:
            self.mazeCopy.append(row[:])
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.start = (0, 0)
        self.end = (0, 0)
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == 'A':
                    self.start = (i, j)
                elif self.maze[i][j] == 'B':
                    self.end = (i, j)
        self.solutions = 0
        self.found = False
        self.sleepTime = 0.1

    def getMaze(self, file: str) -> list[list[int]]:
        with open(file, 'r') as f:  
            reader = csv.reader(f)
            maze = []
            for line in reader:
                maze.append(line)
            return maze

    def displayMaze(self, path: tuple[tuple[int, int]] = ()) -> None:
        m2 = []
        for row in self.maze:
            m2.append(row[:])

        # draw path
        if path:
            for p in path:
                m2[p[0]][p[1]] = '.'
            m2[path[-1][0]][path[-1][1]] = 'X'
        
        # draw A and B
        m2[self.start[0]][self.start[1]] = 'A'
        m2[self.end[0]][self.end[1]] = 'B'

        # draw maze
        draw = ""
        for row in m2:
            for item in row:
                item = str(item).replace('1','█')
                item = str(item).replace('2',' ')
                item = str(item).replace('0',' ')
                draw += item
            draw += "\n"
        print(draw)

    def displayMaze2(self, path: tuple[tuple[int, int]] = (), end: bool = False) -> None:
        m2 = []
        for row in self.maze:
            m2.append(row[:])

        # draw pathF
        if path:
            for p in path:
                m2[p[0]][p[1]] = '.'
            m2[path[-1][0]][path[-1][1]] = 'X'
        if end:
            m2[path[-1][0]][path[-1][1]] = '.'

        # draw A and B
        m2[self.start[0]][self.start[1]] = 'A'
        m2[self.end[0]][self.end[1]] = 'B'

        # draw maze
        draw = ""
        for row in m2:
            for item in row:
                item = str(item).replace('1','█')
                item = str(item).replace('2',' ')
                item = str(item).replace('3',' ')
                item = str(item).replace('0',' ')
                draw += item
            draw += "\n"
        print(draw)

    def bfsSolve(self) -> None:
        self.maze[self.start[0]][self.start[1]] = '2'
        queue = deque([(self.start, )])
        while queue:
            time.sleep(self.sleepTime)
            currPath = queue.popleft()
            currLocation = currPath[-1]
            self.displayMaze(currPath)
            if currLocation == self.end:
                self.maze = self.mazeCopy
                print("Solution found!\n")
                return
            nbrs = [(currLocation[0], currLocation[1] + 1), (currLocation[0] - 1, currLocation[1]), 
                    (currLocation[0], currLocation[1] - 1), (currLocation[0] + 1, currLocation[1])]
            random.shuffle(nbrs)
            for nbr in nbrs:
                if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                    continue
                elif self.maze[nbr[0]][nbr[1]] in {'1', '2'}:
                    continue
                self.maze[nbr[0]][nbr[1]] = '2'
                queue.append(currPath + (nbr, ))
        self.maze = self.mazeCopy

    def aStar(self) -> None:
        self.maze[self.start[0]][self.start[1]] = '2'
        queue = []
        heapq.heappush(queue, (math.sqrt((self.end[0] - self.start[0]) ** 2 + (self.end[1] - self.start[1]) ** 2), (self.start, )))
        while queue:
            time.sleep(self.sleepTime)
            currPath = heapq.heappop(queue)[1]
            currLocation = currPath[-1]
            self.displayMaze(currPath)
            if currLocation == self.end:
                self.maze = self.mazeCopy
                print("Solution found!\n")
                return
            nbrs = [(currLocation[0], currLocation[1] + 1), (currLocation[0] - 1, currLocation[1]), 
                    (currLocation[0], currLocation[1] - 1), (currLocation[0] + 1, currLocation[1])]
            random.shuffle(nbrs)
            for nbr in nbrs:
                if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                    continue
                elif self.maze[nbr[0]][nbr[1]] in {'1', '2'}:
                    continue
                self.maze[nbr[0]][nbr[1]] = '2'
                traveledDistance = len(currPath) - 1
                manhattanDistance = abs(self.end[0] - nbr[0]) + abs(self.end[1] - nbr[1])
                euclideanDistance = math.sqrt((self.end[0] - nbr[0]) ** 2 + (self.end[1] - nbr[1]) ** 2)
                heapq.heappush(queue, (1 + traveledDistance + manhattanDistance, currPath + (nbr, )))
        self.maze = self.mazeCopy

    def bidirectionalBFS(self) -> None:
        currStart = [(self.start, )]
        currEnd = [(self.end, )]
        while currStart and currEnd:
            if len(currStart) <= len(currEnd):
                nextStart = []
                for startPath in currStart:
                    time.sleep(self.sleepTime)
                    self.displayMaze2(startPath)
                    currStartLocation = startPath[-1]
                    if self.maze[currStartLocation[0]][currStartLocation[1]] == '3':
                        for endPath in currEnd:
                            if endPath[-2] == currStartLocation:
                                time.sleep(self.sleepTime)
                                self.displayMaze2(startPath + endPath[:-1])
                                time.sleep(self.sleepTime)
                                self.displayMaze2(startPath + endPath[:-1], True)
                                self.maze = self.mazeCopy
                                return
                    self.maze[currStartLocation[0]][currStartLocation[1]] = '2'
                    nbrs = [(currStartLocation[0], currStartLocation[1] + 1), (currStartLocation[0] - 1, currStartLocation[1]), 
                            (currStartLocation[0], currStartLocation[1] - 1), (currStartLocation[0] + 1, currStartLocation[1])]
                    random.shuffle(nbrs)
                    for nbr in nbrs:
                        if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                            continue
                        elif self.maze[nbr[0]][nbr[1]] in {'1', '2'}:
                            continue
                        contains = 0
                        for nextStartPath in nextStart:
                            if nextStartPath[-1] == nbr:
                                contains += 1
                                break
                        if contains == 0:
                            nextStart.append(startPath + (nbr, ))
                currStart = nextStart
            else:
                nextEnd = []
                for endPath in currEnd:
                    time.sleep(self.sleepTime)
                    self.displayMaze2(endPath)
                    currEndLocation = endPath[-1]
                    if self.maze[currEndLocation[0]][currEndLocation[1]] == '2':
                        for startPath in currStart:
                            if startPath[-2] == currEndLocation:
                                time.sleep(self.sleepTime)
                                self.displayMaze2(startPath[:-1] + endPath)
                                time.sleep(self.sleepTime)
                                self.displayMaze2(startPath[:-1] + endPath, True)
                                self.maze = self.mazeCopy
                                return
                    self.maze[currEndLocation[0]][currEndLocation[1]] = '3'
                    nbrs = [(currEndLocation[0], currEndLocation[1] + 1), (currEndLocation[0] - 1, currEndLocation[1]), 
                            (currEndLocation[0], currEndLocation[1] - 1), (currEndLocation[0] + 1, currEndLocation[1])]
                    random.shuffle(nbrs)
                    for nbr in nbrs:
                        if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                            continue
                        elif self.maze[nbr[0]][nbr[1]] in {'1', '3'}:
                            continue
                        contains = 0
                        for nextEndPath in nextEnd:
                            if nextEndPath[-1] == nbr:
                                contains += 1
                                break
                        if contains == 0:
                            nextEnd.append(endPath + (nbr, ))
                currEnd = nextEnd

    def dfsSolve(self, path: tuple[tuple[int, int], ...]) -> None:
        if self.found:
            return
        elif not path:
            path = (self.start, )
            self.maze[self.start[0]][self.start[1]] = '2'
        self.displayMaze(path)
        curr = path[-1]
        if curr == self.end:
            self.maze = self.mazeCopy
            self.found = True
            print("Solution found!\n")
            return
        nbrs = [(curr[0], curr[1] + 1), (curr[0] - 1, curr[1]), 
                (curr[0], curr[1] - 1), (curr[0] + 1, curr[1])]
        random.shuffle(nbrs)
        first = 0
        for nbr in nbrs:
            if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                continue
            elif self.maze[nbr[0]][nbr[1]] in {'1', '2'}:
                continue
            if first == 0:
                time.sleep(self.sleepTime)
                first += 1
            self.maze[nbr[0]][nbr[1]] = '2'
            self.dfsSolve(path + (nbr, ))
            if self.found:
                return
            self.displayMaze(path)
            time.sleep(self.sleepTime)
        if first == 0:
            time.sleep(self.sleepTime)

    def findTotalSolutions(self, path: tuple[tuple[int, int], ...]) -> None:
        if not path:
            path = (self.start, )
            self.maze[self.start[0]][self.start[1]] = '2'
            self.solutions = 0
        self.displayMaze(path)
        curr = path[-1]
        if curr == self.end:
            self.solutions += 1
            print("Solution Found! Total # of solutions: " + str(self.solutions) + "\n")
            # reset maze visited and not in path
            self.maze = self.mazeCopy
            for i, j in path:
                self.maze[i][j] = '2'
            time.sleep(self.sleepTime)
            return
        nbrs = [(curr[0], curr[1] + 1), (curr[0] - 1, curr[1]), 
                (curr[0], curr[1] - 1), (curr[0] + 1, curr[1])]
        random.shuffle(nbrs)
        first = 0
        for nbr in nbrs:
            if min(nbr) < 0 or nbr[0] == self.height or nbr[1] == self.width:
                continue
            elif self.maze[nbr[0]][nbr[1]] in {'1', '2'}:
                continue
            if first == 0:
                time.sleep(self.sleepTime)
                first += 1
            self.maze[nbr[0]][nbr[1]] = '2'
            self.findTotalSolutions(path + (nbr, ))
            self.maze[nbr[0]][nbr[1]] = '0'
            self.displayMaze(path)
            time.sleep(self.sleepTime)
        if first == 0:
            time.sleep(self.sleepTime)

def main():
    numMazes = len(os.listdir("mazes"))
    while True:
        print("Choose maze:\n")
        mazes = []
        for i in range(1, numMazes + 1):
            print(f"Maze {i}:")
            currMaze = Maze(i)
            currMaze.displayMaze()
            mazes.append(currMaze)
        # choose maze
        try:
            choice = int(input(f"Enter maze selection [1-{numMazes}]: "))
        except KeyboardInterrupt:
            print("\nProgram terminated by user\n")
            break
        except:
            print("Invalid Input. Enter an integer between 1 and " + str(numMazes) + "\n")
            continue
        
        if 1 <= choice <= numMazes:
            chosenMaze = mazes[choice - 1]
            print("")
            chosenMaze.displayMaze()
            print("How would you like to solve?")
            print("1. Breadth First Search")
            print("2. A* Breadth First Search")
            print("3. Bidirectional Breadth First Search")            
            print("4. Depth First Search")            
            print("5. Find total # of solutions")
            print("")            

            solve = input("Enter algorithm selection [1-5]: ")
            # choose to fully solve or find a solution
            if solve == '1':
                chosenMaze.bfsSolve()
                chosenMaze.maze = chosenMaze.mazeCopy
            elif solve == '2':
                chosenMaze.aStar()
                chosenMaze.maze = chosenMaze.mazeCopy
            elif solve == '3':
                chosenMaze.bidirectionalBFS()
                chosenMaze.maze = chosenMaze.mazeCopy
            elif solve == '4':
                chosenMaze.dfsSolve(())
                chosenMaze.found = False
                chosenMaze.maze = chosenMaze.mazeCopy
            elif solve == '5':
                chosenMaze.findTotalSolutions(())
                chosenMaze.maze = chosenMaze.mazeCopy
                print("Total possible solutions = " + str(chosenMaze.solutions))
            else:
                print("Invalid Input. Enter an integer between 1 and 5\n")
        else:
            print("Invalid Input. Enter an integer between 1 and " + str(numMazes) + "\n")

main()