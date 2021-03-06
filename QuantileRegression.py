import datarobot as dr
import pandas as pd
import numpy as np

# #######################################################################################
#
# CREATE THE VECTOR OF QUANTILES NEEDED FOR THE TRAINING DATASET GENERATION
# NOTE: THESE SHOULD BE SAVED TO DISK FOR USE ON SCORING DATA
# TODO: CREATE A CONFIG FILE WRITE AND READ FUNCTIONS TO TAKE CARE OF THE ABOVE
#
# #######################################################################################
def generate_quantile_values( df, target, granularity ):
    minval = min(df[target])
    maxval = max(df[target])
    delta = (maxval-minval)/granularity
    # GENERATE THE TARGET LEVELS WITH THE REQUIRE GRANULAITY
    # TODO: REPLACE WITH np.quantile() IF YOUR VERSION OF numpy SUPPORTS IT
    quantiles = [minval + delta*X for X in range(0,(granularity+1))]
    return quantiles

# #######################################################################################
#
# GENERATE A DATASET WITH A BINARY CLASSIFICATION TARGET THAT ACTS AS 
# TARGET FOR A QUANTILE REGRESSION PROJECT
# df:           The raw pandas dataframe
# target:       The real valued target that we want to generate quantile estimates for
# quant_target: The name for the new target variable
# unique_index: The name of the column that will uniquely identify rows in the raw dataset
# quantiles:    Array containing the set of real valued quantiles to predict. 
#               Usually generated by the function generate_quantile_values()
#
# #######################################################################################
def build_quantile_regression_dataset(in_df, target, quant_target, unique_index, quantiles):
    df = in_df.copy()
    # ADD A UNIQUE INDEX TO THE DATASET
    if(unique_index not in df.columns): 
        df[unique_index] = pd.Series( range(1,len(df)+1), index=df.index )

    # JOIN QUANTILES AGAINST THE DATASET IN AN OUTER JOIN THAT EXHAUSTIVELY
    # GENERATES ALL COMBINATIONS OF DATA AND QUANTILE
    qqdf = pd.DataFrame(data={'quantile':quantiles, 'joinr':1})
    df['joinr'] = 1
    newdf = pd.merge(df, qqdf, on='joinr', how='outer') 

    # NOW GO THROUGH AND GENERATE A BINARY CLASSIFICATION TARGET THAT INDICATES
    # WHETHER THE TARGET IS LESS THAN OR EQUAL TO THE QUANTILE
    newdf[quant_target] = np.where( newdf[target] <= newdf['quantile'], 1, 0 )

    # REMOVE UNNECCESSARY ROWS OR ONES THAT WILL CREATE TARGET LEAKAGE
    # newdf[target] = np.nan 
    newdf.drop([target,'joinr'], inplace=True, axis=1, errors='ignore')

    return newdf


# #######################################################################################
# ADD QUANTILES TO DATASET FOR SCORING
#
# df:           The raw pandas dataframe
# unique_index: The name of the column that will uniquely identify rows in the raw dataset
# quantiles:    Array containing the set of real valued quantiles to predict. 
#               Usually generated by the function create_quantiles
#
# #######################################################################################
def add_quantiles( df, unique_index, quantiles ):
    temp = df.copy()
    # ADD A UNIQUE INDEX TO THE DATASET IF REQUIRED
    if(unique_index not in temp.columns): 
        temp[unique_index] = pd.Series( range(1,len(temp)+1), index=temp.index )

    # JOIN QUANTILES AGAINST THE DATASET IN AN OUTER JOIN THAT EXHAUSTIVELY
    # GENERATES ALL COMBINATIONS OF DATA AND QUANTILE
    qqdf = pd.DataFrame(data={'quantile':quantiles, 'joinr':1})
    temp['joinr'] = 1
    newdf = pd.merge(temp, qqdf, on='joinr', how='outer') 

    # REMOVE UNNECCESSARY ROWS OR ONES THAT WILL CREATE TARGET LEAKAGE
    newdf.drop(['joinr'], inplace=True, axis=1, errors='ignore')
    return newdf

# #######################################################################################
#
# CREATE A DATAROBOT PROJECT TO BUILD THE QUANTILE REGRESSION PROJECT ON A DATASET 
# GENERATED BY THE FUNCTION ABOVE
#
# RETURN A REFERENCE TO THE PROJECT
#
# #######################################################################################
def run_quantile_regression( df, proj_name, quant_target, unique_index, workers ):
    proj = dr.Project.create( df, proj_name, max_wait = 9999 )
    group_partition = dr.GroupCV( holdout_pct = 0, reps = 10, partition_key_cols = [unique_index] )
    proj.set_target( target = quant_target, partitioning_method = group_partition, mode = dr.AUTOPILOT_MODE.FULL_AUTO, max_wait = 9999 )
    proj.set_worker_count( workers )
    proj.wait_for_autopilot()
    return proj

# #######################################################################################
# CREATE A SET OF PLOTS FOR THE QUANTILES OF NEW DATA 
# #######################################################################################
def generate_quantile_plot( df, project, unique_index, quantiles ):
    newdf = add_quantiles(df, quantiles)
    
# #######################################################################################
# SCORE A NEW DATA SET
# #######################################################################################
def score_quantiles( df, project, unique_index, quantiles ):
    newdf = add_quantiles( df, unique_index, quantiles )
    dataset = project.upload_dataset( sourcedata=newdf )
    # WE NEED A TRY CATCH AROUND THIS BECAUSE DATAROBOT DOES NOT GARANTEE
    # TO PROVIDE A RECOMMENDED MODEL
    try:
        model = dr.models.ModelRecommendation.get( project.id ).get_model()
    except (RuntimeError, TypeError, NameError, dr.errors.ClientError):
        model = project.get_models()[0]
    pred_job = model.request_predictions( dataset.id )
    preds = dr.models.predict_job.wait_for_async_predictions( project.id, predict_job_id=pred_job.id, max_wait=600 )
    newdf['prediction'] = preds['positive_probability']
    return newdf


# #######################################################################################
# GENERATE QUANTILES ON A NEW DATA SET
# #######################################################################################
def get_predicted_quantiles( df, project, unique_index, quantiles, desired_quantiles ):
    results = df.copy()
    # RETRIEVE THE RAW PROBABILITY SCORES
    scored = score_quantiles( df, project, unique_index, quantiles ) 
    # NOW GROUP BY THE UNIQUE INDEX AND CALCULATE THE QUANTILE VALUES AT THE REQUIRED POINTS ON THE DISTRIBUTION 
    grpd = scored.groupby(unique_index)
    for quant in desired_quantiles:
        col_name= "Quantile_" + str(quant)
        this_quant = grpd.apply( lambda x: min( x[ x['prediction'] >= quant ]['quantile'] ) )
        results[col_name] = this_quant.values
    return results


