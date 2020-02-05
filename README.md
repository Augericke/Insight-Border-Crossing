# Insight-Border-Crossing | Data Engineer Assignment

## Contents
1. [Problem](README.md#problem)
1. [Approach](README.md#approach)
1. [Instructions](README.md#instructions)

## Problem
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, equipment, passengers and pedestrians crossing into the United States by land.

**For this challenge, we want to you to calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. We also want to know the running monthly average of total number of crossings for that type of crossing and border.**

The full description of the problem, provided by Insight, can be found [here](https://github.com/InsightDataScience/border-crossing-analysis).

## Approach
In general my approach followed:
- Read File
- Perform Aggregation By Group (Sum)
- Calculate Rolling Average
- Write File

In order to get the sum of values per group and montIn order to get the sum of values per group and month I opted to use a dictionary approach - which used a tuple constructed out of the defined groups for the key. As we read in the CSV the values per each group then gets added onto any existing keys - until the result is a dictionary with that same tuple and sum as the value.

For the rolling average a similar dictionary approach was also taken. However, in this case we looped through the resulting dictionary from the previous step and used an additional while loop search for and count the matching keys from proceeding months.

The following packages were also used in this assignment
- sys  | Allow for user selection of the input file  
- csv  | Read in input file
- math | Used floor function for creating a round function (in place of Python3 'Bankers Rounding')

## Instructions
To test this code, you can run the following command within the Insight-Border-Crossing folder:
```
    Insight-Border-Crossing~$ ./run.sh
```
