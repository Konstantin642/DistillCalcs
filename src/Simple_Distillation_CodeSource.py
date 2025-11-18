import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2)
    
def define_equlibrium_data(equlibrium_data_fileName):
    print(f"Equilibrium data were used from the file: {equlibrium_data_fileName}")
    str_data = []
    with open("./data/"+equlibrium_data_fileName, 'r') as f:
        for line in f:
            str_data.append(line.split())
    
    M_1=float(str_data[0][0][str_data[0][0].find("=")+1:])
    M_2=float(str_data[1][0][str_data[1][0].find("=")+1:])
    print(f"M1={M_1}")
    print(f"M2={M_2}")

    equlibrium_str_data = str_data[2:]
    data = np.zeros([len(equlibrium_str_data), 2])
   
    for i in range(len(equlibrium_str_data)):
        data[i][0] = float(equlibrium_str_data[i][0])
        data[i][1] = float(equlibrium_str_data[i][1])
    return M_1, M_2, data


def equlibrium_data_regression(data):
    sorted_indices_y = data[:,0].argsort()
    sorted_data_y = data[sorted_indices_y]
    delete_indices_y = []
    is_equal = False
    n_is_equal=0

    for i in range(len(sorted_data_y)-1):
        if sorted_data_y[i][0]==sorted_data_y[i+1][0]:
            if is_equal==False:
                is_equal=True
                is_equal_start = i
            n_is_equal+=1
        else:
            if is_equal==True:
                if n_is_equal==1:
                    delete_indices_y.append(is_equal_start)                
                if n_is_equal>1:
                    for i in range(n_is_equal+1):
                        if i == round((n_is_equal+1)/2):
                            continue
                        delete_indices_y.append(is_equal_start+i)
                n_is_equal=0
                is_equal = False             
    cleaned_sorted_data_y = np.delete(sorted_data_y, delete_indices_y, axis=0)
    cs_y_eq = CubicSpline(cleaned_sorted_data_y[:,0], cleaned_sorted_data_y[:,1])
    
    return cs_y_eq


def find_y_eq(cs_y_eq, x):
    result = cs_y_eq(x)
    if result.size>1:
        for i in result:
            if i>=-0.01 and i<=1.01:
                return i
        else: print(f"Can't find equilibrium y for x={x}")
    else:
        if result>=-0.01 and result<=1.01:
                return result
        else: print(f"Can't find equilibrium y for x={x}")        


# Check if the first component is the Low-Boiling component
def check_if_first_comp_is_LB(xf, M_1, M_2, data, cs_y_eq):
    if xf>cs_y_eq(xf):
        new_data = 1-data
        is_changed=1
        cs_y_eq = equlibrium_data_regression(new_data)
        
        M_1_temp = M_1
        M_1 = M_2
        M_2 = M_1_temp

        xf = 1- xf

        print(f"Component #1 is a high-boiling component at mole fraction xf={1-xf}!")
        print(f"\n   (Please note!)")
        print(f"   (Components #1 and #2 are swapped for correct calculations!!)")
        
        return new_data, xf, M_1, M_2, cs_y_eq, is_changed

    else:
        is_changed=0
        print(f"Component #1 is a low-boiling component at mole fraction xf={xf}")
        


        return data, xf, M_1, M_2, cs_y_eq, is_changed
    


def find_simple_dist_equation(data, cs_y_eq):

    delete_indices = []
    for i in range(len(data)):
        if data[i][0]==data[i][1]:
            delete_indices.append(i)
    new_data = np.delete(data, delete_indices, axis=0)

    integral_equation_data = np.zeros(len(new_data))
    for i in range(len(new_data)):
        integral_equation_data[i] = 1/(new_data[i][1] - new_data[i][0])

        

    x = np.linspace(0,1,401)
    y_dist_data =[]
    for i in x:
        y_dist_data.append(find_y_eq(cs_y_eq, i))


    delete_indices = []
    for i in range(len(x)):
        if x[i]==y_dist_data[i]:
            delete_indices.append(i)
    new_x = np.delete(x, delete_indices)
    new_y_dist_data = np.delete(y_dist_data, delete_indices)

    integral_equation_y_dist_data = np.zeros(len(new_y_dist_data))
    for i in range(len(new_y_dist_data)):
        integral_equation_y_dist_data[i] = 1/(new_y_dist_data[i] - new_x[i])
            

    cs_dist_eq = CubicSpline(new_x, integral_equation_y_dist_data)

   
    y_axis = []
    x_axis = np.linspace(0,1,251)
    for i in x_axis:
        y_axis.append(cs_dist_eq(i))

    axs[1].plot(x_axis, y_axis, label="regression")
    axs[1].plot(new_data[:,0], integral_equation_data, "r.", label="determined from the equilibrium data")
    axs[1].set_title("x-dependence of Rayleigh equation integrand")    
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("1/(y* - x)")
    axs[1].grid(True)
    axs[1].legend()
    axs[1].set_ylim(0,50)    
    return cs_dist_eq



