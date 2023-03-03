using Domain.Models;

namespace Knapsack;

public class GradeKnapsackModel : IKnapsackModel
{
    // Total number of required night shifts
    private readonly int E;
    // Total number of required day shifts 
    private readonly int D;
    // The schedule containing the shifts to be covered
    private Schedule Schedule;

    public GradeKnapsackModel(Schedule schedule)
    {
        Schedule = schedule;

        E = Schedule.Shifts.Where(x => x.IsNightShift()).Count();
        D = Schedule.Shifts.Count() - E;
    }

    public List<Nurse> SearchTree()
    {
        throw new NotImplementedException();
    }
}
