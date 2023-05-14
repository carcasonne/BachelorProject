# BachelorProject
This is the git repository containing the code for the Bachelor project by Casper Wassar Skourup, Mads Piriwe Risom Andersen, and Villum Nils Robert Sonne for Softwareudvikling at the IT-University of Copenhagen. 

## Run the project

Start by installing the necessary requirements:

```
pip install -r requirements.txt
```

The project can be run via the RunStatistics python file. The runned scenario can be changed in the file RunStatistics.py. It can also be specified how many runs to make and if you want debugging prints:

```
python RunStatistics.py
```

Note that when running the file, the excel sheet 'RunStatisticsResults.xlsx' will be overwritten with data from the new run. 

## Datsets

Datsets can be found in /Data

Example .json files can be found in /Data/Example, while datsets taken from the Nurse Rostering Competition can be found
in /Data/NurseRosteringCompetition
