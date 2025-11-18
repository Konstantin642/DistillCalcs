import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

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


def find_x_eq(cs_y_eq, y):
    result = cs_y_eq.solve(y)
    if result.size>1:
        for i in result:
            if i>=-0.01 and i<=1.01:
                return i
        else: print(f"Can't find equilibrium x for y={y}")
    else:
        if result>=-0.01 and result<=1.01:
            return result[0]
        else: print(f"Can't find equilibrium y for x={x}")

def check_azeotrope_condition(cs_y_eq, xw, xd):
    if (find_y_eq(cs_y_eq, xw)>=xw and find_y_eq(cs_y_eq, xd)<=xd) or (find_y_eq(cs_y_eq, xw)<=xw and find_y_eq(cs_y_eq, xd)>=xd):
        print("Error:")
        print(f"The calculation cannot be performed successfully because the azeotropic point composition is between xW and xD")
        print(f"Change values ​​xW and/or xD and repeat the calculation")       
        return False
    else:
        return True
        
# Check if the first component is Low-Boiling component
def check_if_first_comp_is_LB(xf, xw, xd, M_1, M_2, data, cs_y_eq):
    if xf>cs_y_eq(xf):
        new_data = 1-data
        is_changed=1
        cs_y_eq = equlibrium_data_regression(new_data)
        
        M_1_temp = M_1
        M_1 = M_2
        M_2 = M_1_temp

        xf = 1- xf
        xw_temp = 1- xd
        xd = 1- xw
        xw = xw_temp
       
        return new_data, xf, xw, xd, M_1, M_2, cs_y_eq, is_changed

    else:
        is_changed=0
        return data, xf, xw, xd, M_1, M_2, cs_y_eq, is_changed
    
def find_components_separation_conditions(xw, xf, xd, M_1, M_2, Gf, is_changed):
    xd_mas=xd*M_1/(xd*M_1+(1-xd)*M_2)
    xf_mas=xf*M_1/(xf*M_1+(1-xf)*M_2)
    xw_mas=xw*M_1/(xw*M_1+(1-xw)*M_2)

    Gd = Gf*(xf_mas-xw_mas) / (xd_mas-xw_mas)
    Gw = Gf*(xf_mas-xd_mas) / (xw_mas-xd_mas)
    if is_changed==0:
        print(f"Component #1 is a low-boiling component at xf={xf}")
        print(f"   \t\t\t Mole fractions: \t Mass fractions:")
        print(f"    - Feed: \t\t xf={xf:.3f} \t\t xf_mas={xf_mas:.3f}   ")
        print(f"    - Distillate: \t xd={xd:.3f} \t\t xd_mas={xd_mas:.3f}   ")
        print(f"    - Bottmoms: \t xw={xw:.3f} \t\t xw_mas={xw_mas:.3f}   ")
        
        print(f"\nIf the Feed mass flow rate Gf={Gf} \n   - Distillate: Gd={Gd:.3f} \n   - Bottmoms: Gw={Gw:.3f}")
    else:
        print(f"Component #1 is a high-boiling component at xf={1-xf}")
        print(f"   (Concentrations xW and xD are reversed for the bottoms and distillate!)")

        print(f"   \t\t\t Mole fractions: \t Mass fractions:")
        print(f"    - Feed: \t\t xf={1-xf:.3f} \t\t xf_mas={1-xf_mas:.3f}   ")
        print(f"    - Distillate: \t xd={1-xd:.3f} \t\t xd_mas={1-xd_mas:.3f}   ")
        print(f"    - Bottmoms: \t xw={1-xw:.3f} \t\t xw_mas={1-xw_mas:.3f}   ")        
        print(f"\nIf the Feed mass flow rate Gf={Gf} \n   - Distillate: Gw={Gd:.3f} \n   - Bottmoms: Gd={Gw:.3f}")
        
    print(f"\nYield of low-boing compounent in distillate: Gd*xd_mas/(Gf*xf_mas)*100% = {(Gd*xd_mas/(Gf*xf_mas)*100):.2f}%")
    return xd_mas, xf_mas, xw_mas, Gd, Gw

