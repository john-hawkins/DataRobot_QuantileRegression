# IMPORT THE FILE: QuantileRegression.py
import QuantileRegression as qr
from tabulate import tabulate
import datarobot as dr
import pandas as pd

# ###################################################################################################
#  EXAMPLE DATA TAKEN FROM THE R PACKAGE 'insuranceData' - 
#  Insurance policy data for which we want to predict the claim costs
#  Note: I renamed the columns to make it easier to understand
# ###################################################################################################
df_raw = pd.read_csv('data/insuranceData.csv')

keep_cols = ["age","age_group","zone","vehicle_class","vehicle_age","bonus_class","duration","claim_cost"]

df = df_raw.loc[:,keep_cols]

target = 'claim_cost'
unique_index = 'UNIQUE_INDEX'
quant_target = 'COST_BELOW_THRESHOLD'
granularity = 100
proj_name = "QR_TEST_PROJECT"

# GET THE SUBSET OF RECORDS WITH NON-ZERO CLAIMS COST
newdf = df.loc[ df['claim_cost']>0].copy().reset_index()
test_df = newdf.loc[len(newdf)-10:,]
train_df = newdf.loc[0:500,]

quants = qr.generate_quantile_values(train_df, target, granularity)

training = qr.build_quantile_regression_dataset(train_df, target, quant_target, unique_index, quants)

# THIS CAN TAKE A WHILE AND WILL BLOCK EXECUTION
project = qr.run_quantile_regression(training, proj_name, quant_target, unique_index, 20)

# LETS SCORE AND TEST 
desired_quantiles = [0.2, 0.8]

results = qr.get_predicted_quantiles( test_df, project, unique_index, quants, desired_quantiles )

print( 
    tabulate( 
        results.loc[:,["claim_cost","Quantile_0.2","Quantile_0.8"]], 
        headers=['Claim Cost', 'Lower Quantile', 'Upper Quantile'], tablefmt='orgtbl' 
    )
)



