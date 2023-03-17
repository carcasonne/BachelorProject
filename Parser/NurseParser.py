from Parser.Parsers.JSONParser import JSONParser

import json


class NurseParser:
    def __init__(self):
        self.jsonParser = JSONParser()

    def parseFromJSON(self, filePath):
        file = open(filePath)
        jsonData = json.load(file)
        parsedData = self.jsonParser.parse(jsonData)
        return parsedData

    def parseScenario(self, scenario, example=False):
        return self.jsonParser.parseNRC(scenario, example)