def find_R_min(cs_y_eq, xd,xf):
    R_min = (xd - find_y_eq(cs_y_eq, xf))/(find_y_eq(cs_y_eq, xf)-xf)
    if R_min<0:
        print(f"\nFailed to calculate minimum reflux ratio R_min (R_min<0) due to the closeness ​​of xD and xF (equilibrium y(xF) > xD)")
    else:
        print(f"\nMinimum reflux ratio R_min = {R_min:.3f}")
    return R_min

#Recommended operating reflux ratio
def find_recommended_R_operating(R_min, R_UD):
    if R_min >0:
        R_recommended = 1.2*R_min+0.3
        print(f"Recommended reflux ratio: R = 1.2*R_min+0.3 = {(R_recommended):.3f}")
        
    if R_UD>R_min and R_UD>0:
        R=R_UD
        print(f"Since R_UD > R_min, the operating reflux ratio is fixed at: R = R_UD = {(R_UD):.3f}")
    elif R_min>0:
        R=1.2*R_min+0.3
        print(f"Since R_UD < R_min, the operating reflux ratio is fixed at recommended value: R = {R_recommended:.3f}")
    else:
        R=0.5
        print(f"Since R_min < 0, the operating reflux ratio is fixed at positive value: R = 0.5")
    return R

# Fing y-values for operating Line
def find_y_operating(x_data,xd,xf,xw,R,F):
    y_operating = np.zeros(len(x_data))
    for i in range(len(x_data)):
        x=x_data[i]
        if x<=xf:
            y_operating[i]=(F+R)/(R+1)*x - (F-1)/(R+1)*xw
        if x>xf:
            y_operating[i]=(R)/(R+1)*x + xd/(R+1)   
    return y_operating

# Fing x-values for operating Line
def find_x_operating(y_data,xd,xf,xw,R,F):
    x_operating = np.zeros(len(y_data))
    for i in range(len(y_data)):
        y = y_data[i]
        if y <= find_y_operating([xf],xd,xf,xw,R,F):
            x_operating[i]= (R+1)/(F+R)* y + (F-1)/(F+R)*xw
        if y > find_y_operating([xf],xd,xf,xw,R,F):
            x_operating[i]= (R+1)/(R)* y - xd/R
    return x_operating


def find_N_theoretical_Stages(cs_y_eq, xd,xf,xw,R,F,R_min):
    i=0
    n=0
    x_stages=[xd]
    y_stages=[xd]
    print(f"R={R:.3f}:")
    if R<R_min:
        print("  Error: R<R_min")
    else:    
        while x_stages[i]>xw:
            x_stages.append(find_x_eq(cs_y_eq, y_stages[i]))
            y_stages.append(y_stages[i])      
            i=i+1
            n=n+1
            if x_stages[i]<=xf and x_stages[i-1]>=xf:
                print(f"  - n_feed: {n}")            
            x_stages.append(x_stages[i])
            y_stages.append(*find_y_operating([x_stages[i]],xd,xf,xw,R,F))
            i=i+1                
            if i>400:
                print("  Error: number of theoretical stages n > 200")
                break
    if n < 200 and n>0:
        print(f"  - n: {n}")
    x_stages = np.array(x_stages)
    y_stages = np.array(y_stages)
    return x_stages, y_stages
    

