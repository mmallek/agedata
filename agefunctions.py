# set up

import Image
import numpy as np

im_cover = Image.open('agegrids/Landcover_0809_1955.tif')
im_cond = Image.open('agegridsConditionClass_0809_1954.tif')
im_age = Image.open('agegridsAge_0809_1954.tif')

covarray = np.array([im_cover])
condarray = np.array([im_cond])
agearray = np.array([im_age])

np.dstack((covarray, condarray, agearray))

