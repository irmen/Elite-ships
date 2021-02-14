# simple, minimalistic VRML parser
# just enough to read the Elite ship wrl models.


import string
import glob


class Tokenizer:
    def __init__(self, inputstream):
        self.text = inputstream.read()
        self.ix = 0

    def _nextchar(self):
        if self.ix < len(self.text):
            self.ix += 1
            return self.text[self.ix - 1]
        return None

    def _skipwhitespace(self):
        try:
            while self.text[self.ix] in "\r\n\t ":
                self.ix += 1
        except IndexError:
            pass

    def _skipcomment(self):
        char = ''
        while char != '\n':
            char = self._nextchar()

    def rewind(self, tok):
        if tok[0] in ["symbol", "word", "number"]:
            self.ix -= len(tok[1]) + 1
        else:
            raise ValueError("cannot rewind")

    def __iter__(self):
        return self

    def __next__(self):
        self._skipwhitespace()
        char = self._nextchar()
        if char is None:
            return "EOF", None
        if char == '#':
            self._skipcomment()
            self._skipwhitespace()
            char = self._nextchar()
        if char in string.ascii_letters:
            word = char
            while True:
                char = self._nextchar()
                if char not in string.ascii_letters or not char:
                    return 'word', word
                word += char
        elif char == '-':
            char = self._nextchar()
            number = char
            while True:
                char = self._nextchar()
                if char not in string.digits + "." or not char:
                    return 'number', -(float(number))
                number += char
        elif char in string.digits:
            number = char
            while True:
                char = self._nextchar()
                if char not in string.digits + "." or not char:
                    return 'number', float(number)
                number += char
        else:
            return 'symbol', char


class Shape:
    def __init__(self, geo, appearance):
        self.geo = geo
        self.appearance = appearance


class IndexedFaceSet:
    def __init__(self, faceindexes, vertices):
        self.faceindexes = (int(x) for x in faceindexes)
        self.vertices = vertices


class IndexedLineSet:
    def __init__(self, lineindexes, vertices):
        self.lineindexes = (int(x) for x in lineindexes)
        self.vertices = vertices


class Vertices:
    def __init__(self, coordinates):
        # coordinates is a flat list, split it in tuples of (x,y,z) coordinates
        self.coordinates = []
        ci = iter(coordinates)
        while True:
            try:
                self.coordinates.append((int(next(ci)), int(next(ci)), int(next(ci))))
            except StopIteration:
                break


class VrmlParser:
    def __init__(self, tokenizer):
        self.tokens = tokenizer

    def parse(self):
        shapes = []
        while True:
            shapes.append(self.parse_shape())
            tok = next(self.tokens)
            if tok[0] == "EOF":
                return shapes
            self.tokens.rewind(tok)

    def parse_shape(self):
        tok = next(self.tokens)
        if tok != ('word', 'Shape'):
            raise ValueError("expected Shape")
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        geo = self.parse_geometry()
        appearance = self.parse_appearance()
        tok = next(self.tokens)
        if tok != ('symbol', '}'):
            raise ValueError("expected }")
        return Shape(geo, appearance)

    def parse_geometry(self):
        tok = next(self.tokens)
        if tok != ('word', 'geometry'):
            raise ValueError("expected geometry")
        tok = next(self.tokens)
        if tok == ('word', 'IndexedFaceSet'):
            return self.parse_indexedfaceset()
        elif tok == ('word', "IndexedLineSet"):
            return self.parse_indexedlineset()
        else:
            raise ValueError("invalid geometry")

    def parse_indexedfaceset(self):
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        tok = next(self.tokens)
        if tok != ('word', 'coordIndex'):
            raise ValueError("expected coordIndex")
        numbers = self.parse_numberlist()
        vertices = self.parse_vertices()
        # now skip the rest that occurs in this section
        while True:
            tok = next(self.tokens)
            if tok == ('symbol', '}'):
                return IndexedFaceSet(numbers, vertices)

    def parse_indexedlineset(self):
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        tok = next(self.tokens)
        if tok != ('word', 'coordIndex'):
            raise ValueError("expected coordIndex")
        numbers = self.parse_numberlist()
        vertices = self.parse_vertices()
        # now skip the rest that occurs in this section
        while True:
            tok = next(self.tokens)
            if tok == ('symbol', '}'):
                return IndexedLineSet(numbers, vertices)

    def parse_vertices(self):
        tok = next(self.tokens)
        if tok != ('word', 'coord'):
            raise ValueError("expected coord")
        tok = next(self.tokens)
        if tok != ('word', 'Coordinate'):
            raise ValueError("expected Coordinate")
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        tok = next(self.tokens)
        if tok != ('word', 'point'):
            raise ValueError("expected point")
        numbers = self.parse_numberlist()
        tok = next(self.tokens)
        if tok != ('symbol', '}'):
            raise ValueError("expected }")
        return Vertices(numbers)

    def parse_numberlist(self):
        tok = next(self.tokens)
        if tok != ('symbol', '['):
            raise ValueError("expected [")
        numbers = []
        while True:
            tok = next(self.tokens)
            if tok[0] == 'number':
                numbers.append(tok[1])
            elif tok == ('symbol', ']'):
                break
            else:
                raise ValueError("error in numberlist")
        return numbers

    def parse_appearance(self):
        tok = next(self.tokens)
        if tok != ('word', 'appearance'):
            raise ValueError("expected appearance")
        tok = next(self.tokens)
        if tok != ('word', 'Appearance'):
            raise ValueError("expected Appearance")
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        tok = next(self.tokens)
        if tok != ('word', 'material'):
            raise ValueError("expected material")
        tok = next(self.tokens)
        if tok != ('word', 'Material'):
            raise ValueError("expected Material")
        tok = next(self.tokens)
        if tok != ('symbol', '{'):
            raise ValueError("expected {")
        # now we skip everything in the materials section
        while True:
            tok = next(self.tokens)
            if tok == ('symbol', '}'):
                break
        tok = next(self.tokens)
        if tok != ('symbol', '}'):
            raise ValueError("expected }")


def parse_vrml_file(filename):
    with open(filename, "rt") as ins:
        tokenize = Tokenizer(ins)
        parser = VrmlParser(tokenize)
        return parser.parse()


if __name__ == "__main__":
    files = glob.glob("models/vrml/*.wrl")
    for f in files:
        with open(f, "rt") as ins:
            print("parsing", f)
            tokenize = Tokenizer(ins)
            parser = VrmlParser(tokenize)
            vrml = parser.parse()
            print(vrml)
