#!/usr/bin/env python
# coding: utf-8

import sys
import time
import numpy as np
import pandas as pd
from fastapi import FastAPI
from typing import List
import math

import uvicorn

app = FastAPI(description=__name__)

sys.path.append('../../')

from mockup_base_model import *

app = FastAPI(description=__name__)

# ################
# DEME mockup main ###
# ################

################ GLOBAL VARIABLES ###################
estimate_post_count = 0
mockup_periodicity_max_value = 20
mockup_periodicity_default = 10
mockup_periodicity = mockup_periodicity_default
detection_counter = 0
dfConfiguration = None
listOfDetectionForIteration = []
############### GLOBAL VARIABLES ###################

# def mockup_config():
#     return True

def gaussian(x, A, m, s):
    result = A * math.exp(-((x - m)**2) / (2 * s**2))
    return round(result, 1) 

def prepare_mocked_detection_results(dfConfiguration):
    global mockup_periodicity, listOfDetectionForIteration
    print("================================")
    print("\nConfiguration received:\n")
    print(dfConfiguration)
    print("================================")
    # gaussian parameters
    m = mockup_periodicity/2  # mean
    s = 1.5                 # standard deviation
    x_values = [i for i in range(mockup_periodicity)]  # values from 0 to mockup_periodicity-1 included

    dfNew = dfConfiguration[dfConfiguration.columns[:2]].copy()
    for index, row in dfConfiguration.iterrows():
        for column in dfConfiguration.columns[1:]:
            mapping = {True: [gaussian(x, 0.9, m, s) for x in x_values], False: [5, 6, 7], False: np.round(np.random.rand(mockup_periodicity) * 0.3, 1)}
            dfNew[column] = dfConfiguration[column].map(mapping)

    print("\nPrepared accuracy for instances and features configured:\n")
    print(dfNew)
    print("================================\n\n")
    listOfDetectionForIteration = []
    for iteration in range(mockup_periodicity):
        listOfDetection = []
        for index, row in dfNew.iterrows():
            attacks = []
            attack = None
            for column in dfNew.columns[1:]:
                if attack == None:
                    attack = Attack(attack=column, accuracy=row[column][iteration])
                else:
                    if attack.accuracy < row[column][iteration]:
                        attack = Attack(attack=column, accuracy=row[column][iteration])
            attacks.append(attack)
            detection = Detection(instance=row['instanceName'], detection=attacks)
            listOfDetection.append(detection)

        listOfDetectionForIteration.append(listOfDetection)

def get_mocked_detection(detection_counter):
    return listOfDetectionForIteration[detection_counter]

# readiness probe
@app.get("/is_ok", response_model=IsOK)
def is_deme_mockup_ok():
    """
        This endpoint verifies DEME mockup is up and running.

        Returns:
        - JSON response IsOK.
    """
    return IsOK

@app.post("/deme_mockup_configure", response_model=DoneResponse)
def mockup_configure(mockupConfiguration:MockupConfiguration):
    """
        This POST prepare mocked attacks confidence for each network instance and network feature passed within the parameter.
        These mocked attacks confidence will be returned to each GET/detection invoked.
        These mocked attacks confidence will be mockup_periodicity   each mockup_periodicity to each GET/detection invoked.
        For the feature and the instance where attack_simulation is False the attacks confidences will be always very low.
        For the feature and the instance where attack_simulation is True the attacks confidences will be 0.9 near the .
        The mocked attacks confidence will be different for the first mockup_periodicity GET/detection invoked than will be the same.

        Request Body:
        - A MockupConfiguration object

        Returns:
        - JSON response DoneResponse if mockup_periodicity is less than 20
        - JSON response ErrorConfigResponse otherwise
    """
    global dfConfiguration, mockup_periodicity, mockup_periodicity_max_value, detection_counter, listOfDetectionForIteration
    print("\n\n================================>>>>> Received POST /deme_mockup_configure <<<<<============================")
    mockup_periodicity = mockupConfiguration.mockup_periodicity
    if mockup_periodicity > mockup_periodicity_max_value:
        print("\nERROR: mockup_periodicity maximum value (20) exceeded\n\n")
        return DoneResponse(value="ERROR: max value allowed for mockup_periodicity is 20")
    elif mockup_periodicity <= 0:
        print("\nERROR: mockup_periodicity cannot be 0 or less\n\n")
        return DoneResponse(value="ERROR:  mockup_periodicity cannot be 0 or less")
    # initialization
    detection_counter = 0
    dfConfiguration = None
    listOfDetectionForIteration = []

    datafordataframe = []

    print("mock_periodicity received: " + str(mockup_periodicity))


    nodes_attacks_configuration = mockupConfiguration.attacks_configuration
    nodenamelist = []
    featurenamelist = []

    for node_item in nodes_attacks_configuration:
        datafordataframeRow = []
        nodenamelist.append(node_item.instance)
        datafordataframeRow.append(node_item.instance)
        for attack_configuration in node_item.attack_configuration:
            if attack_configuration.feature not in featurenamelist:
                featurenamelist.append(attack_configuration.feature)
            value = attack_configuration.attack_simulation
            datafordataframeRow.append(bool(value))
        datafordataframe.append(datafordataframeRow)

    rowLen = len(datafordataframe[0])
    df_columns = ['instanceName']
    for i in range(rowLen-1):
        df_columns.append(featurenamelist[i])
    dfConfiguration = pd.DataFrame(datafordataframe, columns=df_columns)
    prepare_mocked_detection_results(dfConfiguration)
    return DoneResponse

@app.post("/estimate", response_model=DoneResponse)
def mockup_estimate(estimate:List[Estimate]):
    global detection_counter
    """
        This mocked post just execute a syntax checking on the input parameters.

        Request Body:
        - A list of Estimate object

        Returns:
        - JSON response DoneResponse.
    """
    print("\n\n================================>>>>> Received POST /estimate <<<<<============================")
    time.sleep(4)
    detection_counter += 1
    return DoneResponse

@app.get("/detection", description='', response_model=List[Detection])
def mockup_detection():
    """
        Returns the mocked confidence of an attack for each network instance and network feature passed within the last deme_mockup_configure POST.

        Returns:
        - A list of Detection objects.
    """
    global dfConfiguration, detection_counter
    print("\n\n================================>>>>> Received GET /detection <<<<<============================")
    if not listOfDetectionForIteration:
        print("\n\nWARN: deme_mockup_configure POST not send yet\n\n")
        return []
    detection_counter = detection_counter % mockup_periodicity
    serializable_detection = get_mocked_detection(detection_counter)
    print(" ===> DETECTION: " + str(serializable_detection))
    return serializable_detection

# def init():
#     mockup_config()


if __name__ == '__main__':
    #init()
    uvicorn.run(app, host="0.0.0.0", port=8091)
