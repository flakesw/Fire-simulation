# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:55:33 2017

@author: Sam
"""

#parameters for the simuation
yearBegin = 0
maxYear = 100 # number of years to simulate
nTrees = 1 # number of trees to start with
pFire = 0.1 # probability of a fire
pReprod = 0 # probability of reproduction
fireSim = False
years = range(maxYear)
barkThreshold = 1 # survival threshold
plotSize = 1000 #m2 -- used to calculate total PAR

#tree traits
diamInit = 1 # initial diameter of a new recruit
diamIncrement = .2 # diameter increment per year
#barkCoefa = 1.16
#barkCoefb = 2.44
sla = 10 #m2 per kg
woodDens = 700 #kg per m2
hmat = 5 #height at maturity

#Individual allometry
crownShape = 12 #crown shape parameter, eta
stemVolAdjust = 1 - 1/(2 + crownShape) + 1/(1 + 2*crownShape) 
leafToSapwood = 4669 #unitless, inverse of Huber value, theta
alpha1 = 5.44 #m^-1, scaling of height with leaf area
beta1 = 0.306 #unitless scaling of height with leaf area
alpha2 = 6.67e-5 #m, scaling of heartwood vol with leaf area
beta2 = 1.75 #unitless scaling of heartwood vol with leaf area
alpha3 = 0.07 #kg m^-2, scaling root mass with leaf area
relBarkThickness = 0.17

#Production
massNitPerAreaLeaf = 1.87e-3 #kg * m^-2
ratioAssToMassNit = 1.78e5 # mol * year^-1 * kg^-1
APerLA = massNitPerAreaLeaf * ratioAssToMassNit
ratioDarkRespToLeafNit = 2.1e4 #mol year-1 kg -1
fineRootRespPerMass = 217 # mol year-1 kg-1
sapwoodRespPerStemVol = 4012 #mol year-1 m-3
yieldCarbon = 0.7 #dimensionless, ratio of fixed carbon per assimilated carbon
carbonToDryMass = 2.45e-2 # kg mol-1, convert mols to kg carbon
alpha4 = 2.86e-2 #m2 kg-1 yr-1, describes scaling of turnover rate for 
                 #leaf with LMA
beta4 = 1.71 #dimensionless, same desc as alpha4
turnoverBark = .2 # year-1, proportion bark turnover
turnoverFineRoots = 1.0 # year-1, proportion root turnover

#physical parameters
extinct = 0.5 #k from beer-lambert
latitude = -30 #used for solar angle stuff

#Seed production
costAccessory = 4 #dimensionless, scale accessory costs by seed mass
maxAllocationReprod = 1.0 #dimensionless, maximum allocation to reprodution
rateOfChangeAtMaturity = 50 # alters equation 16

#carbon assimilation constants
#need to revise to reflect cerrado system, light-response curves for cerrado plants
cP1 = 150.36
cP2 = 0.19

#unused empirical relationship between bark and diameter
#def calc_bark_thickness(diam, barkCoefa, barkCoefb):
#    #relationship parameterized from savanna field data
#    return(barkCoefa + barkCoefb * np.log(diam))
