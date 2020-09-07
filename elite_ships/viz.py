import tkinter
from glob import glob
from .obj import Object3d


def viz():
    objects = []
    for filename in glob("elite-ships-src/vrml/*.wrl"):
        print("loading", filename)
        obj = Object3d()
        obj.load_from_wrl(filename)
        objects.append(obj)
    app = App()

    t = 0.0
    active_object = 0

    def next_object(e):
        nonlocal active_object
        active_object += 1

    def animate():
        nonlocal t, active_object
        robj = objects[active_object].rotated(t)
        app.draw_object(robj)
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
        self.canvas.create_line((x1,y1), (x2,y2), tags="line")

    def poly(self, coords):
        self.canvas.create_polygon(coords, tags="line", fill="", outline="black")

    def clear(self):
        self.canvas.delete("line")

    def project2d(self, x, y, z) -> tuple:
        z, y = y, z
        persp = 500/(z+300)
        return x * persp + self.WIDTH/2, y * persp + self.HEIGHT/2

    def draw_object(self, obj: Object3d) -> None:
        self.clear()
        for face in obj.faces:
            poly_coords = []
            for pointIndex in face:
                point = obj.coords[pointIndex]
                poly_coords.extend(self.project2d(*point))
            self.poly(poly_coords)
        for line in obj.lines:
            p1_2d = self.project2d(*obj.linecoords[line[0]])
            p2_2d = self.project2d(*obj.linecoords[line[1]])
            self.line(p1_2d[0], p1_2d[1], p2_2d[0], p2_2d[1])
