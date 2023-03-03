using System;
namespace Domain.Models;

public class Schedule
{
    public Shift[] Shifts { get; set; }
    public List<Nurse> Nurses { get; set; }

    public Schedule(Shift[] shifts, List<Nurse> nurses)
    {
        // 7 days, 3 shifts each
        if (shifts.Count() != 21)
            throw new ArgumentException();

        Shifts = shifts; 
        Nurses = nurses;
    }
}

