import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import numpy as np
import time
from PIL import Image, ImageTk
from search import *

thuduc_map = UndirectedGraph(dict(
    BinhChieu=dict(TamBinh=180, BinhPhuoc=374),
    TamBinh=dict(BinhPhuoc=234, TamPhu=108),
    BinhPhuoc=dict(TamPhu=210, AnLoiDong=208),
    TamPhu=dict(LinhTay=140, LinhDong=218, AnLoiDong=320),
    AnLoiDong=dict(LinhDong=291),
    LinhTay=dict(LinhTrung=235, LinhChieu=110, LinhDong=175),
    LinhDong=dict(TruongTho=170),
    LinhTrung=dict(LinhXuan=220, LinhChieu=206),
    LinhChieu=dict(BinhTho=108, TruongTho=210),
    TruongTho=dict(BinhTho=140)))

thuduc_map.locations = dict(
    BinhChieu=(190, 760), TamBinh=(240, 640), BinhPhuoc=(90, 440),
    TamPhu=(280, 540), AnLoiDong=(120, 240), LinhTay=(460, 560),
    LinhDong=(360, 430), LinhTrung=(700, 580), LinhXuan=(640, 760),
    LinhChieu=(510, 500), TruongTho=(480, 310), BinhTho=(550, 410)
)

name_city = dict(
    BinhChieu=(-80, 0), TamBinh=(20, -10), BinhPhuoc=(-80, 20),
    TamPhu=(0, -30), AnLoiDong=(20, 0), LinhTay=(-20, -20),
    LinhDong=(-35, 35), LinhTrung=(-90, -20), LinhXuan=(-80, 0),
    LinhChieu=(20, 10), TruongTho=(-90, 0), BinhTho=(5, -25)
)

name_city_display = {
    'BinhChieu': 'Bình Chiểu', 'TamBinh': 'Tam Bình', 'BinhPhuoc': 'Bình Phước',
    'TamPhu': 'Tam Phú', 'AnLoiDong': 'Bình Chánh', 'LinhTay': 'Linh Tây',
    'LinhDong': 'Linh Đông', 'LinhTrung': 'Linh Trung', 'LinhXuan': 'Linh Xuân',
    'LinhChieu': 'Linh Chiểu', 'TruongTho': 'Trường Thọ', 'BinhTho': 'Bình Thọ'
}

node_info = {
    'BinhChieu': {'size': '5.49km2', 'img': 'dest.png'},
    'TamBinh': {'size': '3.41km2', 'img': ''},
    'BinhTho': {'size': '1.08km2', 'img': 'dest.png'},
    'BinhPhuoc': {'size': '7.66km2', 'img': 'dest.png'},
    'TamPhu': {'size': '2.98km2', 'img': 'dest.png'},
    'AnLoiDong': {'size': '6.26km2', 'img': 'dest.png'},
    'LinhTay': {'size': '1.41km2', 'img': 'dest.png'},
    'LinhDong': {'size': '2.59km2', 'img': 'dest.png'},
    'LinhTrung': {'size': '6.81km2', 'img': 'dest.png'},
    'LinhChieu': {'size': '1.3km2', 'img': 'dest.png'},
    'TruongTho': {'size': '4.09km2', 'img': 'dest.png'},
    'LinhXuan': {'size': '3.825km2', 'img': 'dest.png'}
}

