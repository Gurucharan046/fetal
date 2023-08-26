# this is the main and final version of the backbone of our website.the fetal health predictor program
# the data and all other operations remains same but the mahor difference is with the number of attributes we are
# considering for our project is reduced to just 5 from 21. in other words the user can only give the 4 inputs.
# this program aims at gathering the minimum information from the user and predict with the same accuracy which
# we promised for the 21 inputs. Overall there is no change in functionality but the program has  reduced
# the workload on the user and also the interface will now be simpler and yet useful.

# version 1.1 Built by Gurucharan D K for the mini project on date: 06 april 2022
# changes need to be made on the predict_form.html by making the number of inputs 4 from 21
# no changes in the css file
# this fetal_predict2.py file will be soon going to be renamed as fetal_predict.py
# thereby this will be our main program.

import pandas as pd  # importing pandas for reading the csv file
# importing the RandomForestClassifier for our prediction
from sklearn.ensemble import RandomForestClassifier
# importing accuracy
from sklearn.metrics import accuracy_score
# importing train test split for prediction and other operations
from sklearn.model_selection import train_test_split


# reading the csv file
fetal_data = pd.read_csv('fetal_health.csv')
# removing the first row of the csv file
fetal_data = fetal_data.iloc[1:]
# keeping the features abnormal_short_term_variabiliity,mean_value_of_short_term_variability
# percentage_of_thime with_abnormal_long_term_activity ,histogram_mean and removing all other features.
fetal_data_x = fetal_data.drop(['fetal_health', 'baseline value', 'fetal_movement', 'uterine_contractions', 'light_decelerations', 'severe_decelerations', 'mean_value_of_long_term_variability',
                               'histogram_width', 'prolongued_decelerations',
                                'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
                                'histogram_number_of_zeroes', 'histogram_mode', 'histogram_median', 'histogram_variance', 'histogram_tendency'], axis=1)
# making the fetal_health a.k.a target variable for y
fetal_data_y = fetal_data['fetal_health']
# training the data with 70% testing the data with 30% with random state 40  using traintest split method
fetal_data_x_train, fetal_data_x_test, fetal_data_y_train, fetal_data_y_test = train_test_split(
    fetal_data_x, fetal_data_y, train_size=0.7, random_state=40)
# performing the RandomForestClassifier with no of elements as 100, out of box score as true , max dept as 5
fetal_health_classifier = RandomForestClassifier(
    random_state=40, n_jobs=-1, max_depth=5, n_estimators=100, oob_score=True)
# fitting our trained model with the x_train, y_train data
fetal_health_classifier.fit(fetal_data_x_train, fetal_data_y_train)
# developmet of function are yet to be carried out.


def fetalHealthPredictor(list):
    value = fetal_health_classifier.predict(list)
    return value


def getAverage():
    data = []
    data.append(fetal_data_x.accelerations.sum()/2127)
    data.append(fetal_data_x.abnormal_short_term_variability.sum()/2127)
    data.append(fetal_data_x.mean_value_of_short_term_variability.sum()/2127)
    data.append(
        fetal_data_x.percentage_of_time_with_abnormal_long_term_variability.sum()/2127)
    data.append(fetal_data_x.histogram_mean.sum()/2127)


getAverage()
