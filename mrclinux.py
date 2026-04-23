import time
import os
import psutil
import datetime
import tkinter as tk

try:
    import GPUtil
except:
    GPUtil = None

root = tk.Tk()
root.title("Resource Monitor Console")
root.geometry("900x500")
root.configure(background="#2b2b2b")

title_label = tk.Label(root, text="Resource Monitor Console", font=("Arial", 16, "bold"), bg="#444444", fg="#ffffff")
title_label.pack(pady=10)

uptime_label = tk.Label(root, font=("Arial", 12), bg="#ffcccb", fg="#000000")
uptime_label.pack(pady=5)

clp = tk.Label(root, font=("Arial", 12), bg="#c1f0f6", fg="#000000")
clp.pack(pady=5)

cclp = tk.Label(root, font=("Arial", 12), bg="#fce5cd", fg="#000000")
cclp.pack(pady=5)

glp = tk.Label(root, font=("Arial", 12), bg="#d9d2e9", fg="#000000")
glp.pack(pady=5)

mlb = tk.Label(root, font=("Arial", 12), bg="#fff2cc", fg="#000000")
mlb.pack(pady=5)

dlb = tk.Label(root, font=("Arial", 12), bg="#c9daf8", fg="#000000")
dlb.pack(pady=5)

plp = tk.Label(root, font=("Arial", 12), bg="#ead1dc", fg="#000000")
plp.pack(pady=5)

def update_stats():
    btime = psutil.boot_time()
    uptime_secs = time.time() - btime
    uptime_str = str(datetime.timedelta(seconds=int(uptime_secs)))
    uptime_label.config(text=f"System Uptime: {uptime_str}")

    cpu_total = psutil.cpu_percent(interval=None)
    color_cpu = "#238B46" if cpu_total < 50 else "#FFA500" if cpu_total < 80 else "#FF0000"
    clp.config(text=f"CPU Total Usage: {cpu_total}%", fg=color_cpu)

    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
    cclp.config(text=f"CPU per Core: {cpu_per_core}", fg="#3333FF")

    gpu_text = "GPU: Not available"
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            g = gpus[0]
            gpu_text = f"{g.name} | Load: {g.load * 100:.1f}% | VRAM: {g.memoryUsed}MB/{g.memoryTotal}MB"

    glp.config(text=gpu_text, fg="#6600CC")

    mem = psutil.virtual_memory()
    color_mem = "#417241" if mem.percent < 50 else "#FFA500" if mem.percent < 80 else "#FF0000"
    mlb.config(text=f"Memory Total: {round(mem.total/(1024**3),2)} GB | Used: {mem.percent}%", fg=color_mem)

    disk = psutil.disk_usage('/')
    color_disk = "#417241" if disk.percent < 70 else "#FFA500" if disk.percent < 90 else "#FF0000"
    dlb.config(text=f"Disk Total: {round(disk.total/(1024**3),2)} GB | Used: {disk.percent}%", fg=color_disk)

    p = psutil.Process(os.getpid())
    plp.config(text=f"Process CPU %: {p.cpu_percent(interval=None)} | Memory: {round(p.memory_info().rss/(1024**2),2)} MB", fg="#993300")

    root.after(1200, update_stats)

update_stats()
root.mainloop()
