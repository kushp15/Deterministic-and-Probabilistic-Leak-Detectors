from collections import deque

temp_distance_dict = {}

# Creating an dection layout based on the current position of the Grid by co-ordinates..
def CreateDetector(k, grid, botpos):
    innerGridCells = []
    x_bot, y_bot = botpos
    detectorGridSize = (2*k + 1)
    halfSize = (detectorGridSize - 1) // 2
    x1 = x_bot - halfSize
    y1 = y_bot - halfSize
    for i in range(detectorGridSize):
        for j in range(detectorGridSize):
            # Calculate the coordinates of each cell in the inner grid
            inner_x = x1 + i
            inner_y = y1 + j
            # Check if the inner_x and inner_y are within the bounds of the size of the grid and not block cells
            if 0 <= inner_x < len(grid) and 0 <= inner_y < len(grid) and grid[inner_x][inner_y] != "⬛️":
                innerGridCells.append((inner_x, inner_y))
    return innerGridCells


def find_shortest_path(index, original_grid, bot_no, start, end):
    queue = deque([(start, [])])
    visited = set()
    visited_dfs = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            visited_dfs.add((x, y))
            for nx, ny in get_neighbors(index,original_grid, x, y):
                if is_valid_move_bot(original_grid, bot_no, nx, ny):
                    queue.append(((nx, ny), path + [(nx, ny)]))
            visited_dfs.remove((x, y))
    return -1

# Method for Outer safe cell
def outer_detection_cells(grid):
    outer_cells_list = []
    # 1) Get all the safe cells of the originalGrid
    outer_cells = [(i, j) for i in range(len(grid)) for j in range(len(grid)) if grid[i][j] == "✅"]
    for x, y in outer_cells:
        if is_outer_detection(grid, x, y):
            outer_cells_list.append((x, y))
    return outer_cells_list

# Helpers of Methods
def get_neighbors(index, grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    # index = 0 : for finding the neighbors of ' ❌ '  
    if index == 0:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and grid[nx][ny] != "⬜️" and (grid[nx][ny] == "❌" or grid[nx][ny] == "😀" or grid[nx][ny] == "🟥")]
    
    # index = 1 : for finding the neighbors of ' ✅ '
        # Used in Bot - 1 :- At..   
    if index == 1:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and (grid[nx][ny] == "✅" or grid[nx][ny] == "😀")]
    
    # index = 1 : for finding the neighbors not including the Block cells
        # Used in Bot - 2 :- At..
    if index == 2:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️"]


# Give the validity of the move for the BFS
def is_valid_move_bot(grid, bot_no, x, y):
    if bot_no == 1:
        return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[x][y] != "⬛️"
    if bot_no == 2:
        height = len(grid)
        width = len(grid[0])
        return 0 <= x < height and 0 <= y < width and \
               all(0 <= x + dx < height and 0 <= y + dy < width and grid[x + dx][y + dy] != "✅" for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)])

