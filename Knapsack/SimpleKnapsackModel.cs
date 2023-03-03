using Domain.Models;
using Domain.Models.Enums;

namespace Knapsack;

public class SimpleKnapsackModel : IKnapsackModel
{
    // Total number of required night shifts
    private readonly int E;
    // Total number of required day shifts 
    private readonly int D;
    // The schedule containing the shifts to be covered
    private Schedule Schedule;

    public SimpleKnapsackModel(Schedule schedule)
    {
        Schedule = schedule;

        // Måske har jeg forstået den her del forkert fra artiklen

        E = Schedule.Shifts
            .Where(x => x.IsNightShift())
            .Select(x => x.CoverRequirements[Grade.THREE])
            .Sum();

        D = Schedule.Shifts
            .Where(x => !x.IsNightShift())
            .Select(x => x.CoverRequirements[Grade.THREE])
            .Sum();

        Console.WriteLine("Schedule requires: " + E + " nurses to work all night shifts");
        Console.WriteLine("Schedule requires: " + D + " nurses to work all day shifts");
    }

    public List<Nurse> SearchTree()
    {
        // Just return the same nurses from input
        return Schedule.Nurses;
    }
}
