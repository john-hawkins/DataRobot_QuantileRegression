# IMPORT THE FILE: QuantileRegression.py
import QuantileRegression as qr
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
train_df = df.loc[0:10000,]

quants = qr.create_quantiles(train_df, target, granularity)

training = qr.build_quantile_regression_dataset(train_df, target, quant_target, unique_index, quants)

# THIS CAN TAKE A WHILE AND WILL BLOCK EXECUTION
# TODO: CREATE A VERSION THAT RETURNS AND PROVIDES A POLLING FUNCTION

qr.run_quantile_regression(training, proj_name, quant_target, unique_index, 4)



