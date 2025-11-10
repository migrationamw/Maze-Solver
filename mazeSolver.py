import csv,os,time,sys,random

def get_maze(file):
    f = open(file,'r')
    reader = csv.reader(f)
    maze = []
    for line in reader:
        maze.append(line)
    return maze

def display_maze(m, path):
    m2 = m[:]
    for item in path:
        m2[item[0]][item[1]] = "."
    m2[path[-1][0]][path[-1][1]] = "M"
    
    draw = ""
    
    for row in m2:
        for item in row:
            item = str(item).replace("1","█")
            item = str(item).replace("2"," ")
            item = str(item).replace("0"," ")
            draw += item
        draw += "\n"
    print(draw)
   
def move(path, maze):
    time.sleep(0.3)
    cur = path[-1]
    display_maze(maze,path)
    possibilities = [(cur[0],cur[1] + 1),(cur[0],cur[1]- 1),(cur[0] + 1, cur[1]),(cur[0]-1, cur[1]) ]

    # create a different path each time
    random.shuffle(possibilities)
    
    for item in possibilities:
        if item[0] < 0 or item[1] < 0 or item[0] >= len(maze) or item[1] >= len(maze[0]):
            continue
        elif maze[item[0]][item[1]] in ["1","2"] :
            continue
        elif item in path:
            continue
        elif maze[item[0]][item[1]] == "B":
            path = path + (item,)
            display_maze(maze,path)
            input("Solution found! Press enter to finish")
            sys.exit()
        else:
            newpath = path + (item,)
            move(newpath, maze)
            maze[item[0]][item[1]] = "2"
            display_maze(maze,path)
            time.sleep(0.3)

def main():
    mazesList = []
    for i in range(len(os.listdir("mazes"))):
        mazesList.append(i + 1)     
    print("Choose maze:\n")
    for m in mazesList:
        print(f"Maze {m}:")
        mazeChoice = get_maze(f"mazes\\maze{m}.csv")
        display_maze(mazeChoice, ((1, 0),))
    
    while True:
        choice = int(input("Enter integer maze number to play: "))
        if 1 <= choice <= len(mazesList):
            maze = get_maze(f"mazes\\maze{choice}.csv")
            move(((1,0),), maze)
        else:
            print("Invalid Input. Enter an integer between 1 and " + len(mazesList))

main()