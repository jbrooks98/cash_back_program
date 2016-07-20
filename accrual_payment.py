#!/usr/bin/env python
import sys
from decimal import Decimal

from db_layer.customers_db_api import (
    get_all_customers, create_customer, get_customer_name
)
from db_layer.invoices_db_api import (
    get_accrual_payouts, create_invoice, update_invoice_accrual_paid_date
)


def create_new_customer():
    """
    Prompts the user to create a customer if none exists
    Args:
        N/A

    Returns:
        N/A
    """
    print "Create a customer"
    customer_name = raw_input("Enter the name of customer: ").strip()
    create_customer(str(customer_name))

    return


def select_customer():
    """
    Prompts the user to select an existing customer
    Args:
        N/A

    Returns:
        N/A
    """

    all_customers = get_all_customers()
    if not all_customers:
        create_new_customer()
        all_customers = get_all_customers()

    all_customers = dict(all_customers)
    for key, value in all_customers.items():
        print "{0}: {1}".format(key, value)

    while True:
        customer_id = raw_input("Choose a customer: ").strip()
        try:
            customer_id = int(customer_id)
            if customer_id in all_customers.keys():
                return customer_id
            else:
                raise ValueError()

        except ValueError:
            print 'Enter valid customer'


def create_customer_invoice(customer_id):
    """
    Prompts the user to create an invoice for the chosen customer
    Args:
        customer_id: id of the customer

    Returns:
        N/A
    """

    while True:
        try:
            invoice_amount = Decimal(
                raw_input("Enter invoice dollar amount: ").strip()
            )

            if invoice_amount <= 0:
                raise ValueError()

            result = create_invoice(customer_id, invoice_amount)

            if result:
                print "An invoice has been created"

            __pay_customer_accruals()

        except ValueError:
            print 'Enter a valid invoice amount'


def __pay_customer_accruals():
    """
    private function that tells the user when a customer has been paid the
    total amount of eligible accruals for their invoices
    Args:
        N/A

    Returns:
        N/A
    """

    accrual_payments = get_accrual_payouts()

    if not accrual_payments:
        print "Customer has not yet met the threshold for accrual payout"
        return

    for accrual_payment in accrual_payments:
        update_invoice_accrual_paid_date(accrual_payment['invoice_ids'])

        customer_name = get_customer_name(
            str(accrual_payment['customer_id']).strip()
        )

        print ("Congrats {customer} will get a payment in the amount of "
               "${amount} from invoice ids {invoice_ids}".format(
                customer=customer_name,
                amount=str(accrual_payment['total_accrual_amt']).strip(),
                invoice_ids=str(accrual_payment['invoice_ids']).strip()
                ))

    sys.exit()


if __name__ == '__main__':
    customer = select_customer()
    create_customer_invoice(customer)


