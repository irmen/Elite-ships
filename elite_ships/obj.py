from math import sin, cos
from vrml.vrml97.parser import buildParser
from vrml.vrml97.basenodes import IndexedFaceSet, IndexedLineSet


class Object3d:
    def __init__(self):
        self.faces = tuple()
        self.coords = tuple()
        self.lines = tuple()
        self.linecoords = tuple()
        self.specularColor = (0.0, 0.0, 0.0)
        self.diffuseColor = (0.0, 0.0, 0.0)
        self.shininess = 0.0

    def load_from_wrl(self, filename):
        parser = buildParser()
        result = parser.parse(open(filename).read())
        scenegraph = result[1][1]
        if len(scenegraph.children) < 1:
            raise IOError("failed to load vrm file")
        for shape in scenegraph.children:
            mat = shape.appearance.material
            self.shininess = mat.shininess
            self.diffuseColor = tuple(mat.diffuseColor)
            self.specularColor = tuple(mat.specularColor)
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

    def rotated(self, t) -> "Object3d":
        r = Object3d()
        r.faces = self.faces
        r.lines = self.lines
        r.specularColor = self.specularColor
        r.diffuseColor = self.diffuseColor
        r.shininess = self.shininess
        matrix = self._make_matrix(t)
        r.coords = self._rotate(self.coords, matrix)
        r.linecoords = self._rotate(self.linecoords, matrix)
        return r

    def _make_matrix(self, t):
        # make the rotation matrix
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

    def _rotate(self, points, matrix) -> tuple:
        rotated = []
        for x, y, z in points:
            rotated.append((
                x*matrix[0][0] + y*matrix[0][1] + z*matrix[0][2],
                x*matrix[1][0] + y*matrix[1][1] + z*matrix[1][2],
                x*matrix[2][0] + y*matrix[2][1] + z*matrix[2][2]
            ))
        return rotated


def main():
    obj = Object3d()
    obj.load_from_wrl("elite-ships-src/vrml/cobra3.wrl")
    print("FACES:", obj.faces)
    print("FACESCOORDS:", obj.coords)
    print("LINES:", obj.lines)
    print("LINECOORDS:", obj.linecoords)
    print("MATERIAL:", obj.shininess, obj.diffuseColor, obj.specularColor)