def draw_plot(x_stages, y_stages, cs_y_eq, data,xd,xf,xw,R,F,is_changed):
    # Line of 45°
    plt.plot([0,1], [0,1], 'k--')

    x_axis = np.linspace(0,1,401)
    y_axis_eq=[]
    for i in x_axis:
        y_axis_eq.append(find_y_eq(cs_y_eq, i))
    y_axis_eq=np.array(y_axis_eq)
        
    x_axis_operating_line = np.array([xw,xf,xd])
    y_axis_operating_line = find_y_operating(x_axis_operating_line,xd,xf,xw,R,F)
    
    if is_changed==0:
        # Vertical lines for xW, xF, xD
        plt.plot(np.array([xw,xw]), np.array([0,*find_y_operating([xw],xd,xf,xw,R,F)]), 'y-', label="Line for xW")
        plt.plot(np.array([xf,xf]), np.array([0,*find_y_operating([xf],xd,xf,xw,R,F)]), 'r-', label="Line for xF")
        plt.plot(np.array([xd,xd]), np.array([0,*find_y_operating([xd],xd,xf,xw,R,F)]), 'm-', label="Line for xD")
        # Equilibrium Curve           
        plt.plot(x_axis, y_axis_eq, 'g-', label="Equilibrium Curve")
        # Stripping and Rectifying Lines    
        plt.plot(x_axis_operating_line, y_axis_operating_line, 'b-', label="Stripping and Rectifying Lines")
        # Equilibrium Curve Points    
        plt.plot(data[:,0], data[:,1], 'r.')
        # Stages
        plt.plot(x_stages, y_stages, 'k-', label="Stages")

    else:
        # Vertical lines for xW, xF, xD
        plt.plot(np.array([1-xd,1-xd]), 1-np.array([0,*find_y_operating([xd],xd,xf,xw,R,F)]), 'y-', label="Line for xW")
        plt.plot(np.array([1-xf,1-xf]), 1-np.array([0,*find_y_operating([xf],xd,xf,xw,R,F)]), 'r-', label="Line for xF")
        plt.plot(np.array([1-xw,1-xw]), 1-np.array([0,*find_y_operating([xw],xd,xf,xw,R,F)]), 'm-', label="Line for xD")
        # Equilibrium Curve      
        plt.plot(1-x_axis, 1-y_axis_eq, 'g-', label="Equilibrium Curve")
        # Stripping and Rectifying Lines
        plt.plot(1-x_axis_operating_line, 1-y_axis_operating_line, 'b-', label="Stripping and Rectifying Lines")
        # Equilibrium Curve Points    
        plt.plot(1-data[:,0], 1-data[:,1], 'r.')
        # Stages
        plt.plot(1-x_stages, 1-y_stages, 'k-', label="Stages")

    plt.xlabel("Mole fraction of component #1 in the liquid phase")
    plt.ylabel("Mole fraction of component #1 in the vapor phase")
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.grid()
    plt.legend()
    plt.show()

  
def main(equlibrium_data_fileName, xw, xf, xd, R_UD, Gf, R_test):
    M_1, M_2, data = define_equlibrium_data(equlibrium_data_fileName)

    cs_y_eq = equlibrium_data_regression(data)
    
    if check_azeotrope_condition(cs_y_eq, xw, xd):
        data, xf, xw, xd, M_1, M_2, cs_y_eq, is_changed = check_if_first_comp_is_LB(xf, xw, xd, M_1, M_2, data, cs_y_eq)   

        xd_mas, xf_mas, xw_mas, Gd, Gw = find_components_separation_conditions(xw, xf, xd, M_1, M_2, Gf, is_changed)        
        F=(xd-xw)/(xf-xw)
        R_min = find_R_min(cs_y_eq, xd,xf)
        R = find_recommended_R_operating(R_min, R_UD)
       
        print(f"\nTheoretical stages calculation \n(results will be used to plot the operating line of diagram)")
        print(f"  n_feed - recommended feed stage")
        print(f"  n - number of theoretical stages")
        x_stages, y_stages = find_N_theoretical_Stages(cs_y_eq, xd,xf,xw,R,F,R_min)

        if len(R_test)>0:
            print("")
            print(f"\nTheoretical stages calculation \n(for a range of reflux ratio values in R_test)") 
            for i in R_test:
                find_N_theoretical_Stages(cs_y_eq, xd,xf,xw,i,F,R_min)
        
        draw_plot(x_stages, y_stages, cs_y_eq, data,xd,xf,xw,R,F,is_changed)


