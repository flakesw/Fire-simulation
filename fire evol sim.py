# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:40:48 2017

@author: Sam Flake
"""
# todo:
# beer-lambert law function
# calculate light at each stratum of each tree
# research methods: how does this work for a non-spatially-explicit model?
# integrate across leaves of each tree
# add resprouting
# add grass
# add fire ~ grass

##############################################################################
# Import packages and set parameters
##############################################################################

import random as ran
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import solar_model as sol #solar_model.py, does math for insolation
import parameters as pa  #parameters.py, contains parameters for simulation
#exec(params)

def frange(start, stop, step=1.0):
    ''' "range()" like function which accept float type''' 
    i = start
    while i < stop:
        yield i
        i += step

def q(z, h):
    # PDF of leaf distribution as a function of height, crown shape
    
    if z<h:
        return(2 * pa.crownShape * (1-(z**pa.crownShape)*(h**(-pa.crownShape))) * \
               (z**(pa.crownShape - 1)) * (h**(-pa.crownShape)))
    else:
        return(0)
            
def qCDF(z, h):
    # indefinite integral is below. Matches results from q above, so long as
    # z is less than h
    if z> h:
        return(1)
    if z < 0:
        return(0)
    else:
        return(h**(-2*pa.crownShape)*(2*(h**pa.crownShape) * 
                   (z**pa.crownShape) - (z**(2*pa.crownShape))))
         

def getLeafAreaAboveZ(z, tree, standData, year):
    #if the value for z gets anywhere above the tree height,
    # things go crazy pretty fast. But it's faster than solving the integral
    # each time
    leafAreasAboveZ = []
    maxHeight = standData["maxHeight"][year]
    if z < maxHeight:
        for tree in forest:
            propLeafAboveZ = 1 - qCDF(z, tree.height)
            LAaboveZ = propLeafAboveZ * tree.areaLeaves
            leafAreasAboveZ.append(LAaboveZ)
        
        totalLAAboveZ = sum(leafAreasAboveZ)
        
        return(totalLAAboveZ)
    else:
        return(0)

     
def E(z, tree, standData, year):
    # canopy openness at height z given the leaf areas and extinction coefficient
    return(np.exp(-pa.extinct * getLeafAreaAboveZ(z, tree, standData, year)))

def Alf(z, tree, standData, year):
    # leaf-specific instantaneous assimilation rate for given cP1 and cP2, 
    # see appendix S6 of Falster et al 2011
    # approximation to the rectangular hyperbola model
    # canOpen should be between 0 and 1
    canOpen = E(z, tree, standData, year)
    return(pa.cP1 * (canOpen/(canOpen + pa.cP2)))
    

def Alayer(z, tree, standData, year):
    # instantaneous assimilation of the leaves at height z
    # calculated by finding the amount of leaf area at that height (q * area)
    # and the instaneous leaf-specific assimilation rate (Alf)
    return(Alf(z, tree, standData, year) * q(z, tree.height) * tree.areaLeaves)
        

def plotTreeCanopyShape(tree):
    # draws a picture of a tree
    x = list(frange(0, tree.height, step = 0.1))
    y = []
    for i in range(len(x)):
        y.append(q(x[i], tree.height))
        #y.append(tree.areaLeaves * Alayer(x[i], tree))
    plt.axis([0, max(y) + .3, 0, tree.height+1])
    plt.plot(y, x, "bo")
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
        self.areaLeaves = self.massLeaves * pa.sla #omega
        self.height = pa.alpha1 * (self.areaLeaves**pa.beta1)
        self.massSapwood = pa.woodDens * pa.stemVolAdjust * \
            (1/pa.leafToSapwood) * self.height
        self.massHeartwood = pa.woodDens * pa.stemVolAdjust * pa.alpha2 * \
            self.areaLeaves**pa.beta2
        self.massBark = pa.relBarkThickness * self.massSapwood 
        self.massFineRoots = 1
        self.massTotal = self.massLeaves + self.massSapwood + self.massHeartwood\
                       + self.massBark + self.massFineRoots
        self.woodVolume = (self.massSapwood + self.massHeartwood)/pa.woodDens
        self.currentDiam = np.sqrt(self.woodVolume * 3 / self.height / np.pi)
        
        
    def grow(self, photosynthate) :
        # Grow the tree by increment
        self.massLeaves = self.massLeaves + photosynthate
        
        self.areaLeaves = self.massLeaves * pa.sla #omega
        self.height = pa.alpha1 * (self.areaLeaves**pa.beta1)
        self.massSapwood = pa.woodDens * pa.stemVolAdjust * \
            (1/pa.leafToSapwood) * self.height
        self.massHeartwood = pa.woodDens * pa.stemVolAdjust * pa.alpha2 * \
            self.areaLeaves**pa.beta2
        self.massBark = pa.relBarkThickness * self.massSapwood 
        self.massFineRoots = 1
        self.massTotal = self.massLeaves + self.massSapwood + self.massHeartwood\
                       + self.massBark + self.massFineRoots
        self.woodVolume = (self.massSapwood + self.massHeartwood)/pa.woodDens
        self.currentDiam = np.sqrt(self.woodVolume * 3 / self.height / np.pi)
        
        #newDiam = self.currentDiam + increment
        self.currentAge += 1
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


#initialize a stand
forest = [Tree(number = i, birthYear = pa.yearBegin) for i in range(pa.nTrees)]

year = pa.yearBegin

# store trees in a list
standData = {"year" : [],
             "diams" : {},
             "ba" : {},
             "maxHeight" : {}}

#initialize standData for the first year, outside of the loop
yearData = {"biomass" : [],
            "diams" : [],
            "csa" : [],
            "height" : []} #temporary data for the year
for i in range(len(forest)) :
    if forest[i].alive : #get all the diameters
        yearData["biomass"].append(forest[i].massTotal)
        yearData["diams"].append(forest[i].currentDiam),
        yearData["csa"].append(np.pi * (forest[i].currentDiam /2) ** 2)
        yearData["height"].append(forest[i].height)
  
#add stand data to global variable        
standData["year"].append(year)
standData["diams"].update({year : np.mean(yearData["diams"]) } )
ba = sum(yearData["csa"][i] for i in range(0,len(yearData["csa"])))
standData["ba"].update({year : ba})
standData["maxHeight"].update({year : np.max(yearData["height"])})
#print(standData["ba"])


##############################################################################
# Simulation main loop
##############################################################################
tree = forest[0]
# Simulation loop
for year in pa.years :  
           
    
    #is there a fire this year?
    if pa.fireSim:
        fire = (ran.random() < pa.pFire)
    
    #tree loop
    for tree in forest : 
        
        if tree.alive :
            # carbon assimilated by all leaf layers in the tree,
            # corresponds to equation 12 in Falster 2011           
            assim = quad(Alayer, 0, tree.height, args = (tree, standData, year), maxp1=50, limit=300)
            
            #reproduce = ran.random() < pa.pReprod
            
            #print(tree.barkThickness)
            
            tree.grow(assim[0])     
            
            #if fire :   
              #  if (tree.barkThickness < pa.barkThreshold) : 
               #     tree.die()                 
                
#            if reproduce and not fire :
#                newNumber = len(forest) + 1
#                forest.append(Tree(number = newNumber, birthYear = year))

    year += 1
    # Calculate some stand-level summaries in a local variable
    yearData = {"biomass" : [],
                "diams" : [],
                "csa" : [],
                "height" : []} #temporary data for the year
    for i in range(len(forest)) :
        if forest[i].alive : #get all the diameters
            yearData["biomass"].append(forest[i].massTotal)
            yearData["diams"].append(forest[i].currentDiam),
            yearData["csa"].append(np.pi * (forest[i].currentDiam /2) ** 2)
            yearData["height"].append(forest[i].height)
      
    #add stand data to global variable        
    standData["year"].append(year)
    standData["diams"].update({year : np.mean(yearData["diams"]) } )
    ba = sum(yearData["csa"][i] for i in range(0,len(yearData["csa"])))
    standData["ba"].update({year : ba})
    standData["maxHeight"].update({year : np.max(yearData["height"])})
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



x = [list(standData["ba"].keys())]
y = [list(standData["ba"].values())]
plt.axis([0, 100, 0, 600])
plt.plot(x, y, "bo")


##############################################################################
# Extra junk code
##############################################################################

##testing assimilation functions
#x = list(frange(0, 10, step = 0.1))
#y = []
#for i in range(len(x)):
#    #y.append(Alayer(x[i], tree, standData, year))
#    #y.append(Alf(x[i], tree, standData, year))
#    y.append(E(x[i], tree, standData, year))
#plt.plot(x, y, "bo")
#
#x = list(frange(0, 1, step = 0.01))
#y = []
#for i in range(len(x)):
#    y.append(cP1 * (x[i]/(x[i] + cP2)))
#plt.plot(x, y, "bo")
        
