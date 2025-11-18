import src.Simple_Distillation_CodeSource as DistillCalcs
       
""" 
1) Create a text document to store the VLE data (or use the ones provided in the "data" folder).
Enter the file name in the "equlibrium_data_fileName" variable.

2) Follow the file filling recommendations in "Rectification_Usage."
An example of filling out a file is presented in "ethanol_water_equilibrium_1atm.txt."

3) In the current file, specify the mole fraction of component #1 in the feed mixture:
- xf=...    
"""

equlibrium_data_fileName = 'ethanol_water_equilibrium_1atm.txt'

xf=0.20

# Enter the mole fraction of component #1 in the bottoms residue after simple distillation, at which the distillation result should be calculated.
#For example, "xw_test=[0.01, 0.02, 0.05, 0.10]"
xw_test = [0.01, 0.02, 0.05, 0.10]


DistillCalcs.main(equlibrium_data_fileName, xf, xw_test)
