import tkinter as tk
from tkinter import messagebox
from scapy.all import ARP, Ether, srp
import socket

def scan_network():
    target_ip = "192.168.1.0/24"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        try:
            #lấy tên 
            device_name = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            device_name = "?"

        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'name': device_name
        })

    if devices:
        message = "Devices:\n" + "\n".join([
            f"IP: {d['ip']}, MAC: {d['mac']}, Tên: {d['name']}" for d in devices
        ])
    else:
        message = "ko thấy"

    messagebox.showinfo("list:", message)

root = tk.Tk()
root.title("Scan")

window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

scan_button = tk.Button(root, text="Scan", command=scan_network)
scan_button.pack(pady=20)

root.mainloop()