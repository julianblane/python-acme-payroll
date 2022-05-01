# acme_payroll
## Overview
I've chosen to solve this exercise using object-oriented programming, 
since it allows me to handle data in individual units, enabling me to do data parsing and validation in a structured way.<br>
Language chosen is python, since it allows me to implement it in a lightweight but scalable way.

## Architecture
The solution consists of the main script `acme_payroll.py` and a support module `payroll.py`, along their tests `test_acme_payroll.py`, `test_payroll.py` 

The support module implements the following architecture

![image](https://user-images.githubusercontent.com/49913638/166165961-58423b71-b7fe-4c5a-bf64-523189bf2065.png)


## Approach and methodology
My approach involved, first, reading and organizing the exercise prompt `exercise.md`,<br>
Then, I proceeded to design the architecture to give support to the data involved.<br>
After having finished designing, I proceeded to plan the implementation steps, organizing them into issues.<br>
Implementation was test-driven, working with the supplied use cases along new data.<br>
After implementation, I did exploratory testing to further test coverage.

## How to run
Its input is a txt file containing at least 5 employee schedules.<br>
To run, supply the filename as a command-line argument.
```
acme_payroll.py <filename.txt>
```
The file must follow this format:
``` 
EMPLOYEENAME=[MO,TU,WE,TH,FR,SA,SU]HH:MM-HH:MM, ...
```
``` 
ARON=MO12:00-18:00,WE10:00-15:00,FR10:00-22:00
```
## How to test
Use unittest test discovery to run all tests
```
python -m unittest
```