dict_neighbors = thuduc_map.graph_dict

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.start_image = tk.PhotoImage(file='start.png').subsample(2)
        self.dest_image = tk.PhotoImage(file='dest.png').subsample(2)
        image = Image.open("thuduc_map.png")
        resized_image = image.resize((1377, 918), Image.BILINEAR)   #810 540 scale 1.7     
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.title('Tìm đường đi ngắn nhất')
        self.geometry('970x580')
        
        # Vẽ bản đồ
        self.frame_map = tk.Frame(self)
        self.frame_map.grid(row=0, column=0)

        self.cvs_map = tk.Canvas(self.frame_map, width=800, height=572, relief=tk.SUNKEN, border=1)
        self.cvs_map.grid(row=0, column=0)
        
        self.ve_ban_do()
        self.ve_toa_do()

        # Vẽ frame menu
        self.start = 'BinhChieu'          
        self.dest = 'BinhTho'
        self.lst_path = None
        
        self.frame_menu = tk.LabelFrame(self)
        self.frame_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.N)

        lst_city = list(thuduc_map.locations.keys())
        lst_city_display = [name_city_display[city] for city in lst_city]

        lbl_start = ttk.Label(self.frame_menu, text='Xuất phát', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_start.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.combobox_style = ttk.Style()
        self.combobox_style.configure('regular_font', font=('GoogleSans-Regular', 10))

        self.cbo_start = ttk.Combobox(self.frame_menu, values=lst_city_display)
        self.cbo_start.set(name_city_display[self.start])
        self.cbo_start.bind("<<ComboboxSelected>>", self.cbo_start_click)
        self.cbo_start.grid(row=1, column=0, padx=5, pady=5)

        lbl_dest = ttk.Label(self.frame_menu, text='Đích đến', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_dest.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.cbo_dest = ttk.Combobox(self.frame_menu, values=lst_city_display)
        self.cbo_dest.set(name_city_display[self.dest])
        self.cbo_dest.bind("<<ComboboxSelected>>", self.cbo_dest_click)
        self.cbo_dest.grid(row=3, column=0, padx=5, pady=5)

        btn_direction = ttk.Button(self.frame_menu, text='Chỉ đường', command=self.btn_direction_click)
        btn_direction.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW)
        
        btn_run = ttk.Button(self.frame_menu, text='Chạy', command=self.btn_run_click)
        btn_run.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW)

        self.distance_var = tk.StringVar()
        lbl_distance = ttk.Label(self.frame_menu, text='Khoảng cách', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_distance.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_distance_val = ttk.Label(self.frame_menu, textvariable=self.distance_var)
        lbl_distance_val.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.info_var = tk.StringVar()
        self.info_area = tk.StringVar()
        self.info_img = tk.PhotoImage()        
        lbl_info = ttk.Label(self.frame_menu, text='Thông tin', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_info.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_val = ttk.Label(self.frame_menu, textvariable=None)
        lbl_info_val.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_area = ttk.Label(self.frame_menu, textvariable=None)
        lbl_info_area.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_img = ttk.Label(self.frame_menu, textvariable=None)
        lbl_info_img.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.menu_visible = True
        self.btn_toggle_menu = tk.Button(self, text="<", command=self.toggle_menu)
        self.btn_toggle_menu.grid(row=0, column=0, sticky=tk.E, padx=(0, 0))    
        

    def toggle_menu(self):
        if self.menu_visible:
            self.frame_menu.grid_forget()
            self.btn_toggle_menu.config(text=">")
            self.geometry('810x580')
            self.menu_visible = False
        else:
            self.frame_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.N)
            self.btn_toggle_menu.config(text="<")
            self.geometry('970x580')
            self.menu_visible = True

    def open_node_info(self, city):
        self.info_area.set(node_info[city]['size'])
        self.info_img = tk.PhotoImage(file=node_info[city]['img'])  
        self.info_var.set(name_city_display[city])
        lbl_info = ttk.Label(self.frame_menu, text='Thông tin', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_info.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_val = ttk.Label(self.frame_menu, textvariable=self.info_var)
        lbl_info_val.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_area = ttk.Label(self.frame_menu, textvariable=self.info_area)
        lbl_info_area.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_img = ttk.Label(self.frame_menu, textvariable=self.info_img)
        lbl_info_img.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)

    def ve_ban_do(self):
        self.cvs_map.create_image(400, 300, image=self.background_image, tags='background')
        for key, neighbors in thuduc_map.graph_dict.items():
            for neighbor in neighbors:
                x0, y0 = thuduc_map.locations[key]
                x1, y1 = thuduc_map.locations[neighbor]
                y0 = 800 - y0
                y1 = 800 - y1
                self.cvs_map.create_line(x0, y0, x1, y1, fill='#E59600', width=5)
                self.cvs_map.create_line(x0, y0, x1, y1, fill='#E5CE9E', width=4)

    def ve_toa_do(self):
        for key in thuduc_map.graph_dict:
            x0, y0 = thuduc_map.locations[key]
            y0 = 800 - y0
            node_id = self.cvs_map.create_oval(x0-5, y0-5, x0+5, y0+5, fill='blue', outline='black')
            
            self.cvs_map.tag_bind(node_id, "<Button-1>", lambda event, city=key: self.open_node_info(city))
            
            dx, dy = name_city[key]
            city_name = name_city_display[key]
            self.cvs_map.create_text(x0+dx, y0+dy, text=city_name, anchor=tk.W, font=tkFont.Font(family="GoogleSans-Bold.otf", size=10, weight="bold"))

    def cbo_start_click(self, *args):
        selected_display_name = self.cbo_start.get()
        for key, display_name in name_city_display.items():
            if display_name == selected_display_name:
                self.start = key
                break
        print("Thành phố bắt đầu là", self.start)

    def cbo_dest_click(self, *args):
        selected_display_name = self.cbo_dest.get()
        for key, display_name in name_city_display.items():
            if display_name == selected_display_name:
                self.dest = key
                break
        print("Thành phố đích là", self.dest)

    def btn_direction_click(self):
        self.cvs_map.delete(tk.ALL)
        self.ve_ban_do()
        self.ve_toa_do()

        thuduc_problem = GraphProblem(self.start, self.dest, thuduc_map)
        c = astar_search(thuduc_problem)

        self.lst_path = c.path()
        total_distance = c.path_cost * 10
        self.distance_var.set(f'{total_distance / 1000:.2f} km')

        for data in self.lst_path:
            print(name_city_display[data.state], end=' ')
        print()

        L = len(self.lst_path)
        for i in range(L - 1):
            city = self.lst_path[i].state
            x0, y0 = thuduc_map.locations[city]
            y0 = 800 - y0
            for neighbor in dict_neighbors[city]:
                if neighbor == self.lst_path[i + 1].state:
                    x1, y1 = thuduc_map.locations[neighbor]
                    y1 = 800 - y1
                    self.cvs_map.create_line(x0, y0, x1, y1, fill='gray', width=7, tags='path')

        x0, y0 = thuduc_map.locations[self.start]
        y0 = 800 - y0 - 15
        self.cvs_map.create_image(x0, y0, image=self.start_image, tags='start')

        x1, y1 = thuduc_map.locations[self.dest]
        y1 = 800 - y1 - 15
        self.cvs_map.create_image(x1, y1, image=self.dest_image, tags='dest')

        self.ve_toa_do()

    def draw_arrow(self, x0, y0, x1, y1, remaining_distance):
        angle = np.arctan2(y1 - y0, x1 - x0)
        arrow_length = 10
        arrow_width = 5

        x2 = x1 - arrow_length * np.cos(angle + np.pi / 6)
        y2 = y1 - arrow_length * np.sin(angle + np.pi / 6)
        x3 = x1 - arrow_length * np.cos(angle - np.pi / 6)
        y3 = y1 - arrow_length * np.sin(angle - np.pi / 6)

        self.cvs_map.create_polygon(x1, y1, x2, y2, x3, y3, fill='red', outline='black', tags='arrow')

        text = f'{remaining_distance:.0f} m'
        text_bbox = self.cvs_map.create_text(x1, y1 - 30, text=text, fill='black', tags='arrow')
        bbox = self.cvs_map.bbox(text_bbox)
        
        padding = 2
        rect_bbox = (bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding)
        self.cvs_map.create_rectangle(rect_bbox, fill='white', outline='black', tags='arrow')
        
        self.cvs_map.tag_raise(text_bbox)

    def btn_run_click(self):
        if not self.lst_path:
            return

        mypath = []
        L = len(self.lst_path)

        for i in range(L - 1):
            city = self.lst_path[i].state

            x0, y0 = thuduc_map.locations[city]
            y0 = 800 - y0

            if (x0, y0) not in mypath:
                mypath.append((x0, y0))

            for neighbor in dict_neighbors[city]:
                if neighbor == self.lst_path[i + 1].state:
                    x1, y1 = thuduc_map.locations[neighbor]
                    y1 = 800 - y1

                    if (x1, y1) not in mypath:
                        mypath.append((x1, y1))

        L = len(mypath)
        total_distance = sum(
            thuduc_map.graph_dict[self.lst_path[i].state][self.lst_path[i + 1].state] * 10
            for i in range(len(self.lst_path) - 1)
        )
        remaining_distance = total_distance

        for k in range(L - 1):
            x0, y0 = mypath[k]
            x1, y1 = mypath[k + 1]
            d1 = thuduc_map.graph_dict[self.lst_path[k].state][self.lst_path[k + 1].state] * 10
            N1 = 20  # Số lần chia nhỏ để di chuyển
            dt = 1.0 / N1

            for i in range(N1):
                t = i * dt
                x = x0 + (x1 - x0) * t
                y = y0 + (y1 - y0) * t

                self.cvs_map.delete('arrow')
                self.draw_arrow(x0, y0, x, y, remaining_distance)
                time.sleep(0.1)
                self.cvs_map.update()
                remaining_distance -= d1 * dt  # Cập nhật khoảng cách còn lại

            # Cập nhật vẽ mũi tên tại điểm đích
            self.cvs_map.delete('arrow')
            self.draw_arrow(x0, y0, x1, y1, remaining_distance)
            self.cvs_map.update()

        mypath = self.lst_path = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
