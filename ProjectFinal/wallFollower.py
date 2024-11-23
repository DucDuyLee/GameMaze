from Maze import maze,agent,COLOR,textLabel
# Hàm quay theo chiều kim đồng hồ (Rotate Clockwise)
def rotateClockwise():
    global direction
    keys = list(direction.keys())
    values = list(direction.values())
    # Lấy giá trị cuối cùng của danh sách và đặt lên đầu
    values_rotated = [values[-1]] + values[:-1]
    direction = dict(zip(keys, values_rotated))

# Hàm quay ngược chiều kim đồng hồ (Rotate Counterclockwise)
def rotateNotClockwise():
    global direction
    keys = list(direction.keys())
    values = list(direction.values())
    # Lấy giá trị đầu tiên của danh sách và đặt lên cuối
    values_rotated = values[1:] + [values[0]]
    direction = dict(zip(keys, values_rotated))

# Hàm di chuyển về phía trước dựa trên hướng hiện tại
def moveForward(cell):
    if direction['forward'] == 'E':
        return (cell[0], cell[1] + 1), 'E'
    if direction['forward'] == 'W':
        return (cell[0], cell[1] - 1), 'W'
    if direction['forward'] == 'N':
        return (cell[0] - 1, cell[1]), 'N'
    if direction['forward'] == 'S':
        return (cell[0] + 1, cell[1]), 'S'
    
#Hàm thực hiện thuật toán Wall Follower để tìm đường đi trong mê cung.
def wallFollower(m):
    global direction
    # Khởi tạo hướng của agent và ô hiện tại
    direction = {'forward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}
    currCell = (m.rows, m.cols)
    path = ''  # Chuỗi lưu đường đi

    while True:
        # Nếu đến đích (1, 1) thì thoát vòng lặp
        if currCell == (1, 1):
            break
        # Kiểm tra xem có bức tường bên trái của agent không. Nếu giá trị bằng 0, tức là không có bức tường
        if m.maze_map[currCell][direction['left']] == 0:
            # Trong trường hợp không có bức tường bên trái, kiểm tra xem có bức tường phía trước của robot không, nếu bằng không là không có
            if m.maze_map[currCell][direction['forward']] == 0:
                rotateClockwise()  # Quay theo chiều kim đồng hồ
            else:
                currCell, d = moveForward(currCell)
                path += d
        else:
            rotateNotClockwise()  # Quay ngược chiều kim đồng hồ
            currCell, d = moveForward(currCell)
            path += d

    # Loại bỏ các di chuyển không cần thiết (quay ngược lại)
    while 'EW' in path or 'WE' in path or 'NS' in path or 'SN' in path:
        path = path.replace('EW', '')
        path = path.replace('WE', '')
        path = path.replace('NS', '')
        path = path.replace('SN', '')
    
    return path
