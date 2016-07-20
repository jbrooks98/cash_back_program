Cash Back Program
===
Project:    Cash Back Program  
Author:     Jason Brooks  
Email:      jbrooks98@gmail.com  
Version:    1.0 
License:    GNU GPLv3  
Main:       accrual_payment.py  
Python:     2.7.6


Description
---
Customers are eligible to receive a percentage of money back each time they are invoiced.  After a certain amount of invoices a payment gets made to the customer.  Users will be prompted to enter addtional invoices for a customer until the threshold for an accrual payout is met:


- A customer is to recieve 5% accrual per invoice.
- Every 6th invoice a customer will get paid the total accrual amount they have accumulated

Sample output:
```
1: CustomerA
2: CustomerB
3: CustomerC
Choose a customer: 1
Enter invoice dollar amount: 900
An invoice has been created
Customer has not yet met the threshold for accrual payout
Enter invoice dollar amount: 500
Congrats CustomerA will get a payment in the amount of $70 from invoice ids 1,2

```


Installation
---
Only standard Python libraries are used. Python 2.7 is required.


Usage
---
In a terminal, from the project directory run:
`python accrual_payment.py

```

A SQLite database is initially created called `accrual_payments.db` to store. You can peform some basic table and data actions using the database api functions in the directory db_layer if you want to change the default data.

Configurations can be made in `accrual_conf.py`..  


Notes
---
- This is a basic prototype. More complex scenarios are not handled at this time.  