# This Out detection checks for the out cells of the detection Grid
def is_outer_detection(grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in neighbors:
        if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌"):
            return True
    return False


def out_cells_bot_2(k, grid):
    outercell_distance =  k + 1  # Twice the first detection grid
    temp = outer_detection_cells(grid)
    outermost_green_cell = []
    for (x,y) in temp:
        if  0 <= x < len(grid) and 0 <= y+outercell_distance < len(grid) and  (grid[x][y+outercell_distance] == "⬜️" or grid[x][y+outercell_distance] == "❌"):
            outermost_green_cell.append((x,y+outercell_distance))
        if  0 <= x-outercell_distance < len(grid) and 0 <= y < len(grid) and (grid[x-outercell_distance][y] == "⬜️" or grid[x-outercell_distance][y] == "❌"):
            outermost_green_cell.append((x-outercell_distance,y))
        if  0 <= x+outercell_distance < len(grid) and 0 <= y < len(grid) and (grid[x+outercell_distance][y] == "⬜️" or grid[x+outercell_distance][y] == "❌"):
            outermost_green_cell.append((x+outercell_distance,y))
        if  0 <= x < len(grid) and 0 <= y-outercell_distance < len(grid) and (grid[x][y-outercell_distance] == "⬜️" or grid[x][y-outercell_distance] == "❌"):
            outermost_green_cell.append((x,y-outercell_distance))
    result = []
    for (x,y) in outermost_green_cell:
        if is_valid_move_bot(grid, 2, x,y):
            result.append((x,y))
    return result


def find_min_distance_and_path(your_dict):
    min_distance = float('inf')  # Initialize with positive infinity to find the minimum
    min_distance_path = []

    for key, value in your_dict.items():
        distance, path = value
        if distance > 0 and distance < min_distance:
            min_distance = distance
            min_distance_path = path
            #min_distance_key = key

    return min_distance, min_distance_path


# returns shortest path from start location to each and every valid cell in the grid
# Dijkstra's algorithm
def all_distances_bfs(index, original_grid, bot_no, start):
    queue = deque([(start, 0)])
    distances = {start: 0}

    while queue:
        (x, y), current_distance = queue.popleft()

        for nx, ny in get_neighbors(index, original_grid, x, y):
            if is_valid_move_bot(original_grid, bot_no, nx, ny):
                new_distance = current_distance + 1

                if (nx, ny) not in distances or new_distance < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_distance
                    queue.append(((nx, ny), new_distance))

    return distances


def find_shortest_path_bot3(index, original_grid, bot_no, start, end):
    queue = deque([(start, [])])
    visited = set()
    visited_dfs = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            temp_distance_dict[end] = len(path)
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            visited_dfs.add((x, y))
            for nx, ny in get_neighbors(index,original_grid, x, y):
                if is_valid_move_bot(original_grid, bot_no, nx, ny):
                    queue.append(((nx, ny), path + [(nx, ny)]))
            visited_dfs.remove((x, y))
    return []


# P(beep in i | leak in j) = e^(-alpha(d-1))
def beep_in_i_given_leak_in_j(a, grid, start, end, distances):
    e = 2.71828
    result = 0
    d = distances.get(end, float('inf'))
    power = -1 * a * (d - 1)
    result = pow(e, power)
    return result


# P(beep not in i | leak in j) = 1 - e^(-alpha(d-1))
def no_beep_in_i_given_leak_in_j(a, grid, start, end, distances):
    return 1 - beep_in_i_given_leak_in_j(a, grid, start, end, distances)


# P(leak in j | beep not in i)
def prob_leak_given_no_beep(a, grid, cell_probability_dict, botpos, distances):
    denominator = 0
    for key, probability in cell_probability_dict.items():
        x, y = key
        if probability != 0:
            temp = (probability * no_beep_in_i_given_leak_in_j(a, grid, botpos, (x, y), distances))
            denominator += temp

    for key, probability in cell_probability_dict.items():
        x, y = key
        if probability != 0:
            cell_probability_dict[key] = ((probability * no_beep_in_i_given_leak_in_j(a, grid, botpos, (x, y), distances))
                                          / denominator)

    return cell_probability_dict


# P(leak in j | beep in i)
def prob_leak_given_beep(a, grid, cell_probability_dict, botpos, distances):
    denominator = 0
    for key, probability in cell_probability_dict.items():
        x, y = key
        if probability != 0:
            temp = (probability * beep_in_i_given_leak_in_j(a, grid, botpos, (x, y), distances))
            denominator += temp

    for key, probability in cell_probability_dict.items():
        x, y = key
        if probability != 0:
            cell_probability_dict[key] = ((probability * beep_in_i_given_leak_in_j(a, grid, botpos, (x, y), distances))
                                          / denominator)

    return cell_probability_dict


# P(leak in j | leak not in i) = P(leak in j)/(1 - P(leak in i))
def leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i):
    cell_probability_dict[botpos] = 0
    denominator = 1 - leak_in_i

    for key, probability in cell_probability_dict.items():
        if probability != 0:
            cell_probability_dict[key] = probability / denominator

    return cell_probability_dict
