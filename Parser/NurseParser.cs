using System;
using Domain.Models;
using Parser.Parsers;

namespace Parser;

public class NurseParser : IParser
{
	public NurseParser()
	{
	}

    public Schedule ParseFromTxt(string textFile)
    {
        //change this later
        return IdiotParser.Parse();
    }

    public Schedule ParseFromXML(string xml)
    {
        return XMLParser.Parse(xml);
    }

    public Schedule ParseFromJSON(string json)
    {
        return JSONParser.Parse(json);
    }


}


