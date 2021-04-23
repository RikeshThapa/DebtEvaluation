import unittest
from datetime import datetime
#from unittest.mock import patch

#internal imports
from routes import getDebtsDF, getPaymentPlansDF, getPaymentsDF
from get_debts import returnPayload, isInPaymentPlan, getPaymentPlanID, getAmountToPay, getNextPaymentDueDate

class testGetDebts(unittest.TestCase):

    def setUp(self):
        #Pull debts
        self.debtsdf = getDebtsDF()
        #Pull payment plans
        self.ppdf = getPaymentPlansDF()
        #Pull Payments
        self.paymentsdf = getPaymentsDF()
    
    def test_is_in_payment_plan(self):
        self.assertEqual(isInPaymentPlan(0, self.ppdf), True, "Should be True")
        self.assertEqual(isInPaymentPlan(1, self.ppdf), True, "Should be True")
        self.assertEqual(isInPaymentPlan(4, self.ppdf), False, "Should be False")
         

    def test_get_payment_plan_id(self):
        self.assertEqual(getPaymentPlanID(0, self.ppdf), 0, "Should be 0")
        self.assertEqual(getPaymentPlanID(1, self.ppdf), 1, "Should be 1")
        self.assertEqual(getPaymentPlanID(4, self.ppdf), False, "Should be False")

    def test_get_amount_to_pay(self):
        self.assertEqual(getAmountToPay(0, self.debtsdf, self.ppdf, self.paymentsdf), 0, "Should be 0")
        self.assertEqual(getAmountToPay(1, self.debtsdf, self.ppdf, self.paymentsdf), 50, "Should be 50")
        self.assertEqual(getAmountToPay(4, self.debtsdf, self.ppdf, self.paymentsdf), 9238.02, "Should be 9238.02")

    def test_get_next_payment_due_date(self):
        self.debtsdf['is_in_payment_plan'] = [isInPaymentPlan( debtId, self.ppdf ) for debtId in self.debtsdf['id']]
        self.debtsdf['payment_plan_id'] = [getPaymentPlanID( debtId, self.ppdf ) for debtId in self.debtsdf['id']]
        self.debtsdf['remaining_amount'] = [getAmountToPay( debtId, self.debtsdf, self.ppdf, self.paymentsdf ) for debtId in self.debtsdf['id']]

        self.assertEqual(getNextPaymentDueDate(0, self.debtsdf, self.ppdf, self.paymentsdf), None, "Should be None")
        self.assertEqual(getNextPaymentDueDate(4, self.debtsdf, self.ppdf, self.paymentsdf), None, "Should be None")

if __name__ == '__main__':
    unittest.main()
