from django.test import TestCase

from .models import *
from .utils import *

# Create your tests here.


class TestCustomer(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            age=25,
            phone_number=9876543210,
            monthly_salary=100000,
            approved_limit=300000,
        )

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(self.customer.__str__(), self.customer.first_name + " " + self.customer.last_name)

    def test_customer_approved_limit(self):
        self.assertEqual(self.customer.approved_limit, 300000)


class TestLoan(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            age=25,
            phone_number=9876543210,
            monthly_salary=100000,
            approved_limit=300000,
        )

        self.loan = Loan.objects.create(
            borrower=self.customer,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_payment=10000,
            emis_paid_on_time=0,
        )

    def test_loan_creation(self):
        self.assertTrue(isinstance(self.loan, Loan))
        self.assertEqual(self.loan.__str__(), self.loan.borrower.first_name + " " + self.loan.borrower.last_name + " " + str(self.loan.id))

    def test_loan_monthly_payment(self):
        self.assertEqual(self.loan.monthly_payment, 10000)


class TestCheckEligibility(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            age=25,
            phone_number=9876543210,
            monthly_salary=100000,
            approved_limit=300000,
        )

        self.loan = Loan.objects.create(
            borrower=self.customer,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_payment=10000,
            emis_paid_on_time=0,
        )

    def test_check_eligibility(self):
        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 10)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)
        self.assertEqual(message, 'Loan approved')
        self.assertEqual(corrected_interest_rate, 10)

        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 20)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)
        self.assertEqual(message, 'Loan approved')
        self.assertEqual(corrected_interest_rate, 20)

        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 30)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)
        self.assertEqual(message, 'Loan approved')
        self.assertEqual(corrected_interest_rate, 30)

        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 40)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)
        self.assertEqual(message, 'Loan approved')
        self.assertEqual(corrected_interest_rate, 40)

        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 50)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)
        self.assertEqual(message, 'Loan approved')
        self.assertEqual(corrected_interest_rate, 50)

        credit_score, approval, message, corrected_interest_rate = check_eligibility(self.customer, 100000, 12, 60)
        self.assertEqual(credit_score, 100)
        self.assertEqual(approval, True)


