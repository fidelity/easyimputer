# Copyright 2020 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: GPL-3.0-only

import pandas as pd

import numpy as np

from sklearn.experimental import enable_iterative_imputer

from sklearn.impute import IterativeImputer,SimpleImputer,KNNImputer

import datawig

from missingpy import MissForest

import constant

class CSDImputer:
    def __init__(self,models = []):
        self.models = models
        self._supported_models_list = [constant.MEAN,constant.MEDIAN,constant.ITERATIVE,constant.RANDOM_FOREST,constant.KNN,constant.DATAWIG]
        
    def __performDataTypeValidations(self,df):
        return df.shape[1] == df.select_dtypes(include=np.number).shape[1]
    
    def __computeStatistics(self,df):
        statistics = {}
        corr_value = self.__computeCorrelation(df)
        missing_data = self.__computeMissingDataPercentage(df)
        statistics['Correlation'],statistics['Missing Data Percentage'],statistics['5 point summary'] = corr_value,missing_data,df.describe()
        return statistics

    def __computeCorrelation(self,df):
        new_df = df.dropna(how='any',axis=0)
        return new_df.corr()

    def __computeMissingDataPercentage(self,df):
        percent_missing = df.isnull().sum() * 100 / len(df)
        missing_value_df = pd.DataFrame({'Missing percentage': percent_missing})
        return missing_value_df

    def __computePercentageSimilarityOfMissingData(self,df):
        df1 = df.isna()
        df3 = pd.DataFrame(0, index=range(df1.shape[1]), columns=range(df1.shape[1]))
        for index in range(0,df1.shape[1]):
            for inner_index in range(index+1,df1.shape[1]):
                df2 = pd.crosstab(df1.iloc[:,index], df1.iloc[:,inner_index])
                if True in df2.columns and True in df2.index:
                    df3.iloc[index,inner_index] = df2.loc[True, True]
                    df3.iloc[inner_index,index] = df2.loc[True, True]
        df1 = df1[df1.values  == True]
        df1 = df1[~df1.index.duplicated(keep='first')]
        df3 = df3/df1.shape[0] * 100
        df3.columns = df3.index = df.columns
        return df3
        
    def _mean(self,df):
        imputer=SimpleImputer(missing_values=np.nan, strategy=constant.MEAN)  
        imputed_values=pd.DataFrame(imputer.fit_transform(df))
        imputed_values.columns = df.columns
        return imputed_values

    def _median(self,df):
        imputer=SimpleImputer(missing_values=np.nan, strategy=constant.MEDIAN)  
        imputed_values=pd.DataFrame(imputer.fit_transform(df))
        imputed_values.columns = df.columns
        return imputed_values

    def _iterative(self,df):
        imputer=IterativeImputer(max_iter=10, verbose=0) 
        imputed_values=pd.DataFrame(imputer.fit_transform(df))
        imputed_values.columns = df.columns
        return imputed_values

    def _random_forest(self,df): 
        imputer = MissForest(random_state=10) 
        imputed_values = pd.DataFrame(imputer.fit_transform(df))
        imputed_values.columns = df.columns
        return imputed_values
    
    def _knn(self,df):
        imputer = KNNImputer(n_neighbors=20)
        imputed_values =  pd.DataFrame(imputer.fit_transform(df))
        imputed_values.columns = df.columns
        return imputed_values
    
    def _datawig(self,df):
        imputed_values = datawig.SimpleImputer.complete(df)
        imputed_values.columns = df.columns
        return imputed_values
    
    def __impute(self,df,imputed_values,comments,models):
        supported_models_list = self._supported_models_list
        for model in models:
            if model.lower() in supported_models_list:
                imputed_df  = getattr(self, '_'+ model.lower())(df)
                imputed_values[model.lower()] = imputed_df
            else:
                comments.append('The model ' + model + ' is not supported.')
        if comments:
             comments.append('Support models are ' + str(supported_models_list))
        return imputed_values
    
    def __pick_best_models(self,num_columns,max_missing_data,max_similarity):
        if num_columns == 1:
           models = [constant.RANDOM_FOREST,constant.ITERATIVE,constant.DATAWIG]
        elif num_columns == 2:
            if max_missing_data < 25:
                models = [constant.RANDOM_FOREST,constant.ITERATIVE,constant.DATAWIG,constant.MEAN] if max_similarity >= 90 else [constant.RANDOM_FOREST,constant.ITERATIVE,constant.MEDIAN,constant.MEAN]
            else:
                models = [constant.RANDOM_FOREST,constant.MEAN] if max_similarity >= 90 else [constant.RANDOM_FOREST,constant.ITERATIVE,constant.MEAN]
        else:
            if max_missing_data < 25:
                models = [constant.RANDOM_FOREST,constant.ITERATIVE,constant.DATAWIG,constant.MEAN]
            else:
                models = [constant.RANDOM_FOREST,constant.ITERATIVE,constant.MEDIAN,constant.MEAN,constant.DATAWIG]
        return models
    
    def __data_based_impute(self,df,imputed_values,missing_data,missing_data_similarity,comments):
        num_columns = missing_data['Missing percentage'].fillna(0).astype(bool).sum(axis=0)
        max_missing_data = missing_data['Missing percentage'].max()
        if max_missing_data >= 40: 
             models = [constant.RANDOM_FOREST]
             comments.append('Atleast 40% of data is missing in one or more columns. Model may not give the best results.')
        else:
            models = self.__pick_best_models(num_columns,max_missing_data,missing_data_similarity.max().max())
        imputed_values =  self.__impute(df,imputed_values,comments,models)
        return imputed_values
    
    def impute(self,input_df):
        models = self.models
        statistics = {}
        missing_data_similarity = {}
        imputed_values = {}
        comments = []
        pass_value = self.__performDataTypeValidations(input_df)
        if pass_value:
            statistics = self.__computeStatistics(input_df)
            missing_data_similarity = self.__computePercentageSimilarityOfMissingData(input_df)
            if models:
                imputed_values = self.__impute(input_df,imputed_values,comments,models)
            else:
                imputed_values = self.__data_based_impute(input_df,imputed_values,statistics['Missing Data Percentage'],missing_data_similarity,comments)
        else:
            comments.append('Dataframe contains non-numeric columns. Cannot proceed')
        return statistics, imputed_values,comments
    
