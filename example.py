# IMPORT THE FILE: QuantileRegression.py
import QuantileRegression as qr
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
granularity = 20
proj_name = "QR_TEST_PROJECT"

# TRIM OFF THE LAST 10 RECORDS FOR EVALUATION
test_df = df.loc[len(df)-10:,]

# JUST USE 10K FOR THIS EXAMPLE
# train_df = df.loc[0:len(df)-11,]
train_df = df.loc[0:2000,]

quants = qr.generate_quantile_values(train_df, target, granularity)

training = qr.build_quantile_regression_dataset(train_df, target, quant_target, unique_index, quants)

# THIS CAN TAKE A WHILE AND WILL BLOCK EXECUTION
# TODO: CREATE A VERSION THAT RETURNS AND PROVIDES A POLLING FUNCTION

project = qr.run_quantile_regression(training, proj_name, quant_target, unique_index, 20)

project_id = '5d00545dd9436e06620c7bd7'
project = dr.Project.get( project_id )

scored = qr.score_quantiles( test_df, project, unique_index, quants, quant_target )

desired_quantiles = [0.1, 0.9]

results = get_predicted_quantiles( test_df, project, unique_index, quants, desired_quantiles )




