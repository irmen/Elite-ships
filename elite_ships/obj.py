from math import sin, cos, sqrt
from typing import Tuple
import os
from .simplevrml import parse_vrml_file, IndexedFaceSet, IndexedLineSet


class Object3d:
    def __init__(self):
        self.name = ""
        self.faces_points = tuple()
        self.faces_edges = tuple()
        self.all_edges = tuple()
        self.coords = tuple()
        self.rotated_coords = tuple()
        self.lines = tuple()
        self.linecoords = tuple()
        self.rotated_linecoords = tuple()

    def load_from_wrl(self, filename):
        scene = parse_vrml_file(filename)
        if len(scene) < 1:
            raise IOError("failed to load vrm file")
        self.name = os.path.splitext(os.path.split(filename)[1])[0]
        for shape in scene:
            # mat = shape.appearance.material
            # self.shininess = mat.shininess
            # self.diffuseColor = tuple(mat.diffuseColor)
            # self.specularColor = tuple(mat.specularColor)
            if isinstance(shape.geo, IndexedFaceSet):
                faces = []
                face = []
                for index in shape.geo.faceindexes:
                    if index == -1:
                        faces.append(tuple(face))
                        face.clear()
                    else:
                        face.append(index)
                if face:
                    faces.append(tuple(face))
                self.faces_points = tuple(faces)
                self.coords = tuple(shape.geo.vertices.coordinates)
                self.rotated_coords = self.coords
            elif isinstance(shape.geo, IndexedLineSet):
                lines = []
                line = []
                for index in shape.geo.lineindexes:
                    if index == -1:
                        lines.append(tuple(line))
                        line.clear()
                    else:
                        line.append(index)
                if line:
                    lines.append(tuple(line))
                self.lines = tuple(lines)
                self.linecoords = tuple(shape.geo.vertices.coordinates)
                self.rotated_linecoords = self.linecoords
        self._build_edges()

    def load_directXmesh(self, filename):
        lines = iter(open(filename).readlines())
        while True:
            line = next(lines).strip()
            if line.startswith("Mesh "):
                _, self.name, _ = line.split(maxsplit=3)
                line = next(lines).strip().strip(";")
                num_points = int(line)
                coords = []
                scaling = 1
                for i in range(num_points):
                    point = next(lines).split(";")[:3]
                    point = tuple(float(x) * scaling for x in point)
                    coords.append(point)
                self.coords = tuple(coords)
                if scaling != 1:
                    print("----- SCALED COORDS OF ", self.name)
                    for point in self.coords:
                        print(f" {point[0]}; {point[1]}; {point[2]};,")
                    print("----- END SCALED\n")
                self.rotated_coords = self.coords
                next(lines)
                line = next(lines).strip().strip(";")
                num_faces = int(line)
                faces = []
                for i in range(num_faces):
                    line = next(lines).split(";")
                    num_points = int(line[0])
                    points = [int(x) for x in line[1].split(',')]
                    if len(points) != num_points:
                        raise IOError("invalid number of points read")
                    face = tuple(reversed(points))
                    faces.append(face)
                self.faces_points = tuple(faces)
                break
        self._remove_duplicate_coords()
        self._build_edges()

    def rotate(self, t: float) -> None:
        matrix = self._make_matrix(t)
        self.rotated_coords = self._rotate(self.coords, matrix)
        self.rotated_linecoords = self._rotate(self.linecoords, matrix)

    Matrix3x3Type = Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]

    def _make_matrix(self, t: float) -> Matrix3x3Type:
        cosa = cos(t)
        sina = sin(t)
        cosb = cos(t*0.33)
        sinb = sin(t*0.33)
        cosc = cos(t*0.78)
        sinc = sin(t*0.78)

        cosa_sinb = cosa*sinb
        sina_sinb = sina*sinb
        axx = cosa*cosb
        axy = cosa_sinb*sinc - sina*cosc
        axz = cosa_sinb*cosc + sina*sinc
        ayx = sina*cosb
        ayy = sina_sinb*sinc + cosa*cosc
        ayz = sina_sinb*cosc - cosa*sinc
        azx = -sinb
        azy = cosb*sinc
        azz = cosb*cosc
        return ((axx, axy, axz),
                (ayx, ayy, ayz),
                (azx, azy, azz))

    def _rotate(self, points: Tuple, matrix: Matrix3x3Type) -> Tuple:
        return tuple(
            (
                x*matrix[0][0] + y*matrix[0][1] + z*matrix[0][2],
                x*matrix[1][0] + y*matrix[1][1] + z*matrix[1][2],
                x*matrix[2][0] + y*matrix[2][1] + z*matrix[2][2]
            ) for x, y, z in points
        )

    def project2d(self, x: float, y: float, z: float) -> Tuple[float, float]:
        persp = 500/(z+300)
        return x * persp, y * persp

    def normal_z(self, points: Tuple) -> float:
        p1 = self.rotated_coords[points[0]]
        p2 = self.rotated_coords[points[1]]
        p3 = self.rotated_coords[points[2]]
        # So for a triangle p1, p2, p3, if the vector U = p2 - p1 and the vector V = p3 - p1
        # then the normal N = U * V and can be calculated by:
        # Nx = UyVz - UzVy
        # Ny = UzVx - UxVz
        # Nz = UxVy - UyVx
        ux = p2[0]-p3[0]
        uy = p2[1]-p3[1]
        vx = p1[0]-p3[0]
        vy = p1[1]-p3[1]
        return ux*vy - uy*vx

    def normalized_normal(self, points: Tuple) -> Tuple[float, float, float]:
        p1 = self.rotated_coords[points[0]]
        p2 = self.rotated_coords[points[1]]
        p3 = self.rotated_coords[points[2]]
        # So for a triangle p1, p2, p3, if the vector U = p2 - p1 and the vector V = p3 - p1
        # then the normal N = U * V and can be calculated by:
        # Nx = UyVz - UzVy
        # Ny = UzVx - UxVz
        # Nz = UxVy - UyVx
        ux, uy, uz = p2[0]-p3[0], p2[1]-p3[1], p2[2]-p3[2]
        vx, vy, vz = p1[0]-p3[0], p1[1]-p3[1], p1[2]-p3[2]
        nx = uy*vz - uz*vy
        ny = uz*vx - ux*vz
        nz = ux*vy - uy*vx
        length = sqrt(nx*nx + ny*ny + nz*nz)
        return nx/length, ny/length, nz/length

    def _remove_duplicate_coords(self):
        unique_points = {}
        for index, point in enumerate(self.coords):
            if point not in unique_points:
                unique_points[point] = len(unique_points)
        new_points = tuple(pt for ix, pt in sorted((index, point) for point, index in unique_points.items()))
        replaced_faces = []
        for face in self.faces_points:
            points = []
            for pi in face:
                point = self.coords[pi]
                points.append(unique_points[point])
            replaced_faces.append(tuple(points))
        self.coords = new_points
        self.rotated_coords = self.coords
        self.faces_points = tuple(replaced_faces)

    def _build_edges(self):
        edges = []
        faces = []

        def add_edge(point1, point2, face):
            edge = (point1, point2) if point1 < point2 else (point2, point1)
            try:
                edge_i = edges.index(edge)
            except ValueError:
                face.append(len(edges))
                edges.append(edge)
            else:
                face.append(edge_i)

        for face_pts in self.faces_points:
            face_edges = []
            p1 = face_pts[0]
            for p2 in face_pts[1:]:
                add_edge(p1, p2, face_edges)
                p1 = p2
            # connect back to the first point of the face
            p2 = face_pts[0]
            add_edge(p1, p2, face_edges)
            faces.append(face_edges)
        self.faces_edges = tuple(faces)
        self.all_edges = tuple(edges)
        if len(set(edges)) != len(edges):
            raise ValueError("check failed: edges are not unique")
        if len(self.faces_edges) != len(self.faces_points):
            raise ValueError("check failed: faces count mismatch")
