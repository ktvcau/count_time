from datetime import datetime
import tkinter as tk
import platform
import psutil
import socket
import speedtest
import requests
import time

class WorkTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("XIE")
        self.master.geometry("300x200")
        self.master.configure(bg="black")
        
        self.date_label = tk.Label(master, text="", font=("Courier", 12), fg="purple", bg="black", wraplength=300)
        self.date_label.pack()

        self.time_label = tk.Label(master, text="", font=("Courier", 14), fg="cyan", bg="black", wraplength=300)
        self.time_label.pack()

        button_colors = {
            "start": {"bg": "#FF6347", "fg": "white"},
            "stop": {"bg": "#1E90FF", "fg": "#FF69B4"},
            "close": {"bg": "white", "fg": "black"}
        }
     
        self.start_button = tk.Button(master, text="Start Timer", command=self.start_timer, relief=tk.FLAT, **button_colors["start"])
        self.start_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        self.stop_button = tk.Button(master, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED, relief=tk.FLAT, **button_colors["stop"])
        self.stop_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

        self.close_button = tk.Button(master, text="Close App", command=self.close_app, relief=tk.FLAT, **button_colors["close"])
        self.close_button.pack(pady=10)

        self.working = False
        self.start_time = None

        self.update_date()
        self.update_time()

    def update_date(self):
        """Update ngày hiện tại."""
        weekday = self.get_weekday()
        current_date = datetime.now().strftime('%d/%m/%Y')
        self.date_label.config(text=f"{weekday} - {current_date}")
        self.master.after(1000, self.update_date)

    def update_time(self):
        """Update thời gian hiện tại và thời gian đã trôi qua nếu đang làm việc."""
        current_time = datetime.now().strftime("%H:%M:%S")
        time_period = self.get_time_period()
        if self.working:
            elapsed_time = datetime.now() - self.start_time
            elapsed_time_str = str(elapsed_time).split('.')[0]
            current_time = f"{current_time}\n{elapsed_time_str}"
            if elapsed_time.seconds % 2 == 0:
                self.time_label.config(fg="red")  
            else:
                self.time_label.config(fg="cyan")  
        self.time_label.config(text=f"[ {time_period} ] {current_time}")
        self.master.after(1000, self.update_time)

    def start_timer(self):
        """Bắt đầu tính thời gian."""
        self.working = True
        self.start_time = datetime.now()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        """Dừng tính thời gian."""
        self.working = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def close_app(self):
        """Đóng ứng dụng."""
        self.master.destroy()

    def get_time_period(self):
        """Lấy buổi của ngày."""
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
        """Lấy ngày trong tuần."""
        weekdays = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
        current_weekday_index = datetime.now().weekday()
        return weekdays[current_weekday_index]

root = tk.Tk()
root.configure(bg="black")
app = WorkTimerApp(root)
root.mainloop()

def get_ip_address():
    """Lấy địa chỉ IP."""
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        return f"Đã xảy ra lỗi: {e}"

def get_wifi_speed(ip_address):
    """Lấy tốc độ wifi."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        url = f"http://{ip_address}"

        response = requests.get(url)

        while response.status_code != 200:
            time.sleep(1)
            response = requests.get(url)
        
        download_speed = st.download() / 1024 / 1024  
        upload_speed = st.upload() / 1024 / 1024  
        return f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps"
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"
    
def get_system_info():
    """Lấy thông tin hệ thống."""
    try:
        system_info = {}
        system_info['Device Name'] = f"{platform.node()}"
        system_info['Device Type'] = f"{platform.machine()}"
        system_info['IP Address'] = f"{get_ip_address()}"
        system_info['WiFi Speed'] = f"{get_wifi_speed(get_ip_address())} (Updating!!)"
        system_info['CPU'] = f"{platform.processor()}"
        system_info['CPU Usage'] = f"{psutil.cpu_percent(interval=1)}%"
        system_info['RAM'] = f"{round(psutil.virtual_memory().total / (1024 ** 2), 2)} MB"
        system_info['Used Memory'] = f"{round(psutil.disk_usage('/').used / (1024 ** 3), 2)} GB"
        system_info['Total Memory'] = f"{round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB"
        system_info['Free Memory'] = f"{round(psutil.disk_usage('/').free / (1024 ** 3), 2)} GB"
        return system_info
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

def main():
    """Hàm chính."""
    system_info = get_system_info()
    print("System Information")
    for key, value in system_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
