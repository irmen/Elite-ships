import tkinter
from glob import glob
from .obj import Object3d


def viz():

    active_object = Object3d()
    app = App()

    def next_object(e):
        nonlocal active_object
        active_object = Object3d()
        # active_object.load_from_wrl(next(objects))
        active_object.load_directXmesh(next(objects))
        app.shipname(active_object.name)

    # objects = iter(glob("elite-ships-src/vrml/*.wrl"))
    objects = iter(glob("elite-ships-src/Geosbbc/*.X"))
    next_object(None)
    t = 0.0

    def animate():
        nonlocal t, active_object
        active_object.rotate(t)
        app.draw_object_using_lines(active_object)
        # app.draw_object_wireframe(active_object)
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

    def line(self, x1, y1, x2, y2, color="navy", width=2):
        self.canvas.create_line((x1+self.WIDTH/2, y1+self.HEIGHT/2),
                                (x2+self.WIDTH/2, y2+self.HEIGHT/2),
                                tags="line", fill=color, width=width)

    def poly(self, points, color="black"):
        coords = []
        for x, y in points:
            coords.extend((x+self.WIDTH/2, y+self.HEIGHT/2))
        self.canvas.create_polygon(coords, tags="line", fill="", outline=color, width=2)

    def text(self, x, y, text):
        self.canvas.create_text(x+self.WIDTH/2, y+self.HEIGHT/2, text=text, tags="line")

    def clear(self):
        self.canvas.delete("line")

    def shipname(self, name):
        self.canvas.delete("shipname")
        self.canvas.create_text(self.WIDTH//2, 50, text=name, font=("Courier", 24), tags="shipname")

    def draw_object_wireframe(self, obj: Object3d) -> None:
        self.clear()
        # no hidden surface removal, just draw all edges
        for p1i, p2i in obj.all_edges:
            p1_x, p1_y = obj.project2d(*obj.rotated_coords[p1i])
            p2_x, p2_y = obj.project2d(*obj.rotated_coords[p2i])
            self.line(p1_x, p1_y, p2_x, p2_y)

    def draw_object_using_lines(self, obj: Object3d) -> None:
        self.clear()
        num_lines = 0
        edge_drawn = [False] * len(obj.all_edges)
        for face_index in range(len(obj.faces_points)):
            face_points = obj.faces_points[face_index]
            # Quick, but imprecise, surface normal check for backface culling.
            # Should really take the view vector into account with full normal vector
            if obj.normal_z(face_points) >= 0:
                continue   # pointing away from us
            for edge in obj.faces_edges[face_index]:
                if not edge_drawn[edge]:
                    pix1, pix2 = obj.all_edges[edge]
                    p1x, p1y = obj.project2d(*obj.rotated_coords[pix1])
                    p2x, p2y = obj.project2d(*obj.rotated_coords[pix2])
                    self.line(p1x, p1y, p2x, p2y)
                    num_lines += 1
                    edge_drawn[edge] = True
            normal = obj.normalized_normal(face_points)
            self._draw_surface_normal(face_points, obj, normal, str(face_index))

        # certain geometry models have separate lines in them (not the .X ones though)
        for line in obj.lines:
            p1x, p1y = obj.project2d(*obj.rotated_linecoords[line[0]])
            p2x, p2y = obj.project2d(*obj.rotated_linecoords[line[1]])
            self.line(p1x, p1y, p2x, p2y)

    def draw_object_using_poly(self, obj: Object3d) -> None:
        self.clear()
        for faceIndex, face in enumerate(obj.faces_points):
            # Quick, but imprecise, surface normal check for backface culling.
            # Should really take the view vector into account with full normal vector
            if obj.normal_z(face) >= 0:
                continue   # pointing away from us
            # 3d -> 2d projection.
            points2d = []
            for pi in face:
                x, y, z = obj.rotated_coords[pi]
                points2d.append(obj.project2d(x, y, z))
            self.poly(points2d)
            # normal = obj.normalized_normal(face)
            # self._draw_surface_normal(face, obj, normal, str(faceIndex))
        # certain geometry models have separate lines in them (not the .X ones though)
        for line in obj.lines:
            p1x, p1y = obj.project2d(*obj.rotated_linecoords[line[0]])
            p2x, p2y = obj.project2d(*obj.rotated_linecoords[line[1]])
            self.line(p1x, p1y, p2x, p2y)

    def _draw_surface_normal(self, face, obj, normal, text):
        sum_x = sum_y = sum_z = 0
        for pi in face:
            x, y, z = obj.rotated_coords[pi]
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
        self.line(x1, y1, x2, y2, "maroon", 1)
        self.text(x2, y2, text)

