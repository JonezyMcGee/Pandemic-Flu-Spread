# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:48:00 2024

@author: GBjon
"""

import random
import math
from math import factorial as fact
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def pandemic(days=5):
    random.seed()
    
    #Patient zero with the number of days infected
    patient_zero = ['x', 1]
    #Generating the uninfected students
    students = []
    for i in range(30):
        students.append(['o', 0])
    #The total classroom at the start of the simulation
    classroom = students
    classroom.append(patient_zero)
    #Probability of transmission for each 'x'
    p = 0.02
    
    infected_total = []
    probs = []
    #start of simulation
    for i in range(days):
        
        #determining amount infected at start of day
        num_infected = 0
        for j in range(len(classroom)):
            if classroom[j][0] == 'x':
                num_infected += 1
                
        #determining probability of getting infected for each student
        #for this particular day
        if num_infected > 1:
            prob = p*num_infected
            #Applying the inclusion-exclusion principal to get total prob
            for k in range(1,num_infected):
                prob += ((-1)**k) * (fact(num_infected) / (fact(num_infected - (k+1)) * fact(k+1))) * (p**(k+1))
        elif num_infected == 1:
            prob = p
        else:
            prob = 0
        probs.append(prob)
        
            
        #Let's infect some people and cleanse others
        for j in range(len(classroom)):
            if classroom[j][0] == 'o':
                if random.uniform(0,1) <= prob:
                    classroom[j][0] = 'x'
                    classroom[j][1] = 1
            
            elif classroom[j][0] == 'x':
                if classroom[j][1] == 3:
                    classroom[j][0] = 'cleansed'
                else:
                    classroom[j][1] += 1
                    
        #total number of infected at the end of day
        num_infected = 0
        for j in range(len(classroom)):
            if classroom[j][0] == 'x':
                num_infected += 1
        
        #Total infected individuals for the day added to list
        infected_total.append(num_infected)
        
    #Finding the first day with zero infected
    days_zero = []
    for t in range(len(infected_total)):
        if infected_total[t] == 0:
            days_zero.append(t)
    
    #Finds the first day where the number of people infected is zero.
    #This is the end of the pandemic
    if len(days_zero) > 0:
        day_ended = days_zero[0]+1
    else:
        day_ended = days+1
            
    #Returns daily probabilities, daily infected totals, and the end of 
    #the pandemic for each run.
    return probs, infected_total, day_ended


#Simulating 100000 runs of model
days=30
k = 100000
runs = np.zeros(shape=(k,days))
day_ended = np.zeros(shape=(k))
probs = np.zeros(shape=(k,days))
for i in range(k):
    probs[i], runs[i], day_ended[i]  = pandemic(days)


#Expected number infected each day including patient zero
day_means = []
for i in range(runs.shape[1]):
    day_means.append(np.mean(runs[:,i]))
    
#Histogram of amount infected each day for 30 days
plt.plot(day_means)

#Histogram of amount of runs that ended on each day
hist = plt.hist(day_ended, bins=days)

#Average Day that the pandemic ended
avg_day_ended = np.mean(day_ended)
