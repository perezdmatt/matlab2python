import warnings
import numpy as np
import matplotlib.pyplot as plt
sbioloadproject('insulindemo','m1')
ttings = warnings.warn('off','SimBiology:DimAnalysisNotDone_MatlabFcn_Dimensionless')
##
mealDose = sbioselect(m1,'Name','Single Meal')
set(mealDose,'Amount',75)
get(mealDose)
configset = getconfigset(m1,'active')
configset.StopTime = 7
configset.TimeUnits
normalMealSim = sbiosimulate(m1,configset,[],mealDose)
timedata = normalMealSim.Time
##
params = sbioselect(m1,'Type','parameter')
weight = 78
params(17).Value = weight
normalMealSim = sbiosimulate(m1,configset,[],mealDose)
plasmaGlu = normalMealSim.data(:,7)
##
weight = 90
params(17).Value = weight
normalMealSim = sbiosimulate(m1,configset,[],mealDose)
plasmaGluHeavy = normalMealSim.data(:,7)
plasmaGlu = plasmaGlu(np.arange(1,479+1))
plasmaGluHeavy = plasmaGluHeavy(np.arange(1,479+1))
H = horzcat(timedata,plasmaGlu,plasmaGluHeavy)
header = np.array(['Time','Normal Weight','Heavy Weight'])
output = np.array([[header],[num2cell(H)]])
str2 = 'aTest'
writematrix(output,strcat(str2,'.csv'))
##
basePlasma = 91.76
params(21).Value = basePlasma
normalMealSim = sbiosimulate(m1,configset,[],mealDose)
plasmaGlu = normalMealSim.data(:,7)
##
mealDose = sbioselect(m1,'Name','Single Meal')
for i in np.arange(1,10+1).reshape(-1):
    set(mealDose,'Amount',i)
    normalMealSim = sbiosimulate(m1,configset,[],mealDose)
    timedata = normalMealSim.Time
    plasmaGlu = normalMealSim.data(:,7)
    H = horzcat(timedata,plasmaGlu)
    str1 = string(i)
    str2 = 'NrmlCrbSim-'
    writematrix(H,strcat(str2,str1,'.csv'))

##
diabeticMealSim = sbiosimulate(m1,configset,[],mealDose)
for i in np.arange(1,10+1).reshape(-1):
    set(mealDose,'Amount',i)
    diabeticMealSim = sbiosimulate(m1,configset,[],mealDose)
    timedata = diabeticMealSim.Time
    plasmaGlu = diabeticMealSim.data(:,7)
    H = horzcat(timedata,plasmaGlu)
    str1 = string(i)
    str2 = 'Type2CrbSim-'
    writematrix(H,strcat(str2,str1,'.csv'))

##

##
outputNames = np.array(['Plasma Glu Conc','Plasma Ins Conc','Glu Prod','Glu Appear Rate','Glu Util','Ins Secr'])
figure
for i in np.arange(1,np.asarray(outputNames).size+1).reshape(-1):
    subplot(2,3,i)
    tNormal,yNormal = normalMealSim.selectbyname(outputNames[i])
    tDiabetic,yDiabetic = diabeticMealSim.selectbyname(outputNames[i])
    plt.plot(tNormal,yNormal,'-',tDiabetic,yDiabetic,'--')
    # Annotate figures
    outputParam = sbioselect(m1,'Name',outputNames[i])
    plt.title(outputNames[i])
    plt.xlabel('time (hour)')
    if str(outputParam.Type) == str('parameter'):
        plt.ylabel(outputParam.ValueUnits)
    else:
        plt.ylabel(outputParam.InitialAmountUnits)
    plt.xlim(np.array([0,7]))
    # Add legend
    if i == 3:
        plt.legend(np.array(['Normal','Diabetic']),'Location','Best')
