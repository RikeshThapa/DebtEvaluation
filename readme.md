1) in: HTTP API endpoints provided 
   out: debts to stdout 
        - All the Debt object fields returned by the API
        - is_in_payment_plan : 
            - true: debt is associated with an active payment plan
            - false: there is no payment plan, or the payment plan is completed
2) test suite: validate output being produced; other operations performed internally
3) Add new fields to Debt objects in output:
        - remaining_amount : calculated amount ramaining to be paid on the debt
            - type: JSON number
            - if debt is associated iwth payment plan: subtract from the payment plan's amount_to_pay instead
            - in exchange for singing up for a payment plan, we allow reduced amount to satisfy the debt
            - all paments whether on-time or not contribute to paying off debt
4) Add new field to Debt object in output:
         - next_payment_due_date:
            - containing ISO 8601 UTC date (i.e. "2019-09-07") of when the next payment is due
            - null if there is no payment plan of if debt has been paid off
         - calculated:
            - payment plan start_date and installment_frequency --> is the next installment date after the last payment even if it is in the past



implementation:
- I chose to go with pandas as the tool for converting JSON to JSON Lines format as the size is smaller. 
Not significantly, but this can matter. Pandas is shorter (no spaces) whereas JSONLines package includes spaces.

Assumptions:
- In calculating next payment due on I have ignored the possibility of bank holidays and included weekends as possible payment due days.