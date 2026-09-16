import numpy as np
import os, sys
# the compiled mocsy module is in the repository root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from mocsy import *

temp    = np.array([-1, 12, 25])  
salt    = temp*0 + 35.

phi0_cfc11 =    gasx.phizero('cfc11', temp, salt)
phi0_cfc12 =    gasx.phizero('cfc12', temp, salt)
phi0_sf6   =    gasx.phizero('sf6',   temp, salt)
phi0_co2   =    gasx.phizero('co2',   temp, salt)
phi0_n2o   =    gasx.phizero('n2o',   temp, salt)

print("phi0_cfc11 =", phi0_cfc11)
print("phi0_cfc12 =", phi0_cfc12)
print("phi0_sf6   =", phi0_sf6)
print("phi0_co2   =", phi0_co2)
print("phi0_n2o   =", phi0_n2o)


