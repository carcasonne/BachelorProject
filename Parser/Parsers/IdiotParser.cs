using System;
using Domain.Models;
using Domain.Models.Enums;

namespace Parser.Parsers;

internal class IdiotParser
{
    public static Schedule Parse()
    {
        var nurses = new List<Nurse>();
        var shifts = new Shift[21];

        var nurse1 = new Nurse("Jens", Grade.ONE);
        var nurGse2 = new Nurse("Emma", Grade.TWO);
        var nurse3 = new Nurse("Paolo", Grade.THREE);

        nurses.Add(nurse1);
        nurses.Add(nurse2);
        nurses.Add(nurse3);

        var requirements = new Dictionary<Grade, int>();
        requirements[Grade.ONE] = 1;
        requirements[Grade.TWO] = 2;
        requirements[Grade.THREE] = 4;

        for(int i = 0; i < shifts.Count(); i++)
        {
            if(i % 3 == 0)
            {
                shifts[i] = new Shift(requirements, true);
            }
            else
            {
                shifts[i] = new Shift(requirements, false);
            }
        }

        return new Schedule(shifts, nurses);
    }
}

