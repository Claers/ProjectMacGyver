import math
import json


# Labyrinth class definition:
# Global Variable : Cells in array, what they contains, 0 for wall,1 for path
# Use variable at init : lenght,height
# Function to read a labyrinth
# Function to create a labyrinth
class Labyrinth:
    Cells = []

    def __init__(self):
        self._Init = True

    def RandomLab(self, LabCells):
        def Visit(xpos, ypos, isVisited):
            pass
        Visit(0, 0, False)
        return LabCells

    def CreateLab(self, filename, height, lenght):
        print(__name__)
        self.lenght = lenght
        self.height = height
        self.Cells = [[0 for x in range(height)] for y in range(lenght)]
        self.RandomLab(self.Cells)
        with open("LabyrinthFiles/" + filename + ".labyrinth", "w+") as file:
            json.dump(self.Cells, file)
