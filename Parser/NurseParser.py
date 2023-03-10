from Parser.Parsers.IdiotParser import *
from Parser.Parsers.JSONParser import *

import json


class NurseParser:
    def __init__(self):
        self.jsonParser = JSONParser()

    def parseFromJSON(self, filePath):
        file = open(filePath)
        jsonData = json.load(file)
        parsedData = self.jsonParser.parse(jsonData)
        
        return parsedData
