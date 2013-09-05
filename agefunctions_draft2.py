
# exported rasters (as ascii)
covarray = genfromtxt("agegrids/cover_0815_1142.txt", dtype = int, skip_header = 6)
condarray = genfromtxt("agegrids/condclass_0815_1151.txt", dtype = int, skip_header = 6)
agearray = genfromtxt("agegrids/age_0815_1153.txt", dtype = int, skip_header = 6)

# lookup table from csv
# col 1 = CoverCode, col 2 = ConditionCode, col 4 = min age, col 5 = max age
lookup = genfromtxt("agelookuptable.csv", dtype = "S7,int,S9,int,int,int", delimiter = ',', names = True)

for cc in lookup:
    covercode = cc["CoverCode"] 
    condcode = cc["ConditionCode"]
    minage = cc["Min_Age"]
    maxage = cc["Max_Age"]
    covcond = (covercode == covarray) & (condcode == condarray)
    print covcond.shape
    if covcond.sum() == 0:
        continue
    clipped_agearray = np.clip(agearray[covcond], minage, maxage)
    np.place(agearray, covcond, clipped_agearray)
    print cc["Cover"], cc["Condition"], "ages revised."
    figure()
    hist(clipped_agearray)
    title(cc["Cover"] + ', ' + cc["Condition"])
    axvline(minage, c = 'r', ls = '--')
    axvline(maxage, c = 'r', ls = '--')
    xlabel("Age")
    #savefig("covcondage_plots/ages_hist_" + lookup["Cover"] + '_' + lookup["Condition"])
myheader = '''ncols         4506
nrows         3212
xllcorner     614891.22333361
yllcorner     4333092.4910081
cellsize      30
NODATA_value  -9999'''
np.savetxt("agegrids/revisedage_0823_1733.txt", agearray, fmt = '%1d' header = myheader, comments = '')