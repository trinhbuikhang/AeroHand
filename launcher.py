"""
AeroHand Launcher với GUI đơn giản
"""

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import threading
import os

class AeroHandLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AeroHand Launcher")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.create_widgets()
        self.aerohand_process = None
        
    def center_window(self):
        """Căn giữa cửa sổ trên màn hình"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
    
    def create_widgets(self):
        """Tạo giao diện"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🚀 AeroHand", 
            font=("Arial", 24, "bold"),
            fg="#2E86AB"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root,
            text="Gesture Mouse Control",
            font=("Arial", 12),
            fg="#666666"
        )
        subtitle_label.pack(pady=(0, 20))
          # Status
        self.status_var = tk.StringVar(value="Ready to launch")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg="#333333"
        )
        status_label.pack(pady=10)
        
        # Camera selection frame
        camera_frame = tk.LabelFrame(self.root, text="Camera Selection", font=("Arial", 10, "bold"))
        camera_frame.pack(pady=10, padx=20, fill="x")
        
        self.camera_type = tk.StringVar(value="local")
        
        # Local camera option
        local_radio = tk.Radiobutton(
            camera_frame,
            text="Local Camera",
            variable=self.camera_type,
            value="local",
            font=("Arial", 9),
            command=self.on_camera_type_change
        )
        local_radio.pack(anchor="w", padx=10, pady=2)
        
        # Network camera option
        network_radio = tk.Radiobutton(
            camera_frame,
            text="Network Camera",
            variable=self.camera_type,
            value="network",
            font=("Arial", 9),
            command=self.on_camera_type_change
        )
        network_radio.pack(anchor="w", padx=10, pady=2)
        
        # Network camera IP input
        self.ip_frame = tk.Frame(camera_frame)
        self.ip_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.ip_frame, text="Camera IP:", font=("Arial", 9)).pack(side="left")
        self.ip_entry = tk.Entry(self.ip_frame, font=("Arial", 9), width=15)
        self.ip_entry.pack(side="left", padx=(5, 10))
        self.ip_entry.insert(0, "192.168.14.123")  # Default IP
        
        # Scan button
        scan_btn = tk.Button(
            self.ip_frame,
            text="Scan Network",
            font=("Arial", 8),
            command=self.scan_network,
            bg="#FF9800",
            fg="white",
            width=12
        )
        scan_btn.pack(side="left")
        
        # Initially hide IP frame
        self.ip_frame.pack_forget()
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Launch button
        self.launch_btn = tk.Button(
            button_frame,
            text="🎯 Launch AeroHand",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            command=self.launch_aerohand
        )
        self.launch_btn.pack(pady=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop AeroHand",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=15,
            height=1,
            command=self.stop_aerohand,
            state="disabled"
        )
        self.stop_btn.pack(pady=5)
        
        # Setup button
        setup_btn = tk.Button(
            button_frame,
            text="⚙️ Setup & Install",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=15,
            height=1,            command=self.run_setup
        )
        setup_btn.pack(pady=5)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Instructions:\n• Point index finger to move cursor\n• Pinch for left click\n• Fist for right click",
            font=("Arial", 9),
            fg="#666666",
            justify="center"
        )
        instructions.pack(pady=(10, 10))
        
        # Exit button
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 9),
            command=self.exit_app,
            width=10
        )
        exit_btn.pack(pady=5)
    def launch_aerohand(self):
        """Khởi chạy AeroHand"""
        if self.aerohand_process and self.aerohand_process.poll() is None:
            messagebox.showwarning("Warning", "AeroHand is already running!")
            return
        
        try:
            self.status_var.set("Launching AeroHand...")
            self.launch_btn.config(state="disabled")
            
            # Chuẩn bị command
            cmd = [sys.executable, "main.py"]
            
            # Thêm network camera arguments nếu cần
            if self.camera_type.get() == "network":
                camera_ip = self.ip_entry.get().strip()
                if not camera_ip:
                    messagebox.showerror("Error", "Please enter camera IP address")
                    self.launch_btn.config(state="normal")
                    self.status_var.set("Launch failed - No IP address")
                    return
                
                cmd.extend(["--camera-ip", camera_ip])
                self.status_var.set(f"Connecting to {camera_ip}...")
            else:
                self.status_var.set("Starting with local camera...")
            
            # Chạy AeroHand trong thread riêng
            def run_aerohand():
                try:
                    self.aerohand_process = subprocess.Popen(
                        cmd,
                        cwd=os.path.dirname(os.path.abspath(__file__))
                    )
                    
                    camera_info = "network camera" if self.camera_type.get() == "network" else "local camera"
                    self.root.after(0, lambda: self.status_var.set(f"AeroHand running with {camera_info}"))
                    self.root.after(0, lambda: self.stop_btn.config(state="normal"))
                    
                    # Đợi process kết thúc
                    self.aerohand_process.wait()
                    
                    # Update UI khi process kết thúc
                    self.root.after(0, self.on_aerohand_stopped)
                    
                except Exception as e:
                    self.root.after(0, lambda: self.on_launch_error(str(e)))
            
            thread = threading.Thread(target=run_aerohand)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.on_launch_error(str(e))
    
    def stop_aerohand(self):
        """Dừng AeroHand"""
        if self.aerohand_process and self.aerohand_process.poll() is None:
            try:
                self.aerohand_process.terminate()
                self.aerohand_process = None
                self.on_aerohand_stopped()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop AeroHand: {e}")
    
    def on_aerohand_stopped(self):
        """Callback khi AeroHand dừng"""
        self.status_var.set("AeroHand stopped")
        self.launch_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
    
    def on_launch_error(self, error_msg):
        """Callback khi có lỗi launch"""
        self.status_var.set("Launch failed")
        self.launch_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        messagebox.showerror("Launch Error", f"Failed to launch AeroHand:\n{error_msg}")
    
    def run_setup(self):
        """Chạy setup script"""
        try:
            self.status_var.set("Running setup...")
            subprocess.Popen([sys.executable, "setup.py"])
        except Exception as e:
            messagebox.showerror("Setup Error", f"Failed to run setup:\n{e}")
            self.status_var.set("Setup failed")
    
    def exit_app(self):
        """Thoát ứng dụng"""
        if self.aerohand_process and self.aerohand_process.poll() is None:
            if messagebox.askyesno("Confirm Exit", "AeroHand is still running. Stop and exit?"):
                self.stop_aerohand()
                self.root.after(1000, self.root.quit)
        else:
            self.root.quit()
    
    def on_camera_type_change(self):
        """Callback khi thay đổi loại camera"""
        if self.camera_type.get() == "network":
            self.ip_frame.pack(fill="x", padx=20, pady=5)
        else:
            self.ip_frame.pack_forget()
    
    def scan_network(self):
        """Scan network để tìm camera servers"""
        try:
            self.status_var.set("Scanning network...")
            
            def scan_in_thread():
                try:
                    from network_scanner import NetworkScanner
                    scanner = NetworkScanner()
                    found_servers = scanner.scan_network()
                    
                    self.root.after(0, lambda: self.on_scan_complete(found_servers))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.on_scan_error(str(e)))
            
            thread = threading.Thread(target=scan_in_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Scan Error", f"Failed to scan network: {e}")
            self.status_var.set("Scan failed")
    
    def on_scan_complete(self, found_servers):
        """Callback khi scan hoàn thành"""
        if found_servers:
            self.status_var.set(f"Found {len(found_servers)} camera server(s)")
            # Tự động điền IP đầu tiên
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, found_servers[0])
            messagebox.showinfo("Scan Complete", 
                              f"Found camera servers:\n" + "\n".join(found_servers))
        else:
            self.status_var.set("No camera servers found")
            messagebox.showwarning("Scan Complete", "No camera servers found on network")
    
    def on_scan_error(self, error_msg):
        """Callback khi scan lỗi"""
        self.status_var.set("Scan failed")
        messagebox.showerror("Scan Error", f"Network scan failed:\n{error_msg}")
    
    # ...existing code...
    
    def run(self):
        """Chạy launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.root.mainloop()

def main():
    """Hàm main"""
    launcher = AeroHandLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
