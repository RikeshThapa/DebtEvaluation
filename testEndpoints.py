import requests
import pandas as pd
import numpy as np
import json
from datetime import timedelta

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
        return amountToPay
        
    #payment plan exists
    else:
        amountPaid = getAmountPaid(ppid)
        df = debtsdf.query("id=="+str(debtId))
        return df["amount"].iloc[0]

# assumption 
def getNextPaymentDueDate( debtId, debtsdf, ppdf, paymentsdf ):
    # debt_id 0; remaining_amount == 0 ; dd = null
    # debt_id 1; remaining_amout == 50; last pyment: 2020-08-08; next payment: last payment + 7 = 2020-08-15

    #implementation:
    queryDf = debtsdf.query("id=="+str(debtId))
    if( queryDf['is_in_payment_plan'].iloc[0] ):
        if( queryDf['remaining_amount'].iloc[0] > 0 ):
            ppid = queryDf['payment_plan_id'].iloc[0]
            # get greatest(last) date from paymentsDf by ppid
            mostRecentDate = getMostRecentPaymentDate(ppid, paymentsdf)
            # get installment_frequency increment from ppdf by debtid
            increment = getDayAddition( ppid, ppdf)
            # add installment frequency to greatest(last) payment date
            nextPaymentDueOn = mostRecentDate + timedelta(days=increment)
            return nextPaymentDueOn
        else:
            # debt has been paid off 
            return None
    else:
        # user is not on a payment plan yet
        return None

    return None

def getMostRecentPaymentDate( ppid, paymentsdf ):
    df = paymentsdf.query('payment_plan_id=='+str(ppid))
    most_recent_date = df['date'].max()
    return most_recent_date

def getDayAddition( ppid, ppdf):
    paymentsQuerydf = ppdf.query("id=="+str(ppid))
    installment_frequency = paymentsQuerydf['installment_frequency'].iloc[0]
    if(installment_frequency == "WEEKLY"):
        return 7
    else:
        return 14

## Composition function:
def returnPayload():
    debtsdf = getDebtsDF()
    ppdf = getPaymentPlansDF()
    paymentsdf = getPaymentsDF()

    # print(np.any(ppdf[:, 0] == debtsdf['id']))
    debtsdf['is_in_payment_plan'] = [isInPaymentPlan( debtId ) for debtId in debtsdf['id']]

    # Add payment plan id to debtsdf
    debtsdf['payment_plan_id'] = [getPaymentPlanID( debtId ) for debtId in debtsdf['id']]

    # remaining amout 
    debtsdf['remaining_amount'] = [getAmountToPay( debtId, debtsdf, ppdf ) for debtId in debtsdf['id']]

    # get final payment due on 
    debtsdf['next_payment_due_date'] = [getNextPaymentDueDate( debtId, debtsdf, ppdf, paymentsdf ) for debtId in debtsdf['id']]

    return [debtsdf, ppdf, paymentsdf]



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