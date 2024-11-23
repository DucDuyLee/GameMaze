import tkinter as tk
from tkinter import messagebox
from Maze import *
import re
import time
from PIL import Image as PILImage, ImageTk
from Maze import *
from wallFollower import *
from aStar import *
from BFS import *
from dijkstra import *
from DFS import *
from ucs import *
from greedy import *

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Game")
        self.master.configure(bg="black")  # Chọn màu nền tùy chọn, ví dụ là màu trắng ("white")
        self.l1 = None
        self.l2 = None
        self.l3 = None

        # Đặt kích thước cửa sổ bằng kích thước của màn hình
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")

        # Tạo khung
        self.left_frame = tk.Frame(self.master, bg="gray")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Tạo hình ảnh từ file imageMaze.png và điều chỉnh kích thước
        original_image = PILImage.open("imageMaze.jpg")
        resized_image = original_image.resize((300, 300), resample=PILImage.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

        self.canvas = tk.Canvas(self.left_frame, width=300, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)  # Use grid instead of pack
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        # Tính kích thước đồng đều cho các nút
        button_width = 7

        self.label_coordinates = tk.Label(self.left_frame, text="Enter coordinates (e.g., '(10, 10), (15, 20)'):", font=("Arial", 12))
        self.label_coordinates.grid(row=1, column=0, pady=5, columnspan=2)  # Increase columnspan to 2

        self.entry_coordinates = tk.Entry(self.left_frame, width=50)  # Increase the width value
        self.entry_coordinates.grid(row=2, column=0, pady=10, columnspan=2)  # Increase columnspan to 2

        # Thêm ComboBox để chọn thuật toán
        algorithms = ["Wall Follower", "BFS", "DFS", "A*", "Greedy", "UCS", "Dijkstra"]
        self.algorithm_var = tk.StringVar(self.left_frame)
        self.algorithm_var.set(algorithms[0])  # Đặt giá trị mặc định
        self.algorithm_dropdown = tk.OptionMenu(self.left_frame, self.algorithm_var, *algorithms)
        self.algorithm_dropdown.config(width=20, font=("Arial", 18))
        self.algorithm_dropdown.grid(row=3, column=0, pady=15)

        # Tạo nút Play
        self.play_button = tk.Button(self.left_frame, text="Play", bg="blue", fg="white", font=("Arial", 24), width=button_width, command=self.play_maze)
        self.play_button.grid(row=4, column=0, pady=10, padx=(10, 0), sticky="w")  # Set sticky to "w"

        # Tạo nút Create
        self.create_button = tk.Button(self.left_frame, text="Create", bg="green", fg="white", font=("Arial", 24), width=button_width, command=self.create_maze)
        self.create_button.grid(row=5, column=0, pady=10, padx=(10, 0), sticky="w")  # Set padx and sticky to "w"
        
        # Tạo nút Pause
        self.pause_button = tk.Button(self.left_frame, text="Pause", bg="purple", fg="white", font=("Arial", 24), width=button_width, command=self.pause_maze)
        self.pause_button.grid(row=4, column=0, pady=10, padx=(180, 10), sticky="w")  # Set padx and sticky to "w"

        # Tạo nút Reset
        self.reset_button = tk.Button(self.left_frame, text="Reset", bg="orange", fg="white", font=("Arial", 24), width=button_width, command=self.reset_maze)
        self.reset_button.grid(row=5, column=0, pady=10, padx=(180, 10), sticky="w")  # Set padx and sticky to "w"
        
        # Tạo nút Quit
        self.quit_button = tk.Button(self.left_frame, text="Quit", bg="red", fg="white", font=("Arial", 24), width=button_width, command=self.confirm_quit)
        self.quit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=(90, 10), sticky="w")  # Set padx and sticky to "w"

    def play_maze(self):
        # Lấy tên thuật toán được chọn từ ComboBox
        algorithm_name = self.algorithm_var.get()
       
        # Tạo đối tượng thuật toán dựa trên tên
        if algorithm_name == "Wall Follower":
            a=agent(self.myMaze,shape='arrow',footprints=True)
            path=wallFollower(self.myMaze)
            self.myMaze.tracePath({a:path},delay = 30)
            result = self.run_algorithm_with_timing(wallFollower, self.myMaze)
            self.l1=textLabel(self.myMaze,'Wall Follower Path Length',len(path)+1)
            self.l2=textLabel(self.myMaze,'Time',result)

        elif algorithm_name == "A*":
            searchPath,aPath,fwdPath=aStar(self.myMaze)
            a=agent(self.myMaze,footprints=True,color=COLOR.blue,filled=True, shape = 'arrow')
            b=agent(self.myMaze,1,1,footprints=True,color=COLOR.yellow,filled=True,goal=(self.myMaze.rows,self.myMaze.cols) )
            c=agent(self.myMaze,footprints=True,color=COLOR.red, shape='arrow')
            self.myMaze.tracePath({a:searchPath},delay=30)
            self.myMaze.tracePath({b:aPath},delay=30)
            self.myMaze.tracePath({c:fwdPath},delay=30)
            result = self.run_algorithm_with_timing(aStar, self.myMaze)
            self.l1=textLabel(self.myMaze,'A Star Path Length',len(fwdPath)+1)
            self.l2=textLabel(self.myMaze,'A Star Search Length',len(searchPath))
            self.l3=textLabel(self.myMaze,'Time',result)

        elif algorithm_name == "BFS":
            bSearch,bfsPath,fwdPath=BFS(self.myMaze)
            a=agent(self.myMaze,footprints=True,shape='arrow',filled=True)
            b=agent(self.myMaze,1,1,footprints=True,color=COLOR.yellow,shape='square',filled=True,goal=(self.myMaze.rows,self.myMaze.cols))
            c=agent(self.myMaze,footprints=True,color=COLOR.red,shape='arrow',filled=False)
            self.myMaze.tracePath({a:bSearch},delay=30)
            self.myMaze.tracePath({b:bfsPath},delay=30)
            self.myMaze.tracePath({c:fwdPath},delay=30)
            result = self.run_algorithm_with_timing(BFS, self.myMaze)
            self.l1=textLabel(self.myMaze,'BFS Path Length',len(fwdPath)+1)
            self.l2=textLabel(self.myMaze,'BFS Search Length',len(bSearch))
            self.l3=textLabel(self.myMaze,'Time',result)
            
        elif algorithm_name == "Dijkstra":
            path,c=dijkstra(self.myMaze)
            self.l2=textLabel(self.myMaze,'Total Cost',c+1)
            a=agent(self.myMaze,shape = 'arrow',footprints=True)
            result = self.run_algorithm_with_timing(dijkstra, self.myMaze)
            self.myMaze.tracePath({a:path},delay = 30)
            self.l1=textLabel(self.myMaze,'Time',result)

        elif algorithm_name == "DFS":
            dSeacrh,dfsPath,fwdPath=DFS(self.myMaze) # (5,1) is Start Cell, Change that to any other valid cell
            a=agent(self.myMaze,footprints=True,shape='arrow',filled=True)
            b=agent(self.myMaze,1,1,footprints=True,color=COLOR.yellow,shape='square',filled=True,goal=(self.myMaze.rows,self.myMaze.cols))
            c=agent(self.myMaze,footprints=True,color=COLOR.red,shape='arrow',filled=False)
            self.myMaze.tracePath({a:dSeacrh}, delay = 30)
            self.myMaze.tracePath({b:dfsPath}, delay = 30)
            self.myMaze.tracePath({c:fwdPath}, delay = 30)
            result = self.run_algorithm_with_timing(DFS, self.myMaze)
            self.l1=textLabel(self.myMaze,'DFS Path Length',len(fwdPath)+1)
            self.l2=textLabel(self.myMaze,'DFS Search Length',len(dSeacrh))
            self.l3=textLabel(self.myMaze,'Time',result)

        elif algorithm_name == "UCS":
            searchPath, ucsPath, fwdPath = UCS(self.myMaze)
            a = agent(self.myMaze, footprints=True, color=COLOR.blue, filled=True, shape='arrow')
            b = agent(self.myMaze, 1, 1, footprints=True, color=COLOR.yellow, filled=True, goal=(self.myMaze.rows, self.myMaze.cols))
            c = agent(self.myMaze, footprints=True, color=COLOR.red,shape='arrow')
            self.myMaze.tracePath({a: searchPath}, delay=30 )
            self.myMaze.tracePath({b: ucsPath}, delay=30)
            self.myMaze.tracePath({c: fwdPath}, delay=30)
            result = self.run_algorithm_with_timing(UCS, self.myMaze)
            self.l1 = textLabel(self.myMaze, 'UCS Path Length', len(fwdPath) + 1)
            self.l2 = textLabel(self.myMaze, 'UCS Search Length', len(searchPath))
            self.l3 = textLabel(self.myMaze,'Time',result)

        elif algorithm_name == "Greedy":
            searchPath, aPath, fwdPath = greedy(self.myMaze)
            a = agent(self.myMaze, footprints=True, color=COLOR.blue, filled=True, shape='arrow')
            b = agent(self.myMaze, 1, 1, footprints=True, color=COLOR.yellow, filled=True, goal=(self.myMaze.rows, self.myMaze.cols))
            c = agent(self.myMaze, footprints=True, color=COLOR.red, shape = 'arrow')
            self.myMaze.tracePath({a: searchPath}, delay=30)
            self.myMaze.tracePath({b: aPath}, delay=30)
            self.myMaze.tracePath({c: fwdPath}, delay=30)
            result = self.run_algorithm_with_timing(greedy, self.myMaze)
            self.l1 = textLabel(self.myMaze, 'Greedy Path Length', len(fwdPath) + 1)
            self.l2 = textLabel(self.myMaze, 'Greedy Search Length', len(searchPath))
            self.l3 = textLabel(self.myMaze,'Time',result)

        self.myMaze.run()

    def create_maze(self, m=10, n=10):
        # Lấy giá trị từ ô nhập liệu
        coordinates_input = self.entry_coordinates.get()

        # Kiểm tra xem người dùng đã nhập gì vào ô không
        if not coordinates_input:
            messagebox.showerror("Invalid Input", "Please enter coordinates.")
        try:
            # Chuyển đổi chuỗi nhập liệu thành danh sách các cặp số nguyên
            coordinates_list = [tuple(map(int, pair.strip('()').split(','))) for pair in coordinates_input.split(')') if pair]

            # Kiểm tra xem danh sách có rỗng hay không
            if not coordinates_list:
                raise ValueError("Invalid format. Please enter coordinates in the format 'm, n'.")

            # Lấy giá trị m và n từ cặp đầu tiên
            m, n = coordinates_list[0]

            # Kiểm tra định dạng
            if not re.match(r'^\d+,\s*\d+$', coordinates_input):
                raise ValueError("Invalid format. Please enter coordinates in the format 'm, n'.")

            # Tạo mê cung với các tham số từ người dùng
            self.myMaze=maze(m,n)
            self.myMaze.CreateMaze()

        except ValueError as e:
            # Xử lý trường hợp nhập liệu không hợp lệ
            messagebox.showerror("Invalid Input", str(e))

    def reset_maze(self):
        if self.l1 is not None:
            self.l1.delete_label()
        if self.l2 is not None:
            self.l2.delete_label()
        if self.l3 is not None:
            self.l3.delete_label()

        self.myMaze.deleteAllAgents()
        maze._tracePathList = []  # Đảm bảo rằng biến tracePath được làm mới trước khi vẽ đường đi mới.
        
    def pause_maze(self):
        pass

    def run_algorithm_with_timing(self, algorithm_func, *args, **kwargs):
        start_time = time.time()
        result = algorithm_func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Algorithm took {elapsed_time:.5f} seconds to run.")
        
        # Trả về kết quả của thuật toán
        return elapsed_time

    def confirm_quit(self):
        # Hiển thị hộp thoại xác nhận trước khi thoát
        result = messagebox.askokcancel("Confirm Quit", "Are you sure you want to quit the game?")
        if result:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    maze_game = MazeGame(root)
    root.mainloop()