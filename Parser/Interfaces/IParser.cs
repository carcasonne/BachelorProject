using System;
using Domain.Models;

public interface IParser
{
    public Schedule ParseFromTxt(string textFile);
    public Schedule ParseFromXML(string textFile);
    public Schedule ParseFromJSON(string textFile);
}