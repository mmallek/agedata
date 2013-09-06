Work Week of 0826

# Generate plots for revised age array
# Only by cover type
# To be used in conjunction with Age raster to evaluate quality.

coverlist = np.genfromtxt('cover_copy.csv', usecols=(0,1,2), names=True, delimiter=',', dtype="int,S44,S7")

revisedagearray = np.genfromtxt("agegrids/revised_age_0822_1112.txt", dtype = None, skip_header = 6)
covarray = np.genfromtxt("agegrids/cover_0815_1142.txt", dtype = None, skip_header = 6)

for covtype in coverlist:
    cov = covtype['cover_id']
    ages = revisedagearray[(covarray == cov) & (revisedagearray >= 0)]
    #if ages.size > 0:
    figure()
    title(covtype['cover_abr'])
    plt.xlabel('Age')
    hist(ages, bins = 20)
    savefig('age_by_cover_hists/ages_hist_'+'_'.join([covtype['cover_abr']])+'.png')        