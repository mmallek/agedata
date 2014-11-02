# set up

import Image
import numpy as np
import csv
import matplotlib.pyplot as plt


# generate array from ascii file
agearray = np.genfromtxt("agegrids_0630/age.txt", dtype = None, skip_header = 6)
covarray = np.genfromtxt("agegrids_0630/cover.txt", dtype = None, skip_header = 6)
condarray = np.genfromtxt("agegrids_0630/condition.txt", dtype = None, skip_header = 6)

lookup = np.genfromtxt('agelookuptable20140708.csv', names=True, delimiter=',', dtype="S9,int,S9,int,int,int")

revisedagearray = np.genfromtxt("agegrids_0630/revised_ages_0630.txt", dtype = None, skip_header = 6)
oldagearray = np.genfromtxt("agegrids_0630/revised_ages_0630.txt", dtype = None, skip_header = 6)

========================================================

# Generate plots for initial age array

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    ages = agearray[(covarray == cov) & (condarray == cond) & (agearray >= 0)]

    if ages.size > 0:
        figure()
        title(','.join([row['Condition'],row['Cover']]))
        hist(ages, bins = 20)
        axvline(x=row['Min_ge'], color = 'r', ls = '--')
        if row['MaxAge'] < 9999:
            axvline(x=row['MaxAge'], color = 'r', ls = '--')
        savefig('covcondage_plots/ages_hist_'+'_'.join([row['Condition'],row['Cover']])+'.png')

========================================================

# Generate plots for revised age array

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    ages = revisedagearray[(covarray == cov) & (condarray == cond) & (revisedagearray >= 0)]
    if ages.size > 0:
        figure()
        title(','.join([row['Cover'],row['Condition']]))
        hist(ages, bins = 20)
        axvline(x=row['MinAge'], color = 'r', ls = '--')
        if row['MaxAge'] < 9999:
            axvline(x=row['MaxAge'], color = 'r', ls = '--')
        elif row['MaxAge'] == 9999:
            axvline(x=500, color = 'r', ls = '--')
        savefig('covcondage_plots/ages_hist_'+'_'.join([row['Cover'],row['Condition']])+'.png')        

======================================================

# Revise ages to fit allowed values

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    minage = row['MinAge']
    maxage = row['MaxAge']
    covcond_combo = (covarray == cov) & (condarray == cond) & (agearray >= 0)
    ages = agearray[covcond_combo]
    ages_clip = np.clip(ages, minage, maxage)
    np.place(agearray, covcond_combo, ages_clip)
    print "writing " + row['Cover'] + " " + row['Condition'] + " to array."
    # make sure header info below matches exported ascii files
    myheader = '''ncols         2910
nrows         2244
xllcorner     643616.208
yllcorner     4347856.558
cellsize      30
NODATA_value  -9999'''
np.savetxt("agegrids_0630/revised_ages_0630_1503.txt", agearray, fmt='%d', header=myheader, comments = '')

#[flag]width[.precision]specifier


==========================================================

# Number of pixels at maximum age for condition

#comboarray = np.genfromtxt("agecovcond_dis.txt", skip_header = 1, delimiter = ',', usecols = (1,2,3))

covcond_combo = (covarray == cov) & (condarray == cond) & (revisedagearray >= 0)

lookup = np.genfromtxt('agelookuptable.csv', names=True, delimiter=',', dtype="S9,int,S9,int,int,int")

for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    minage = row['Min_Age']
    maxage = row['Max_Age']
    #check = (cov == comboarray[:,2]) & (cond == comboarray[:,1]) & (maxage == comboarray[:,0])
    #check = np.isclose(cov,comboarray[:,2]) & np.isclose(cond, comboarray[:,1]) & np.isclose(maxage, comboarray[:,0])
    #check = (covarray == cov) & (condarray == cond) & (revisedagearray == maxage)
    check2 = (covarray == cov) & (condarray == cond) & (oldagearray == maxage)
    #maxagecount = cov, cond, np.sum(check)
    maxagecount = cov, cond, np.sum(check2)
    print maxagecount
np.savetxt("maxagecount.txt", maxagecount, fmt='%d')



==========================================================

# Create Condition-Age
# Condition-Age is the # of years in that condition class
# We decided to make everything the youngest it could be, so this function needs to take the current age
# and subtract the min age. Thus if a pixel is LPN MDC and 50 years old, and the minimum age for MDC is 10,
# then the condition-age will be 40. 

#So we need to load the revisedagearray, covarray, and condarray at the top of this document, as well as the lookup

agearray = np.genfromtxt("agegrids/age_0815_1153.txt", dtype = None, skip_header = 6)
covarray = np.genfromtxt("agegrids/cover_0815_1142.txt", dtype = None, skip_header = 6)
condarray = np.genfromtxt("agegrids/condclass_0905_1302.txt", dtype = None, skip_header = 6)

lookup = np.genfromtxt('agelookuptable.csv', names=True, delimiter=',', dtype="S9,int,S9,int,int,int")

revisedagearray = np.genfromtxt("agegrids_0630/revised_ages_0630_1503.txt", dtype = None, skip_header = 6)


for row in lookup:
    cov = row['CoverCode']
    cond = row['ConditionCode']
    minage = row['MinAge']
    if minage == 99998:
        continue 
    covcond_combo = (covarray == cov) & (condarray == cond)
    ages = revisedagearray[covcond_combo]
    condages = ages - minage
    np.place(revisedagearray, covcond_combo, condages)
    print "writing " + row['Cover'] + " " + row['Condition'] + " to array."

    myheader = '''ncols         2910
nrows         2244
xllcorner     643616.208
yllcorner     4347856.558
cellsize      30
NODATA_value  -9999'''
np.savetxt("agegrids_0630/condage_0630_1513.txt", revisedagearray, fmt='%d', header=myheader, comments = '')














