import src.Rectification_CodeSource as DistillCalcs
       
""" Instructions for use
1) Create a text document to store VLE data (or use the ones provided in the "data" folder).
- In the first two lines, write the molecular masses of components #1 and #2:
    - M_1=...
    - M_2=...
- Enter the VLE data starting with the third line:
    - In the first column: write the equilibrium mole fractions of component #1 in the liquid
    - In the second column: write the equilibrium mole fractions of component #1 in the vapor
- An example of filling out a file is presented in "ethanol_water_equilibrium_1atm.txt".
3) Place the created file in the "data" folder. Copy the name of the created file to the "equlibrium_data_fileName" variable.
4) Specify the mole fraction of component #1:
    - xd=... - in the distillate
    - xf=... - in the feed
    - xw=... - in the bottoms residue
5) Specify:
    - Gf=... - mass flow rate of the feed
    - R_UD=... - operating reflux ratio defined by the user (enter R_UD=0 if you want to use the empirical formula for calculating R)
"""

equlibrium_data_fileName = 'ethanol_water_equilibrium_1atm.txt'

xd=0.78
xf=0.20
xw=0.04

Gf=100

R_UD=2

# Enter the reflux ratio values ​​at which the theoretical stages number of column should be calculated
#For example, "R_test=[1, 1.5, 2, 2.5, 3]"
R_test = [0.5, 1, 1.5, 2, 2.5, 3]


DistillCalcs.main(equlibrium_data_fileName, xw, xf, xd, R_UD, Gf, R_test)
