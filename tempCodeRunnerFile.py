    node_data = self.node_info_data.get(city, "Không có thông tin")
        
        info_text = f"Tên: {name_city_display[city]}\n"
        for key, value in node_data.items():
            info_text += f"{key}: {value}\n"
        
        self.info_var.set(info_text)
        
        lbl_info = ttk.Label(self.frame_menu, text='Thông tin', font=tkFont.Font(family="GoogleSans-Bold.otf", size=12, weight="bold"))
        lbl_info.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        
        lbl_info_val = tk.Text(self.frame_menu, height=10, width=40, wrap=tk.WORD)
        lbl_info_val.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        lbl_info_val.insert(tk.END, info_text)
        lbl_info_val.config(state=tk.DISABLED)