def find_dist_results(cs_dist_eq, data, xw, xf, M_1, M_2):
    integral = np.zeros(len(xw))
    for i in range(len(xw)):
        integral[i] = cs_dist_eq.integrate(xw[i], xf)

    Gw_to_Gf =  1 / ( np.exp(integral) )
    Gd_to_Gf = 1 - Gw_to_Gf
    xd = (xf - Gw_to_Gf*xw) / Gd_to_Gf
 
    Gw_to_Gf_mass = Gw_to_Gf*(xw*M_1+(1-xw)*M_2)/(xf*M_1+(1-xf)*M_2)
    Gd_to_Gf_mass = Gd_to_Gf*(xd*M_1+(1-xd)*M_2)/(xf*M_1+(1-xf)*M_2)
    
    return Gw_to_Gf, Gd_to_Gf, xd, Gw_to_Gf_mass, Gd_to_Gf_mass


def find_opt(cs_dist_eq, data, xf, M_1, M_2,xw_test):
    xw = np.linspace(0+0.0001,xf-0.0001,400)
    Gw_to_Gf, Gd_to_Gf, xd, Gw_to_Gf_mass, Gd_to_Gf_mass = find_dist_results(cs_dist_eq, data, xw, xf, M_1, M_2)
    xd_mass = 1/((1/xd-1)*M_2/M_1+1)
    xw_mass = 1/((1/xw-1)*M_2/M_1+1) 
    print(f"Mole fraction of low-boiling compounent in feed: xf = {xf:.2f} \n  (will be used to plot the diagram)")  

    print("\nSimple distillation calculation \n(for a range of values in xw_test")
    print("  xw - mole fraction of low-boiling compounent in bottoms")
    print("  xd - mole fraction of low-boiling compounent in distillate")
    print("  xw_mass - mass fraction of low-boiling compounent in bottoms")
    print("  xd_mass - mass fraction of low-boiling compounent in distillate")
    print("  yield - yield of low-boiling compounent in distillate")   
    print("  Gw/Gf - the ratio of the bottoms product molar flow rate to the feed molar flow rate")
    print("  Gd/Gf - the ratio of the distillate molar flow rate to the feed molar flow rate")
    print("  Gw/Gf (mass) - the ratio of the bottoms product mass flow rate to the feed mass flow rate")
    print("  Gd/Gf (mass) - the ratio of the distillate mass flow rate to the feed mass flow rate")

    xw_test = np.array(xw_test)  
    Gw_to_Gf_test, Gd_to_Gf_test, xd_test, Gw_to_Gf_mass_test, Gd_to_Gf_mass_test = find_dist_results(cs_dist_eq, data, xw_test, xf, M_1, M_2) 
    xd_mass_test = 1/((1/xd_test-1)*M_2/M_1+1)
    xw_mass_test = 1/((1/xw_test-1)*M_2/M_1+1)
    
    print("")  
    for i in range(len(xw_test)):
        print(f"xw={xw_test[i]:.3f}")
        print(f"  xw_mass={xw_mass_test[i]:.3f} xd={xd_test[i]:.2f} xd_mass={xd_mass_test[i]:.2f} yield={(Gd_to_Gf_test[i]*xd_test[i]/xf):.2f} Gd/Gf={Gd_to_Gf_test[i]:.2f}  Gw/Gf={Gw_to_Gf_test[i]:.2f} Gd/Gf_(mass)={Gd_to_Gf_mass_test[i]:.2f}  Gw/Gf_(mass)={Gw_to_Gf_mass_test[i]:.2f}")
        print("")
    axs[0].plot(Gd_to_Gf*xd/(xf), xd_mass, label="Distillate purity: xd_mass", color="r", linestyle="-")
    axs[0].plot(Gd_to_Gf*xd/(xf), xw_mass, label="xw_mass", color="b", linestyle="-")
    axs[0].plot(Gd_to_Gf*xd/(xf), Gd_to_Gf_mass, label="Ratio: Gd/Gf (mass)", color="r", linestyle="--")
    axs[0].plot(Gd_to_Gf*xd/(xf), Gw_to_Gf_mass, label="Ratio: Gw/Gf (mass)", color="b", linestyle="--")

    axs[0].grid(True)
    axs[0].set_xlabel("Yield of low-boiling component in distillate: Gd*xd/(Gf*xf)")
    axs[0].legend()
    axs[0].set_title("Results of simple distillation")
    axs[0].set_xlim(0,1)
    axs[0].set_ylim(0,1)
    
    plt.show()


    
def main(equlibrium_data_fileName, xf, xw_test):
    M_1, M_2, data = define_equlibrium_data(equlibrium_data_fileName)
    cs_y_eq = equlibrium_data_regression(data)
    data, xf, M_1, M_2, cs_y_eq, is_changed = check_if_first_comp_is_LB(xf, M_1, M_2, data, cs_y_eq)
    cs_dist_eq = find_simple_dist_equation(data, cs_y_eq)
    find_opt(cs_dist_eq, data, xf, M_1, M_2,xw_test)


    
