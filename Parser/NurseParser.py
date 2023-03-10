from Parser.Parsers.IdiotParser import *
from Parser.Parsers.XMLParser import *
from Parser.Parsers.JSONParser import *

import json


class NurseParser:
    def __init__(self):
        self.idiotParser = IdiotParser()
        self.xmlParser = XMLParser()
        self.jsonParser = JSONParser()

    def parseFromTxt(self, textFile):
        return self.idiotParser.parse()

    def parseFromXML(self, xml):
        return self.xmlParser.parse(xml)

    def parseFromJSON(self, filePath):
        file = open(filePath)
        jsonData = json.load(file)
        parsedData = self.jsonParser.parse(jsonData)
        
        return parsedData
