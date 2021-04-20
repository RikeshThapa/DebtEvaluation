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

def returnPayload():
    debtsdf = getDebtsDF()
    ppdf = getPaymentPlansDF()
    paymentsdf = getPaymentsDF()

    #print(np.any(ppdf[:, 0] == debtsdf['id']))
    debtsdf['is_in_payment_plan'] = [isInPaymentPlan( debtId ) for debtId in debtsdf['id']]

    #Add payment plan id to debtsdf
    debtsdf['payment_plan_id'] = [getPaymentPlanID( debtId ) for debtId in debtsdf['id']]

    #remaining amout 
    debtsdf['remaining_amount'] = [getAmountToPay( debtId, debtsdf, ppdf ) for debtId in debtsdf['id']]
    return [debtsdf, ppdf, paymentsdf]

#
# Helper Functions
#

def isInPaymentPlan( debtId ):
    ppdf = getPaymentPlansDF()
    if debtId in ppdf.loc[: , 'debt_id']:
        return True
    else:
        return False

def getPaymentPlanID( debtId ):
    ppdf = getPaymentPlansDF()
    if debtId in ppdf.loc[:, 'debt_id']:
        temp = ppdf.query("debt_id=="+str(debtId))
        return temp["id"].iloc[0]
    else:
        return False

# get amount paid so far by payment_plan_id
# return 0 if no payment plan 
def getAmountPaid( payment_plan_id ):
    paymentsdf = getPaymentsDF()
    amountPaid = paymentsdf.groupby(['payment_plan_id']).amount.sum()
    if payment_plan_id > -1 and np.issubdtype(type(payment_plan_id), int):
        print("internal function amount paid: ", amountPaid[payment_plan_id])
        return amountPaid[payment_plan_id]    
    else:
        return 0              

def getAmountToPay( debtId, debtsdf, ppdf ):
    ppid = getPaymentPlanID( debtId )
    # no payment plan and nothing has been paid
    if(ppid > -1 and np.issubdtype(type(ppid), int) ):        
        amountPaid = getAmountPaid(ppid)
        df = ppdf.query("id=="+str(ppid))
        amountToPay = df["amount_to_pay"].iloc[0] - amountPaid
        print("ppid: ", ppid)
        print(type(ppid))
        print("amountPaid: ", amountPaid)
        print("amountToPay: ", amountToPay)
        return amountToPay
        
    #payment plan exists
    else:
        amountPaid = getAmountPaid(ppid)
        df = debtsdf.query("id=="+str(debtId))
        return df["amount"].iloc[0]


def main():
    output = returnPayload()  
    print(output[0])
    print(output[1])
    print(output[2])

    ##Testing if debtId is in payment plan 
    #isInPaymentPlan(4)

    #Testing how much has been paid for a given payment plan id 
    #x = getAmountPaid(0)
    #print(x)
    
    return output

if __name__ == "__main__":
    main()