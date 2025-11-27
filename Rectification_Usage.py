import src.Rectification_CodeSource as DistillCalcs

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
