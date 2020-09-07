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
        app.bind("<space>", next_object)
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
        self.canvas.create_line((x1+self.WIDTH/2, y1+self.HEIGHT/2),
                                (x2+self.WIDTH/2, y2+self.HEIGHT/2),
                                tags="line", fill="navy", width=2)

    def poly(self, points):
        coords = []
        for x, y in points:
            coords.extend((x+self.WIDTH/2, y+self.HEIGHT/2))
        self.canvas.create_polygon(coords, tags="line", fill="", outline="black", width=2)

    def text(self, x, y, text):
        self.canvas.create_text(x+self.WIDTH/2, y+self.HEIGHT/2, text=text, tags="line")

    def clear(self):
        self.canvas.delete("line")

    def shipname(self, name):
        self.canvas.delete("shipname")
        self.canvas.create_text(self.WIDTH//2, 50, text=name, font=("Courier", 24), tags="shipname")

    def draw_object(self, obj: Object3d) -> None:
        self.clear()
        for faceIndex, face in enumerate(obj.faces):
            normal = obj.normalized_normal(face)
            if normal[2] >= 0:
                continue   # pointing away
            points = []
            for pointIndex in face:
                x, y, z = obj.rotated_coords[pointIndex]
                x, y = obj.project2d(x, y, z)
                points.append((x, y))
            self.poly(points)
            self._draw_normal(face, obj, normal, str(faceIndex))
        for line in obj.lines:
            p1x, p1y = obj.project2d(*obj.rotated_linecoords[line[0]])
            p2x, p2y = obj.project2d(*obj.rotated_linecoords[line[1]])
            self.line(p1x, p1y, p2x, p2y)

    def _draw_normal(self, face, obj, normal, text):
        sum_x = sum_y = sum_z = 0
        for i in face:
            x, y, z = obj.rotated_coords[i]
            sum_x += x
            sum_y += y
            sum_z += z
        nx1 = sum_x / len(face)
        ny1 = sum_y / len(face)
        nz1 = sum_z / len(face)
        nx2 = nx1 + normal[0] * 30
        ny2 = ny1 + normal[1] * 30
        nz2 = nz1 + normal[2] * 30
        x1, y1 = obj.project2d(nx1, ny1, nz1)
        x2, y2 = obj.project2d(nx2, ny2, nz2)
        self.line(x1, y1, x2, y2)
        self.text(x2, y2, text)

