# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:32:52 2024

@author: GBjon
"""

import random
import math
from math import factorial as fact
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def pandemic(days=5):
    
    #Selecting a 'random' seed.
    random.seed()
    
    #Patient zero with the number of days infected
    patient_zero = ['x', 1]
    
    #Generating the uninfected students
    #Each have a 50/50 chance of being immunized, 'i'.
    students = []
    for i in range(30):
        u = random.uniform(0,1)
        if u > 0.5:
            students.append(['o', 0])
        else:
            students.append(['i', 0])
            
    #The total classroom at the start of the simulation
    classroom = students
    classroom.append(patient_zero)
    
    #Probability of transmission for each infectious individual
    #They are independent of each other
    p = 0.02
    
    #Lists that hold the total infectious individuals for the day and probability for the day
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
        #If the number of infectious individuals is greater than 1
        if num_infected > 1:
            prob = p*num_infected
            #Applying the inclusion-exclusion principal to get total prob for day
            for k in range(1,num_infected):
                prob += ((-1)**k) * (fact(num_infected) / (fact(num_infected - (k+1)) * fact(k+1))) * (p**(k+1))
                
        #If there is only one infectious person, the total probability equals p
        elif num_infected == 1:
            prob = p
            
        #If there are zero infected individuals, the probability is zero. 
        else:
            prob = 0
        probs.append(prob)
        
            
        #Let's infect some people and cleanse others
        for j in range(len(classroom)):
            #Generating a random uniform number, if it is under the cdf of the probability
            #That person becomes infected.
            #Immunized individuals cannot become infected.
            if classroom[j][0] == 'o':
                if random.uniform(0,1) <= prob:
                    classroom[j][0] = 'x'
                    classroom[j][1] = 1
            
            #Once you are at your third day of being infected, you become cleansed after the day. 
            elif classroom[j][0] == 'x':
                if classroom[j][1] == 3:
                    classroom[j][0] = 'cleansed'
                else:
                    classroom[j][1] += 1
                    
        #total number of infected at the end of day
        day_infected = 0
        for j in range(len(classroom)):
            if classroom[j][0] == 'x':
                day_infected += 1
        
        #Total infected individuals for the day added to list
        infected_total.append(day_infected)
        
    #Finding the first day with zero infected
    days_zero = []
    for t in range(len(infected_total)):
        if infected_total[t] == 0:
                days_zero.append(t)
                
    if len(days_zero) > 0:
        day_ended = days_zero[0]+1
    else:
        day_ended = days+1
            
        
    return probs, infected_total, day_ended

days=30
infected = pandemic(days)
#print(infected)

#plt.plot(infected)
#plt.ylabel('Nunber Infected')
#plt.xlabel('Days')

#Simulating 100000 runs of model
k = 100000
runs = np.zeros(shape=(k,days))
day_ended = np.zeros(shape=(k))
probs = np.zeros(shape=(k,days))
for i in range(k):
   probs[i], runs[i], day_ended[i]  = pandemic(days)

#Mean number infected on day one
#day_one = runs[:,0]
#day_one -= 1
#mean_day_one = np.mean(day_one)
 
#Mean number infected by day two
#day_two =runs[:,1]
#day_two -= 1
#mean_day_two = np.mean(day_two)   

#Expected number infected each day including tommy
day_means = []
for i in range(runs.shape[1]):
    day_means.append(np.mean(runs[:,i]))
    
#Histogram of amount infected each day for 30 days
plt.plot(day_means)

#Histogram of amount of runs that ended on each day
hist = plt.hist(day_ended, bins=days)

np.mean(day_ended)
