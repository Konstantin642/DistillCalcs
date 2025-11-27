# DistillCalcs
This project is designed to model the distillation process for separating binary mixtures.
The project include two main program files to be executed:
1) Rectification_Usage – a file for calculating the rectification process.
2) Simple_Distillation_Usage – a file for calculating simple distillation.

## Rectification
"Rectification_Usage" allows you to calculate the following distillation column parameters:
- Number of theoretical stages
- Feed stage
- Minimum reflux ratio
- Distillate and bottoms composition
- Distillate and bottoms flow rate for a given feed mixture flow rate

<img src="https://github.com/Konstantin642/DistillCalcs/blob/main/images/Rectification_example1.png" height="200"> <img src="https://github.com/Konstantin642/DistillCalcs/blob/main/images/Rectification_example2.png" height="200">

## Simple_Distillation
"Simple_Distillation_Usage" allows you to determine the composition and flows of the bottoms and distillate of simple distillation depending on the degree of removal of the volatile component from the feed mixture.

<img src="https://github.com/Konstantin642/DistillCalcs/blob/main/images/Simple_Distillation_example1.png" height="200"> <img src="https://github.com/Konstantin642/DistillCalcs/blob/main/images/Simple_Distillation_example2.png" height="200">

## Instructions for use 
To successfully run the program, the following Python libraries must be installed:
 - NumPy
 - Matplotlib
 - SciPy

## Quick Start
Download the repository archive and unzip it.
 - Double-click "Rectification_Usage.py" to run the rectification calculation using the current settings in this file.
 - Double-click "Simple_Distillation_Usage.py" to run the simple distillation calculation using the current settings in this file.

## Setting up distillation parameters
### Rectification (file: "Rectification_Usage.py")
1) Find the file containing the VLE data for the components of interest in the "data" folder.
2) Copy the name of this file to the "equlibrium_data_fileName" variable.
3) Specify the mole fraction of component #1:
    - xd=... - in distillate
    - xf=... - in feed
    - xw=... - in bottom product
4) Specify:
    - Gf=... - feed mass flow rate
    - R_UD=... - user-defined working reflux ratio (enter R_UD=0 if you want to use the empirical formula to calculate R)

### Simple distillation (file: "Simple_Distillation_Usage.py")
1) Find the file containing the VLE data for the components of interest in the "data" folder.
2) Copy the name of this file to the "equlibrium_data_fileName" variable.
3) Specify the mole fraction of component #1 in the feed mixture:
    - xf=...

## Creating a document for storing VLE data*
1) Create a text document in the "data" folder.
2) In the first two rows, enter the molecular masses of components #1 and #2:
    - M_1=...
    - M_2=...
3) Enter the VLE data, starting with the third row:
    - equilibrium mole fractions of component #1 in the liquid in the first column
    - equilibrium mole fractions of component #1 in the vapor in the second column

*An example of filling out a file is presented in file "ethanol_water_equilibrium_1atm.txt".

## Sources:
- the VLE data presented in the "date" folder was obtained from the DWSIM program using the "Utilities" option and the "NRTL" property package.
