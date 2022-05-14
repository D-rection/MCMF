import tkinter as tk
from tkinter import *
from acl import *
import time
import win32gui
import win32con
import win32api
from settings import *


def create_animation_window():
    window = Tk()
    window.title("Курсач")
    window.geometry(f'{Window_Width}x{Window_Height}')
    window.config(bg='snow')
    return window


def debugmode(window: Frame):
    if Loop:
        window.mainloop()


class Pipe:
    def __init__(self, window: Tk, source: Importance, stock: Importance):
        self._window = window
        self._source = source
        self._stock = stock

        self._canvas = Pipevas(window)
        children = window_p.winfo_children()
        if not children.__contains__(self._canvas):
            self._canvas.set_position(Point(0, 0), Size(Window_Width, Window_Height))



        self._created = False

        self.source_section = None
        self.stock_section = None
        self.middle_section = None
        self.update()

        self._canvas.pack()

    def update(self):
        if self._created is False:
            self._created = True
        else:
            self._canvas.delete(self.source_section)
            self._canvas.delete(self.stock_section)
            self._canvas.delete(self.middle_section)

        so_le, so_ri, so_anc = self.decide_source_section()
        st_le, st_ri, st_anc = self.decide_stock_section()

        self.source_section = self._canvas.create_rectangle(
            so_le.x, so_le.y,
            so_ri.x, so_ri.y,
            outline="#fb0", fill="purple"
        )
        self.stock_section = self._canvas.create_rectangle(
            st_le.x, st_le.y,
            st_ri.x, st_ri.y,
            outline="#fb0", fill="purple"
        )
        self.middle_section = self._canvas.create_polygon(
            [so_ri.x, so_ri.y, so_anc.x, so_anc.y, st_le.x, st_le.y, st_anc.x, st_anc.y],
            fill="Blue"
        )

    def decide_source_section(self):
        adjustment = Bufferzone_Height / 2
        point_left = Point(self._source.node.right_side.x,
                           self._source.node.right_side.y - adjustment)
        point_right = Point(self._source.node.right_side.x + Bufferzone_Width,
                            self._source.node.right_side.y + adjustment)
        point_anchor = Point(self._source.node.right_side.x + Bufferzone_Width,
                             self._source.node.right_side.y - adjustment)
        return point_left, point_right, point_anchor

    def decide_stock_section(self):
        adjustment = Bufferzone_Height / 2
        point_left = Point(self._stock.node.left_side.x - Bufferzone_Width,
                           self._stock.node.left_side.y - adjustment)
        point_right = Point(self._stock.node.left_side.x,
                            self._stock.node.left_side.y + adjustment)
        point_anchor = Point(self._stock.node.left_side.x - Bufferzone_Width,
                             self._stock.node.left_side.y + adjustment)
        return point_left, point_right, point_anchor


class Node:
    def __init__(self, window: Frame, position: Point, size: Size, info: NodeInformation):
        self._window = window
        self._canvas = TransparentCanvas(self._window)  # full black
        self._canvas.configure(width=size.width, height=size.height)

        self.rectangle = self._canvas.create_rectangle(
            0, 0,
            size.width, size.height,
            outline="#fb0", fill="Green"
        )
        self.information = info
        self._label = self._canvas.create_text((Node_Width / 2, Node_Height / 2),
                                              anchor="center",
                                              text=self.information.ID,
                                              font="Times 20",
                                              fill="darkblue")

        self.left_side = Point(position.x, position.y + size.height / 2 - Bufferzone_Height / 2)
        self.right_side = Point(position.x + size.width, position.y + size.height / 2 - Bufferzone_Height / 2)
        self._pipes = []

        self._canvas.bind("<B1-Motion>", self.drag)
        self._canvas.pack()
        self._canvas.place(x=position.x, y=position.y)

    def connect_to(self, other_node):
        pipe = Pipe(self._window, )
        pass

    def add_pipe(self, pipe: Pipe):
        self._pipes.append(pipe)

    def move(self, vector: Point):
        self._canvas.move(self.rectangle, vector.x, vector.y)

    def update_sides(self, x, y):
        dx = Node_Width / 2
        dy = Node_Height / 2
        self.right_side = Point(x + dx, y)
        self.left_side = Point(x - dx, y)

    def drag(self, event):
        mouse_x = self._window.winfo_pointerx() - self._window.winfo_rootx()
        mouse_y = self._window.winfo_pointery() - self._window.winfo_rooty()
        event.widget.place(x=mouse_x, y=mouse_y, anchor=CENTER)

        for pipe in self._pipes:
            pipe.update()

        self.update_sides(mouse_x, mouse_y)


window_p = create_animation_window()

node_source = Node(window_p, Point(50, 50), Size(Node_Width, Node_Height), NodeInformation('', 0))
node_stock = Node(window_p, Point(400, 90), Size(Node_Width, Node_Height), NodeInformation('', 1))
node_seva = Node(window_p, Point(779, 1), Size(Node_Width, Node_Height), NodeInformation('', 2))

i_sc = Importance(node_source, 1, 1, 0)
i_st = Importance(node_stock, 1, 1, 0)
i_sv = Importance(node_seva, 1, 1, 0)
pipe = Pipe(window_p, i_sc, i_st)
other_pipe = Pipe(window_p, i_sc, i_sv)

node_source.add_pipe(pipe)
node_source.add_pipe(other_pipe)

node_stock.add_pipe(pipe)
node_seva.add_pipe(other_pipe)
# move_style(window, node)

debugmode(window_p)
