import tkinter
from glob import glob
from .obj import Object3d


def viz():

    active_object = Object3d()
    app = App()

    def next_object(e):
        nonlocal active_object
        active_object = Object3d()
        active_object.load_from_wrl(next(objects))
        app.shipname(active_object.name)

    objects = iter(glob("elite-ships-src/vrml/*.wrl"))
    next_object(None)
    t = 0.0

    def animate():
        nonlocal t, active_object
        active_object.rotate(t)
        app.draw_object(active_object)
        app.bind("<Key>", next_object)
        t += 0.08
        app.after(1000//30, animate)

    app.after(100, animate)
    app.mainloop()


class App(tkinter.Tk):

    WIDTH = 1024
    HEIGHT = 900

    def __init__(self):
        super().__init__()
        self.canvas = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()

    def line(self, x1, y1, x2, y2):
        self.canvas.create_line((x1,y1), (x2,y2), tags="line", fill="navy", width=2)

    def poly(self, coords):
        self.canvas.create_polygon(coords, tags="line", fill="", outline="black", width=2)

    def clear(self):
        self.canvas.delete("line")

    def shipname(self, name):
        self.canvas.delete("shipname")
        self.canvas.create_text(self.WIDTH//2, 50, text=name, font=("Courier", 24), tags="shipname")

    def draw_object(self, obj: Object3d) -> None:
        self.clear()
        for face in obj.faces:
            poly_coords = []
            for pointIndex in face:
                x, y, z = obj.rotated_coords[pointIndex]
                x, y = obj.project2d(x, y, z)
                poly_coords.append(x + self.WIDTH/2)
                poly_coords.append(y + self.HEIGHT/2)
            self.poly(poly_coords)
        for line in obj.lines:
            p1x, p1y = obj.project2d(*obj.rotated_linecoords[line[0]])
            p2x, p2y = obj.project2d(*obj.rotated_linecoords[line[1]])
            self.line(p1x + self.WIDTH/2, p1y + self.HEIGHT/2, p2x + self.WIDTH/2, p2y + self.HEIGHT/2)
