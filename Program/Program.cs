using Parser;
using Domain;
using Knapsack;

Console.WriteLine("Begging");



Console.WriteLine("Parsing...");

IParser parser = new NurseParser();
var Schedule = parser.ParseFromTxt("Hej med dig");

// Print alle de nurses vi har nu
Console.WriteLine("Parsed nurses:");
foreach (var nurse in Schedule.Nurses)
    nurse.Print();




Console.WriteLine("Running through knapsack...");

IKnapsackModel knapsackModel = new SimpleKnapsackModel(Schedule);
var feasibleNurses = knapsackModel.SearchTree();




Console.WriteLine("Tabu searching...");

TabuSearch.Class1.Print();




Console.WriteLine("Network flowing...");

NetworkFlow.Class1.Print();





Console.WriteLine("Done");

test();

void test()
{
    Console.WriteLine("En lille test");
}