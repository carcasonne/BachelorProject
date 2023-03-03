using System;
using Domain.Models;

public interface IKnapsackModel
{
    // This will return a list of nurses, which are feasible for the schedule
    public List<Nurse> SearchTree();
}

