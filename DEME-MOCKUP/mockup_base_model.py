#!/usr/bin/env python
# coding: utf-8

from pydantic import BaseModel, Field
from typing import List

############### BASE MODEL CLASSES FOR FASTAPI ###################
class IsOK(BaseModel):
    message: str = "ok"

############### /mockupConfiguration ###################
class AttackSimulationConfiguration(BaseModel):
    feature:str = Field(..., description='The type of network feature', example='NTP')
    attack_simulation:bool = Field(..., description='A boolean indicating the attack simulation', example=True)

class AttackConfiguration(BaseModel):
    instance:str = Field(..., description='The network instance name', example='Test_Instance')
    attack_configuration: List[AttackSimulationConfiguration] = Field(...,description='List of AttackSimulationConfiguration objects (feature name and related attack simulation info)', example='[{"feature": "NTP","attack_simulation": True},{"feature": "DNS","attack_simulation": False},{"feature": "PFCP","attack_simulation": False}]}]')

class MockupConfiguration(BaseModel):
    mockup_periodicity:int = Field(..., description='number of GET/detection cycles', example=10)
    attacks_configuration:List[AttackConfiguration] = Field(...,description='List of AttackConfiguration objects (instance name and related features)', example='[{"instance": "Test_Instance","attack_configuration": [{"feature": "NTP","attack_simulation":"True"},{"feature": "DNS","attack_simulation": "False"},{"feature": "PFCP","attack_simulation": "False"}]}]')
############### /mockupConfiguration ###################

############### /detection ###################
class Attack(BaseModel):
    attack:str = Field(..., description='The type of attack', example='NTP')
    accuracy:float = Field(...,description="The accuracy of the prediction of the attack", example=0.5)

class Detection(BaseModel):
    instance:str = Field(..., description='The instance name', example='Test_Instance')
    detection: List[Attack] = Field(...,description='List of Attack objects (attacks and related accuracies)', example='[{"attack":"NTP","accuracy":0.5}]')
############### /detection ###################

############### /estimate ###################
class Feature(BaseModel):
    feature:str = Field(..., description='The type of network feature', example='NTP')
    value:float = Field(..., description='The value associated to a network feature at a specific instant', example=141.0)

class Instance(BaseModel):
    instance:str = Field(..., description='The instance name', example='Test_Instance')
    features:List[Feature] = Field(...,description='List of Feature objects (network features and related values)', example='[{"feature": "NTP","value": 141.0},{"feature": "DNS","value": 125.0},{"feature": "PFCP","value": 138.0}]}]')

class Estimate(BaseModel):
    timestamp: str = Field(..., description='The timestamp in Unix epoch format', example='1713303373')
    instances:List[Instance] = Field(...,description='List of Instance objects (instances name and related features).', example='[{"instance": "Test_Instance","features": [{"feature": "NTP","value": 141.0},{"feature": "DNS","value": 125.0},{"feature": "PFCP","value": 138.0}]}]')
############### /estimate ###################

class DoneResponse(BaseModel):
    value: str = "done"

class TrueResponse(BaseModel):
    value: str = "true"

############### BASE MODEL CLASSES FOR FASTAPI ###################