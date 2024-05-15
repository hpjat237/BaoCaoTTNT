    def ve_ban_do(self):
        for key, neighbors in thuduc_map.graph_dict.items():
            for neighbor in neighbors:
                x0, y0 = thuduc_map.locations[key]
                x1, y1 = thuduc_map.locations[neighbor]
                y0 = 800 - y0
                y1 = 800 - y1

                # Tính toán góc của line
                angle = degrees(atan2(y1 - y0, x1 - x0))

                # Vẽ line
                self.cvs_map.create_line(x0, y0, x1, y1, fill='gray')

                # Vẽ mũi tên chỉ hướng
                arrow_length = 10
                arrow_degrees = 20
                arrow1_x = x1 - arrow_length * cos(radians(angle + arrow_degrees))
                arrow1_y = y1 - arrow_length * sin(radians(angle + arrow_degrees))
                arrow2_x = x1 - arrow_length * cos(radians(angle - arrow_degrees))
                arrow2_y = y1 - arrow_length * sin(radians(angle - arrow_degrees))

                self.cvs_map.create_polygon(x1, y1, arrow1_x, arrow1_y, arrow2_x, arrow2_y, fill='gray', outline='gray')

        for key in thuduc_map.graph_dict:
            x0, y0 = thuduc_map.locations[key]
            y0 = 800 - y0
            self.cvs_map.create_oval(x0-5, y0-5, x0+5, y0+5, fill='blue', outline='blue')

            dx, dy = name_city[key]
            city_name = name_city_display[key]
            self.cvs_map.create_text(x0+dx, y0+dy, text=city_name, anchor=tk.W, font=tkFont.Font(family="GoogleSans-Bold.otf", size=10, weight="bold"))
