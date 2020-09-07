from math import sin, cos, sqrt
from typing import Tuple
import os
from vrml.vrml97.parser import buildParser
from vrml.vrml97.basenodes import IndexedFaceSet, IndexedLineSet


class Object3d:
    def __init__(self):
        self.name = ""
        self.faces = tuple()
        self.coords = tuple()
        self.rotated_coords = tuple()
        self.lines = tuple()
        self.linecoords = tuple()
        self.rotated_linecoords = tuple()

    def load_from_wrl(self, filename):
        parser = buildParser()
        result = parser.parse(open(filename).read())
        scenegraph = result[1][1]
        if len(scenegraph.children) < 1:
            raise IOError("failed to load vrm file")
        self.name = os.path.splitext(os.path.split(filename)[1])[0]
        for shape in scenegraph.children:
            # mat = shape.appearance.material
            # self.shininess = mat.shininess
            # self.diffuseColor = tuple(mat.diffuseColor)
            # self.specularColor = tuple(mat.specularColor)
            geo = shape.geometry
            if isinstance(geo, IndexedFaceSet):
                faces = []
                face = []
                for index in geo.coordIndex:
                    if index == -1:
                        faces.append(tuple(face))
                        face.clear()
                    else:
                        face.append(index)
                if face:
                    faces.append(tuple(face))
                self.faces = tuple(faces)
                self.coords = tuple(tuple(xyz) for xyz in geo.coord.point)
                self.rotated_coords = self.coords
            elif isinstance(geo, IndexedLineSet):
                lines = []
                line = []
                for index in geo.coordIndex:
                    if index == -1:
                        lines.append(tuple(line))
                        line.clear()
                    else:
                        line.append(index)
                if line:
                    lines.append(tuple(line))
                self.lines = tuple(lines)
                self.linecoords = tuple(tuple(xyz) for xyz in geo.coord.point)
                self.rotated_linecoords = self.linecoords

    def load_directXmesh(self, filename):
        # TODO the mesh coordinates need to be de-duped!
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
                if scaling!=1:
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
                    points = tuple(int(x) for x in line[1].split(','))
                    if len(points) != num_points:
                        raise IOError("invalid number of points read")
                    faces.append(tuple(reversed(points)))
                self.faces = tuple(faces)
                break

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

    def normal_z(self, face: Tuple) -> float:
        p1 = self.rotated_coords[face[0]]
        p2 = self.rotated_coords[face[1]]
        p3 = self.rotated_coords[face[2]]
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

    def normalized_normal(self, face: Tuple) -> Tuple[float, float, float]:
        p1 = self.rotated_coords[face[0]]
        p2 = self.rotated_coords[face[1]]
        p3 = self.rotated_coords[face[2]]
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
