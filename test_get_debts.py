import unittest
#from unittest.mock import patch

#importing get_gebts
#target = __import__("get_debts.py")
#get_debts = target.returnPayload
from get_debts import returnPayload

class testGetDebts(unittest.TestCase):

    def setUp(self):
        #Pull debts
        #Pull payment plans
        #Pull Payments
        pass
    
    def tearDown(self):
        pass

    def test_get_debts(self):
        #with path('employee.request.get') as mocked_get:
        #    mocked_get.return_value.ok = True
        #    mocked_get.return_value.text = 'Success'
        self.assertEqual(sum([1,2,3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
