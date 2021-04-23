import requests
import pandas as pd
import numpy as np
import json


# Debts 
def getDebts():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts')
    debtsdf = pd.read_json(json.dumps(response.json()))
    debts = debtsdf.to_json(orient='records', lines=True)
    return debts

#For data manipulation purposes maintaining debts dataframe 
def getDebtsDF():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts')
    debtsdf = pd.read_json(json.dumps(response.json()))
    return debtsdf

# payment plans 
def getPaymentPlans():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans')
    paymentPlansDf = pd.read_json(json.dumps(response.json()))
    paymentPlans = paymentPlansDf.to_json(orient='records', lines=True)
    return paymentPlans

def getPaymentPlansDF():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans')
    paymentPlansDf = pd.read_json(json.dumps(response.json()))
    return paymentPlansDf

def getPayments():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments')
    paymentsDf = pd.read_json(json.dumps(response.json()))
    payments = paymentsDf.to_json(orient='records', lines=True)
    return payments

def getPaymentsDF():
    response = requests.get('https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments')
    paymentsDf = pd.read_json(json.dumps(response.json()))
    return paymentsDf