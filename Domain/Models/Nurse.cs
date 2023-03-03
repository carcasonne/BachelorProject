using System;
using Domain.Models.Enums;

namespace Domain.Models;

public class Nurse
{
    public string Name { get; set; }
    public Grade Grade { get; set; }

    public Nurse(string name, Grade grade)
    {
        Grade = grade;
        Name = name;
    }

    public void Print()
    {
        Console.WriteLine(Name + " is of grade: " + Grade);
    }
}

