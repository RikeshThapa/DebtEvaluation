Author: Rikesh Thapa
Date: April 22 2021

Requirements: 
- Python 3 (although python 2 should work)
- requests: for getting endpoints
- pandas: df manipulation
- numpy: series manipulation
- json
- datetime

Project Structure
- is very straightforward
- TrueAccord:
    - get_debts.py  > comprises main function along with helper functions
    - routes.py > module for pulling respective endpoints
    - test_get_debts.py > testing suite
    - readme.txt

Running the project:
- pip install -r requirements.txt : install dependencies
- python get_debts.py : execute main function for purpose of exercise 
- python test_get_debts.py: execute test suite

Implementation:
- I chose to go with pandas as the tool for converting JSON to JSON Lines format as the size is smaller. 
Not significantly, but this can matter. Pandas is shorter (no spaces) whereas JSONLines package includes spaces.
- Furthermore doing bid data manipulation (whihch I suspect is the purpose of this dataset) can be easie in pandas/ numpy due to the tools available in the library

Problems:
   1) get_debts.py in returnPayload() line 98
      in: HTTP API endpoints provided 
      out: debts to stdout 
         - All the Debt object fields returned by the API
         - is_in_payment_plan : 
               - true: debt is associated with an active payment plan
               - false: there is no payment plan, or the payment plan is completed
      
   2) test_get_debts.py 
      test suite: validate output being produced; other operations performed internally
   3) get_debts.py in returnPayload()
      Add new fields to Debt objects in output:
         - remaining_amount : calculated amount ramaining to be paid on the debt
         - line 104 
   4) get_debts.py in returnPayload() line 107
      Add new field to Debt object in output:
         - next_payment_due_date:
               - containing ISO 8601 UTC date (i.e. "2019-09-07") of when the next payment is due
               - null if there is no payment plan of if debt has been paid off
            - calculated:
               - payment plan start_date and installment_frequency --> is the next installment date after the last payment even if it is in the past

Assumptions:
- In calculating next payment due on I have ignored the possibility of bank holidays and included weekends as possible payment due days.

Testing:
- unittest from Python Standard library has been used for purposes of testing
- Here we test every function that the return function relies on

Improvements
- Creating a full project out of this code would be the logical next steps
- At present I use no error handling due to time constraints even simple try-catch blocks will help prevnt basic errors in how data is received and handled
- There is no Async/Await structure; everything is sequential; Setting up a proper structure will greatly improve code quality
- My Pandas df manipulation and implementation can be greatly improved-- I call a for loop over the same data set in lines 98, 101, 104, 107 and 110. This naturally is as imeffecient as the process gets. We can manipulate all of these objects at once 