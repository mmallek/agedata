# set up

import Image
import numpy as np
import csv
import matplotlib.pyplot as plt


# generate array from ascii file
agearray = np.genfromtxt("agegrids/age_0815_1153.txt", dtype = None, skip_header = 6)
covarray = np.genfromtxt("agegrids/cover_0815_1142.txt", dtype = None, skip_header = 6)
condarray = np.genfromtxt("agegrids/condclass_0815_1151.txt", dtype = None, skip_header = 6)

lookup = np.genfromtxt('agelookuptable.csv', names=True, delimiter=',', dtype="S9,int,S9,int,int,int")

revisedagearray = np.genfromtxt("agegrids/revised_ages_0815.txt", dtype = None, skip_header = 6)

========================================================

# Generate plots for initial age array

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    ages = agearray[(covarray == cov) & (condarray == cond) & (agearray >= 0)]
    #ages = agearray_cropped[(covarray == cov) & (condarray == cond) & (agearray_cropped >= 0)]
    #print cov,cond,ages.size
    if ages.size > 0:
        figure()
        title(','.join([row['Condition'],row['Cover']]))
        hist(ages, bins = 20)
        #plot(row['Min_Age'],0,'ro')
        axvline(x=row['Min_Age'], color = 'r', ls = '--')
        #plot(row['Min_Age'], 0, '-')
        #plot(x,y,'o', x,a*x+b,'-')
        #scatter(row['Min_Age'],100)
        if row['Max_Age'] < 9999:
            #plot(row['Max_Age'],100,'ro')
            axvline(x=row['Max_Age'], color = 'r', ls = '--')
            #scatter(row['Max_Age'],100)
        savefig('covcondage_plots/ages_hist_'+'_'.join([row['Condition'],row['Cover']])+'.png')

========================================================

# Generate plots for revised age array

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    ages = revisedagearray[(covarray == cov) & (condarray == cond) & (revisedagearray >= 0)]
    if ages.size > 0:
        figure()
        title(','.join([row['Condition'],row['Cover']]))
        hist(ages, bins = 20)
        #plot(row['Min_Age'],0,'ro')
        axvline(x=row['Min_Age'], color = 'r', ls = '--')
        #plot(row['Min_Age'], 0, '-')
        #plot(x,y,'o', x,a*x+b,'-')
        #scatter(row['Min_Age'],100)
        if row['Max_Age'] < 9999:
            #plot(row['Max_Age'],100,'ro')
            axvline(x=row['Max_Age'], color = 'r', ls = '--')
        elif row['Max_Age'] == 9999:
            axvline(x=500, color = 'r', ls = '--')
            #scatter(row['Max_Age'],100)
        #axvline(x=row['Max_Age'], color = 'r', ls = '--')
        savefig('covcondage_plots/ages_hist_'+'_'.join([row['Condition'],row['Cover']])+'.png')        

======================================================

# Revise ages to fit allowed values

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    minage = row['Min_Age']
    maxage = row['Max_Age']
    covcond_combo = (covarray == cov) & (condarray == cond) & (agearray >= 0)
    ages = agearray[covcond_combo]
    ages_clip = np.clip(ages, minage, maxage)
    np.place(agearray, covcond_combo, ages_clip)
    print "writing " + row['Cover'] + " " + row['Condition'] + " to array."
#    revisedages = np.ma.clip(ages, minage, maxage)
#    if ages.size > 0:
#        #if (ages >= minage) & (ages <= maxage):
#        #if logical_and(ages >= minage, ages <= maxage): 
#            continue
#        elif ages < minage:
#            ages = minage
#        elif ages > maxage:
#            ages = maxage
    myheader = '''ncols         4506
nrows         3212
xllcorner     614891.22333361
yllcorner     4333092.4910081
cellsize      30
NODATA_value  -9999'''
np.savetxt("agegrids/revised_ages_0815.txt", agearray, fmt='%d', header=myheader), comments = ''

%[flag]width[.precision]specifier


==========================================================

# Number of pixels at maximum age for condition

covarray = np.genfromtxt("agegrids/cover_0815_1142.txt", dtype = None, skip_header = 6)
condarray = np.genfromtxt("agegrids/condclass_0815_1151.txt", dtype = None, skip_header = 6)
revisedagearray = np.genfromtxt("agegrids/revised_ages_0815.txt", dtype = None, skip_header = 6)
comboarray = np.genfromtxt("agecovcond_dis.txt", skip_header = 1, delimiter = ',', usecols = (1,2,3))
lookup = np.genfromtxt('agelookuptable.csv', names=True, delimiter=',', dtype="S9,int,S9,int,int,int")

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    minage = row['Min_Age']
    maxage = row['Max_Age']
    check = (cov == comboarray[:,2]) & (cond == comboarray[:,1]) & (maxage == comboarray[:,0])
    #check = np.isclose(cov,comboarray[:,2]) & np.isclose(cond, comboarray[:,1]) & np.isclose(maxage, comboarray[:,0])
    maxagecount = cov, cond, np.sum(check)
    #print np.sum(cov == comboarray[:,2]), np.sum(cond == comboarray[:,1]), np.sum(maxage == comboarray[:,0])
np.savetxt("maxagecount.txt", maxagecount, fmt='%d')



