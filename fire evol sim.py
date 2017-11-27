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
from parameters import *  #parameters.py, contains parameters for simulation
#exec(params)


def q(z, h = tree.height):
    # PDF of leaf distribution as a function of height, crown shape
    
    if z<h:
        return(2 * crownShape * (1-(z**crownShape)*(h**(-crownShape))) * \
               (z**(crownShape - 1)) * (h**(-crownShape)))
    else:
        return(0)
            
quad(q, 0, 9, args = 10)  #PDF checks out, integral from 0 to h = 1
 
def qCDF(z,h):
    #indefinite integral is below. Matches results from q above 
    return(h**(-2*crownShape)*(2*(h**crownShape) * (z**crownShape) - (z**(2*crownShape))))
         

def getLeafAreaAboveZ(z):
    leafAreasAboveZ = []
    
    for tree in forest:
        propLeafAboveZ = 1 - qCDF(z, tree.height)
        LAaboveZ = propLeafAboveZ * tree.areaLeaves
        leafAreasAboveZ.append(LAaboveZ)
    
    totalLAAboveZ = sum(leafAreasAboveZ)
    
    return(totalLAAboveZ)

# canopy openness at height z given the leaf areas and     
def E(z):
    return(-extinct * getLeafAreaAboveZ(z))

#leaf-specific instantaneous assimilation rate for given cP1 and cP2, 
#see appendix S6 of Falster et al 2011

def Alf(z):
    return(cP1 * (E(z)/(E(z) + cP2)))
    
#instantaneous assimilation of the leaves at height z
def Alayer(z):
    
    return(Alf(z) * q(z) * tree.areaLeaves)
        
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


#initialize a stand
forest = [Tree(number = i, birthYear = yearBegin) for i in range(nTrees)]

year = yearBegin

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
for year in years :  
           
    
    #is there a fire this year?
    if fireSim:
        fire = (ran.random() < pFire)
    
    #tree loop
    for tree in forest : 
        
        #insolation of leaves
        

        
        assim = tree.areaLeaves * quad(Alayer, 0, tree.height)
        
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
    
    if year > yearBegin:
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

