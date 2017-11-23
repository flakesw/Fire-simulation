# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:59:16 2017

@author: Sam
"""

#solar model, stolen from Falster and friends

from scipy.integrate import quad
import numpy as np

# Returns incoming PAR on surface normal to incoming light, for given solar
# angle (in radians) S_atmos = radiation outside atmosphere W / m2/s tau:
# transmisivity of shortest atmospheric path PAR_frac Fraction of light that is
# Photosynthetically Active return value in mol PAR / m2/ day
def PAR_given_solar_angle(solar_angle, S_atmos = 1360, tau = 0.8, PAR_frac = 0.5):
  
  # Adjust intensity for relative path-length through atmosphere
  # Would adjust for altitude here, but this function disabled
  altitude_adjustment = 1
  
  M = 1/np.cos(np.pi/2 - solar_angle) * altitude_adjustment
  
  mol_per_watt = 4.6/1e+06
  sec_per_day = 3600 * 24
  # Watts /m2/s
  ret = (S_atmos * PAR_frac) * tau**M * mol_per_watt * sec_per_day
  
  if solar_angle <= 0:
      ret = 0
  
  return(ret)



# Returns solar angle = angle between the horizontal and the line connecting to
# the sun for given latitude and time of day, in radians
def solar_angle(decimal_day_time, latitude):

  day = np.floor(decimal_day_time)
  time = (decimal_day_time - day) * 24
  
  def radians(x):
    return(x/180 * np.pi)
    
  lat_radians = radians(latitude)
  
  # solar declination (radians) - angle b/w the earth-sun line and the equatorial
  # plane
  delta = 0.39785 * np.sin(4.869 + day/365 * 2 * np.pi + 0.03345 * np.sin(6.224 + day/365 * 
    2 * np.pi))
  
  # Hour Angle (degrees) - angular distance that earth has rotated in a day
  HrAng = radians(180 - time * 15)
  
  # Sin of solar angle & Solar Angle - angle between the horizontal and the line
  # connecting to the sun
  SinA = np.sin(lat_radians) * np.sin(delta) + np.cos(lat_radians) * np.cos(delta) * np.cos(HrAng)
  
  return(np.arcsin(SinA))



def PAR_given_day_time(decimal_day_time):
    return(PAR_given_solar_angle(solar_angle = solar_angle(decimal_day_time, -30)))



quad(PAR_given_day_time, 0, 366)
