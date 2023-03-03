from Parser.Parsers.IdiotParser import *
from Parser.Parsers.XMLParser import *
from Parser.Parsers.JSONParser import *


class NurseParser:
    def __init__(self):
        self.idiotParser = IdiotParser()
        self.xmlParser = XMLParser()
        self.jsonParser = JSONParser()

    def parseFromTxt(self, textFile):
        return self.idiotParser.parse()

    def parseFromXML(self, xml):
        return self.xmlParser.parse(xml)

    def parseFromJSON(self, json):
        return self.jsonParser.parse(json)
