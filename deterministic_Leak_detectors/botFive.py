import random
from helperMethod import CreateDetector, find_shortest_path, get_neighbors, outer_detection_cells

class bot5():
    
    def __init__(self, k,  getGrid, bot_pos, leakpos_1, leakpos_2):
        
        bot_5_grid = [row.copy() for row in getGrid]
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2
        self.SENSOR = 0 # sensing counter
        self.MOVES = 0 # MOVES counter
        self.innerGridCells = []
        self.k = k
        self.debug = 0
        self.task_for_bot5(bot_5_grid, bot_pos)
        
    def task_for_bot5(self, grid, bot_pos):
        t=0
        m=0
        outcell_dict = {}
        botpos = bot_pos
        detectionGrid = []
        type = True
        positive_cells = []
        negative_cells = []
        leak = 1
        while True:
            # botpos != self.leakpos_1 and botpos != self.leakpos_2
            
            if botpos == self.leakpos_1 and leak == 2:
                break
            if botpos == self.leakpos_2 and leak == 2:
                break
            if botpos == self.leakpos_1 and leak == 1:
                self.leakpos_1 = (99,99)
                leak+=1                
            if botpos == self.leakpos_2 and leak == 1:
                self.leakpos_2 = (99,99)
                leak+=1
                
            
            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, grid, botpos)

            # Print Layout
            if self.debug == 1:
                for x in grid:
                    print(''.join(x))
                print()
          
            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1
            if (self.leakpos_1 in detectionGrid) or (self.leakpos_2 in detectionGrid):
                if self.leakpos_1 in detectionGrid:
                    t+=1
                    if t == 1:
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_1 and (x,y) != self.leakpos_2:
                                grid[x][y] = "❌"
                
                if self.leakpos_2 in detectionGrid:
                    m+=1
                    if m == 1:
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_1 and (x,y) != self.leakpos_2:
                                grid[x][y] = "❌"
                      
                i,j = botpos
                neighbors = get_neighbors(0, grid, i,j)
                grid[i][j] = "✅"
                # print("neighbors", neighbors)
                if len(neighbors) != 0:
                    botpos = neighbors[random.randint(0,len(neighbors)-1)]
                    self.MOVES+=1 # UPDATE MOVES BOT POS
                else:
                    outcell_dict = {}
                    negative_cells = []
                    for x in range(len(grid)):
                        for y in range(len(grid)):
                            if grid[x][y] == "❌" or grid[x][y] == "🟥":
                                negative_cells.append((x,y))
                    for item in negative_cells:
                        l = find_shortest_path(2, grid ,1 ,botpos, item)
                        if l:
                            try:
                                l = int(l)
                                outcell_dict[item] = l  
                            except:
                                l = len(l)
                                outcell_dict[item] = l 
                    botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                    self.MOVES += (outcell_dict[botpos] + 1) # UPDATE MOVE BOT POS
                type = False    
            else:
                type = True



            if type:
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1 and (x,y) != self.leakpos_2:
                        grid[x][y] = "✅"
                        positive_cells.append((x,y))
                # If not then find the next position for the bot
                x_bot, y_bot = botpos
                outcell_dict = {}
                for item in outer_detection_cells(grid):
                    # From the botpos to all marked outer cell which has atleast one open cell - Running BFS and storng data
                    # into the dictionary with key = co-ordinates and values = length of the path
                    l = find_shortest_path(1, grid ,1 ,botpos, item)
                    if l:
                        # Try if the return value if -1 which means no path found from botpos to that item
                        try:
                            l = int(l)
                            outcell_dict[item] = l  
                        # Now, store the length of the BFS and increament the MOVES needed to reach teh cell
                        except:
                            l = len(l)
                            outcell_dict[item] = l 
                
                # Marked the visited cell - No Leak
                grid[x_bot][y_bot] = "✅"
                # Get the minimum positive distance from botpos to nearest the outerlayer of the detection grid from the dictionary
                botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                # Steps needed to get the Outlayer of the detection Grid
                # +1 is for to move to open cell form the outer layer of detection grid
                self.MOVES += (outcell_dict[botpos] + 1)
                botpos = self.get_open(grid, botpos)[0]
            
            
            # Distance changed from the current botpos, so assign dictionary value empty
            # outcell_dict = {}
            # Mark Last bot postion
            x_bot,y_bot = botpos
            grid[x_bot][y_bot] = "😀"
            
            
            
            # Print Layout
            if self.debug == 1:
                print(botpos, self.leakpos_1)
                for x in grid:
                    print(''.join(x))
                print()
            # print(self.MOVES, self.SENSOR)


    def get_open(self,  grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        # Open Cells
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌")]
