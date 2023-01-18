Agent-Based-Modelling Project

Agent Based Modelling approach, to simulate spatio-temporel person's movement in a city.
***************************************************************************************

Model Assumption:

• This model contains 2 agents: Person and Places

• The agent places are divided into 4 subtypes (4 species) Home, School, Work and Leisure.

• Every person is characterised by his age and his specific home.


• Persons gone to School, Work and Leisure the most closest.

• Every person has a probability going to School, Work or Leisure. This probability depends on person’s
age, distance from home to the closest place, day, and the current time.

• From Monday to Friday we have for current time in [8 am: 18 pm]:

– Every person his age ∈ [0,5] stay at home.

– Every person his age ∈ [6,25] has p = 0.9 to go to school (the most closest to his home).

– Every person his age ∈ [26,60] has p = 0.9 to go to work (the most closest to his home).

– Persons who’s ages are ∈ [61,90] have p = 0.5 to go to Leisure (the most closest to his home) or
stay at home.

• From Monday to Friday we have for the current time in [19 pm: 7 am (next day)]: All persons are is
their home

• During the week-end all persons has probability p = 0.9 to go to Leisure or staying at home with
probability p = 0.1.

Model Parameters:

• MEAN SPEED = 2: Persons’ displacement speed

• SIMULATION STEP = 1 1 minute: Model time-step

• ENV SIZE = 200 40000 m2: Environment dimensions

• NB WORKS = 5: Number of work places

• NB SCHOOLS = 5: Number of schools

• NB LEISURES = 5 : Number of leisure zones

• NB HOMES = 10 : Number of homes

• NB PERSONS = 100 : Number of persons

***************************************************************************************

Remarks:
1) For reasons related to my computer computing resources I have simulated the model for the period from January 1. to January 31. 2022.
2) In case you run the code to get demonstration (agent movement) kindly uncomment lines ( 190, 191, 205, 206) and comment lines ( from line 194 - to line 202 ).  And please be sure to change the date each time at the interval you want line ( 141, 142).
3) In case you run the code to get Figures kindly comment lines ( from line 194 - to line 202 ) and comment lines  ( 190, 191, 205, 206). And please be sure to change the date each time at the interval you want line ( 141, 142).
