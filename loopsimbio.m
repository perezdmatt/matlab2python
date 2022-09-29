sbioloadproject('insulindemo', 'm1')
ttings = warning('off', 'SimBiology:DimAnalysisNotDone_MatlabFcn_Dimensionless');
%%
mealDose = sbioselect(m1, 'Name', 'Single Meal');
set(mealDose, "Amount", 75)
get(mealDose)
configset = getconfigset(m1, 'active');
configset.StopTime = 7;
configset.TimeUnits
normalMealSim= sbiosimulate(m1, configset, [], mealDose);
timedata = normalMealSim.Time
%%
params = sbioselect(m1,'Type','parameter')
weight = 78;
params(17).Value = weight;

normalMealSim= sbiosimulate(m1, configset, [], mealDose);
plasmaGlu = normalMealSim.data(:, 7);
%%
weight = 90;
params(17).Value = weight;

normalMealSim= sbiosimulate(m1, configset, [], mealDose);
plasmaGluHeavy = normalMealSim.data(:, 7);
plasmaGlu = plasmaGlu(1:479);
plasmaGluHeavy = plasmaGluHeavy(1:479);

H = horzcat(timedata, plasmaGlu, plasmaGluHeavy);
header = ["Time", "Normal Weight", "Heavy Weight"]
output = [header; num2cell(H)];
str2 = 'aTest';
writematrix(output, strcat(str2,'.csv'));
%%
basePlasma = 91.76;
params(21).Value = basePlasma;
normalMealSim= sbiosimulate(m1, configset, [], mealDose);
plasmaGlu = normalMealSim.data(:, 7);
%%
mealDose = sbioselect(m1, 'Name', 'Single Meal');
for i = 1:10
    set(mealDose, "Amount", i)
    normalMealSim= sbiosimulate(m1, configset, [], mealDose);
    timedata = normalMealSim.Time;
    plasmaGlu = normalMealSim.data(:, 7);
    H = horzcat(timedata, plasmaGlu);
    str1 = string(i);
    str2 = 'NrmlCrbSim-';
    writematrix(H, strcat(str2, str1,'.csv'));
end
%%
diabeticMealSim = sbiosimulate(m1, configset, [], mealDose);
for i = 1:10
    set(mealDose, "Amount", i)
    diabeticMealSim = sbiosimulate(m1, configset, [], mealDose);
    timedata = diabeticMealSim.Time;
    plasmaGlu = diabeticMealSim.data(:, 7);
    H = horzcat(timedata, plasmaGlu);
    str1 = string(i);
    str2 = 'Type2CrbSim-';
    writematrix(H, strcat(str2, str1,'.csv'));
end
%%

%%
outputNames = {'Plasma Glu Conc', 'Plasma Ins Conc', 'Glu Prod', ...
    'Glu Appear Rate', 'Glu Util', 'Ins Secr'};
figure;
for i = 1:numel(outputNames)
    subplot(2, 3, i);

    [tNormal, yNormal  ]  = normalMealSim.selectbyname(outputNames{i});
    [tDiabetic, yDiabetic]  = diabeticMealSim.selectbyname(outputNames{i});
    
    plot( tNormal    , yNormal   , '-'       , ... 
          tDiabetic  , yDiabetic , '--'      );
  
    % Annotate figures 
    outputParam = sbioselect(m1, 'Name', outputNames{i});  
    title(outputNames{i});
    xlabel('time (hour)');
    if strcmp(outputParam.Type, 'parameter')
        ylabel(outputParam.ValueUnits);
    else
        ylabel(outputParam.InitialAmountUnits);
    end
    xlim([0 7]);
    
    % Add legend
    if i == 3
        legend({'Normal', 'Diabetic'}, 'Location', 'Best');
    end
    
end