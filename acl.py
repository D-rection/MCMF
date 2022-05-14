# Auxiliary Class Library
from tkinter import *
from settings import *
import win32gui
import win32con
import win32api


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class TransparentCanvas(Canvas):
    def __init__(self, window):
        super().__init__(window)
        self.configure(bg='#000000')
        hwnd = self.winfo_id()
        colorkey = win32api.RGB(0, 0, 0)  # full black in COLORREF structure
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 255, win32con.LWA_COLORKEY)

        self.configure(width=Window_Width, height=Window_Height)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class NodeInformation:
    def __init__(self, name: str, identifier: int):
        self.name = name
        self.ID = identifier


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


@singleton
class Pipevas(TransparentCanvas):
    def set_position(self, vector: Point, size: Size):
        self.configure(width=size.width, height=size.height)
        self.place(relx=vector.x, rely=vector.y)


class Importance:
    def __init__(self, node, ports_count, bandwidth, port_number):
        self.ports_count = ports_count
        self.bandwidth = bandwidth
        self.port_number = port_number
        self.node = node
