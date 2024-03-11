import tkinter as tk
from datetime import datetime

class WorkTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("XIE")

        self.date_label = tk.Label(master, text="", font=("Arial", 12), wraplength=300)
        self.date_label.pack()

        self.time_label = tk.Label(master, text="", font=("Arial", 14), wraplength=300)
        self.time_label.pack()

        self.start_button = tk.Button(master, text="Đếm thời gian", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Làm mới thời gian", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

        self.working = False
        self.start_time = None

        self.update_date()
        self.update_time()

    def update_date(self):
        weekday = self.get_weekday()
        current_date = datetime.now().strftime('%d/%m/%Y')
        self.date_label.config(text=f"{weekday} - {current_date}")
        self.master.after(1000, self.update_date)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        time_period = self.get_time_period()
        if self.working:
            elapsed_time = datetime.now() - self.start_time
            current_time = f"{current_time}\n{str(elapsed_time).split('.')[0]}"
        self.time_label.config(text=f"[ {time_period} ] {current_time}")
        self.master.after(1000, self.update_time)

    def start_timer(self):
        self.working = True
        self.start_time = datetime.now()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        self.working = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def get_time_period(self):
        current_hour = datetime.now().hour
        if 1 <= current_hour < 11:
            return "Buổi sáng"
        elif 11 <= current_hour < 13:
            return "Buổi trưa"
        elif 13 <= current_hour < 18:
            return "Buổi chiều"
        elif 18 <= current_hour < 22:
            return "Buổi tối"
        else:
            return "Đêm"

    def get_weekday(self):
        weekdays = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
        current_weekday_index = datetime.now().weekday()
        return weekdays[current_weekday_index]

root = tk.Tk()
app = WorkTimerApp(root)
root.mainloop()
