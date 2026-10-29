from tkinter import Tk, font, Canvas, PhotoImage
from configparser import ConfigParser
import os, pyglet, systemstatus

# config load start
print("load config")
cfg = ConfigParser()
cfg.read("config.ini")
BG = cfg["WINDOW"]["BgColor"]

class UI:
    def __init__(self): # ui init
        self.root = Tk()
        self.loadFont()

        self.root.title("newlai")
        self.root.geometry(cfg['WINDOW']['WindowSize'])
        self.root.resizable(False, False)
        self.root.configure(background=BG)

        self.defaultImagePath = "./assets/imgs"
        self.defaultSoundPath = "./assets/sfx"
        self.loadWidgets()
        self.checkSystemStatus()
        self.root.mainloop()

    def loadFont(self):
        fontfiles = next(os.walk('./assets/fonts/'), (None, None, []))[2]
        print(fontfiles)
        for cs_font in fontfiles:
            pyglet.font.add_file(os.path.join('./assets/fonts/', cs_font))
            print(f'loaded font: {cs_font}')

        self.default_normal = font.Font(family="ConsoleSans-Regular", size=15)
        self.default_bold = font.Font(family="ConsoleSans-Bold", size=15)

    def loadWidgets(self): # home - ui objects
        self.canvas = Canvas(self.root, bg=BG, highlightthickness=0, bd=0)
        self.canvas.pack(fill='both', expand=True)

        # wifi status
        self.wifistatus_off = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/wifi_off.png"))
        self.wifistatus_on = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/wifi_on.png"))

        # battery status
        self.battery_full = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/battery_full.png"))
        self.battery_mid = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/battery_mid.png"))
        self.battery_low = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/battery_low.png"))
        self.battery_none = PhotoImage(file=os.path.join(self.defaultImagePath, "general/status/battery_notfound.png"))

        self.wifi_item = self.canvas.create_image(25, 25, image=self.wifistatus_off, anchor='nw')
        self.batt_item = self.canvas.create_image(60, 20, image=self.battery_full, anchor='nw')
        self.batt_percent = self.canvas.create_text(100, 24, text=f'{systemstatus.getBattPowerGauge()}%', font=self.default_bold, anchor='nw', fill="black")
    
    def checkSystemStatus(self):
        # battery status
        if(not systemstatus.getBattery()): self.canvas.itemconfigure(self.batt_item, image=self.battery_none)
        if(systemstatus.getBattPowerGauge() <= 50): self.canvas.itemconfigure(self.batt_item, image=self.battery_mid)
        if(systemstatus.getBattPowerGauge() <= 20): self.canvas.itemconfigure(self.batt_item, image=self.battery_low)
        self.root.after(5000, self.checkSystemStatus)

if __name__ == "__main__":
    ui = UI()