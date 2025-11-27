import src.Simple_Distillation_CodeSource as DistillCalcs

equlibrium_data_fileName = 'ethanol_water_equilibrium_1atm.txt'

xf=0.20

# Enter the mole fraction of component #1 in the bottoms residue after simple distillation, at which the distillation result should be calculated.
#For example, "xw_test=[0.01, 0.02, 0.05, 0.10]"
xw_test = [0.01, 0.02, 0.05, 0.10]


DistillCalcs.main(equlibrium_data_fileName, xf, xw_test)
