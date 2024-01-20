from programPage.models.Composer import Composer


class MusicPiece:
    def __init__(self, composer: Composer, title: str, movements: list[int]):
        self.composer = composer
        self.title = title
        self.movements = movements


class Program:
    def __init__(self, pieces: list[MusicPiece]):
        self.pieces = pieces


def generateProgramPage(program: Program) -> str:
    print(program)
    # return string to filepath
    return "tmp"
