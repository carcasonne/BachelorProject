using System;
using Domain.Models.Enums;

namespace Domain.Models;

public class Shift
{
    public IDictionary<Grade, int> CoverRequirements { get; set; }
    public readonly bool NightShift;

    public Shift(IDictionary<Grade, int> coverRequirements, bool nightShift)
    {
        CoverRequirements = coverRequirements;
        NightShift = nightShift;
    }

    public bool IsNightShift()
    {
        return NightShift;
    }
}

