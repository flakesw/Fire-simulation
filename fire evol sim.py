# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:40:48 2017

@author: Sam Flake
"""

# add resprouting
# add grass
# add fire ~ grass
# 

##############################################################################
# Import packages and set parameters
##############################################################################

import random as ran
import numpy as np

#parameters for the simuation
yearBegin = 0
maxYear = 100 # number of years to simulate
nTrees = 1 # number of trees to start with
pFire = 0.1 # probability of a fire
pReprod = 0 # probability of reproduction
fireSim = False
years = range(maxYear)
barkThreshold = 1 # survival threshold

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

######################################################################
# Define classes
######################################################################


class Tree(object) :
       
    '''
    Attributes:
        number: tree number
        currentDiam: current diameter
        barkThickness: relative bark thickness
        alive: logical, whether tree is alive or not
    '''
        
    def __init__(self, number, birthYear = 0, currentAge = 0, alive = True,\
                 diamInit = diamInit):
        
        self.number = number
        self.currentAge = 0
        self.birthYear = birthYear
        self.currentDiam = diamInit
        self.diamsDict =  {birthYear : diamInit}
        self.alive = True
        self.aliveDict = {birthYear: alive}
        
        #tree traits
        self.massLeaves = 0.5
        self.areaLeaves = self.massLeaves * sla #omega
        self.height = alpha1 * (self.areaLeaves**beta1)
        self.massSapwood = woodDens * stemVolAdjust * (1/leafToSapwood) * self.height
        self.massHeartwood = woodDens * stemVolAdjust * alpha2 * self.areaLeaves**beta2
        self.massBark = relBarkThickness * self.massSapwood 
        self.massFineRoots = 1
        self.massTotal = self.massLeaves + self.massSapwood + self.massHeartwood\
                       + self.massBark + self.massFineRoots
        self.woodVolume = (self.massSapwood + self.massHeartwood)/woodDens
        self.currentDiam = np.sqrt(self.woodVolume * 3 / self.height / np.pi)
        
        
    def grow(self, photosynthate) :
        # Grow the tree by increment
        # Will set increment later as function of stand and tree characteristics
        
        #newDiam = self.currentDiam + increment
        self.currentAge = self.currentAge + 1
        self.aliveDict.update({year + 1 : True })
        
        self.newDiam = np.sqrt(self.woodVolume * 3 / self.height / np.pi)
            
        self.diamsDict.update({ year + 1 : self.newDiam })
        
        #self.barkThickness = calc_bark_thickness(self.currentDiam, barkCoefa, barkCoefb)
        
    def die(self) :
        # Simple enough
        # We can add in sprouting here
        
        self.alive = False
        
#############################################################################
# Initialize some data structures
#############################################################################

# store trees in a list
standData = {"year" : [],
             "diams" : {},
             "ba" : {}}


forest = [Tree(number = i, birthYear = yearBegin) for i in range(nTrees)]
    
##############################################################################
# Simulation body
##############################################################################

   
# Simulation loop
for year in years :  
    
    #is there a fire this year?
    if fireSim:
        fire = (ran.random() < pFire)
    
    
    
    
    #tree loop
    for tree in forest : 
        
        #insolation of leaves
        
        
        #carbon uptake
        canopyOpen = 1
                
        q = 2g(1-znh)n)zn)1h)n if z £ h, otherwise 0 
        z = 
        def q(h, z):
            2 * crownShape * (1-z**crownShape)
        LA above height z = 
        
        Ez = exp(-extinct * integral(0 to infinity) of 
                 (LA above height z) * leaf area * )
        
        Alf = cP1 * (Ez/(Ez + cP2))
        
        assim = leaf area * integral(from 0 to height) of (Alf * PDF of leaves)
        
        reproduce = ran.random() < pReprod
        
        if tree.alive :
            #print(tree.barkThickness)
            
            tree.grow()     
            
            if fire :   
                if (tree.barkThickness < barkThreshold) : 
                    tree.die()                 
                
#            if reproduce and not fire :
#                newNumber = len(forest) + 1
#                forest.append(Tree(number = newNumber, birthYear = year))
    
    
    # Calculate some stand-level summaries in a local variable
    yearData = {"biomass" : []} #temporary data for the year
    for i in range(len(forest)) :
        if forest[i].alive : #get all the diameters
            yearData["biomass"].append(forest[i].massTotal)
            yearData["csa"].append(forest[i].currentDiam ** 2)
      
    #add stand data to global variable        
    standData["year"].append(year)
    standData["diams"].update({year : np.mean(yearData["diams"]) } )
    ba = sum(yearData["csa"][i] for i in range(0,len(yearData["csa"])))
    standData["ba"].update({year : ba})
    #print(standData["ba"])
            
            
##############################################################################         
# Summarize data
##############################################################################
#data = 
#year = 5
#
#for i in range(len(forest)) :
#    if forest[i].alive :
#        data["diams"].append(forest[i].diamsDict[30])
#
#print(np.mean(data["diams"])) 


import matplotlib.pyplot as plt

x = [list(standData["ba"].keys())]
y = [list(standData["ba"].values())]
plt.axis([0, 100, 0, 600])
plt.plot(x, y, "bo")

