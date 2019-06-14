# IMPORT THE FILE: QuantileRegression.py
import QuantileRegression as qr
from tabulate import tabulate
import datarobot as dr
import pandas as pd

df = pd.read_csv('data/train.csv')


target = 'SalePrice'
unique_index = 'Id'
quant_target = 'SALE_BELOW_THRESHOLD'
granularity = 100
proj_name = "QR_BOSTON_HOUSING_PROJECT"

# GET THE SUBSET OF RECORDS WITH NON-ZERO CLAIMS COST
test_df = df.loc[len(df)-50:,]
train_df = df.loc[0:1000,]

quants = qr.generate_quantile_values(train_df, target, granularity)

training = qr.build_quantile_regression_dataset(train_df, target, quant_target, unique_index, quants)

# THIS CAN TAKE A WHILE AND WILL BLOCK EXECUTION
project = qr.run_quantile_regression(training, proj_name, quant_target, unique_index, 20)

# LETS SCORE AND TEST 
desired_quantiles = [0.2, 0.8]

results = qr.get_predicted_quantiles( test_df, project, unique_index, quants, desired_quantiles )

results['in_band'] = np.where( (results['Quantile_0.2']<results["SalePrice"]) & (results['Quantile_0.8']>results["SalePrice"]) ,1,0) 

print( 
    tabulate( 
        results.loc[:,["SalePrice","Quantile_0.2","Quantile_0.8"]], 
        headers=['SalePrice', 'Lower Quantile', 'Upper Quantile'], tablefmt='orgtbl' 
    )
)

print("---")
print( "Calibration: Quantile Gap", str( round(desired_quantiles[1]-desired_quantiles[0],2) ), 
       " Proportion in band: ", str(results['in_band'].mean()) 
     )


