from .models import *
from django.db.models import Sum

import datetime


def check_eligibility(customer, loan_amount, tenure, interest_rate):
    customer_loans = Loan.objects.filter(borrower=customer)

    credit_score = calculate_credit_score(customer_loans, customer, loan_amount)
    response = calculate_interest_rate(customer_loans, credit_score, interest_rate, customer)

    return credit_score, response['approval'], response['message'], response['corrected_interest_rate']

def calculate_credit_score(loan_data, customer, current_loan_amount):
    credit_score = 100

    # i. Past Loans paid on time
    paid_on_time_count = loan_data.aggregate(Sum('emis_paid_on_time'))['emis_paid_on_time__sum']
    credit_score -= paid_on_time_count/10  

    # ii. No of loans taken in past
    loans_taken_count = loan_data.count()
    credit_score -= loans_taken_count  

    # iii. Loan activity in current year
    current_year_activity = loan_data.count()  # Adjust the year
    credit_score -= current_year_activity  


    # v. If sum of current loans of customer > approved limit of customer, credit score = 0
    current_loans_sum = loan_data.aggregate(Sum('loan_amount'))['loan_amount__sum']
    if current_loans_sum + current_loan_amount > customer.approved_limit:
        credit_score = 0

    return max(credit_score, 0)  


def calculate_interest_rate(customer_loans, credit_score, interest_rate, customer):
    response_data = {}

    # If credit_rating > 50, approve loan
    if credit_score > 50:
        response_data['approval'] = True
        response_data['message'] = 'Loan approved'
        response_data['corrected_interest_rate'] = interest_rate
    # If 50 > credit_rating > 30, approve loans with interest rate > 12%
    elif 30 < credit_score <= 50:
        response_data['approval'] = True
        response_data['message'] = 'Loan approved with interest rate > 12%'
        response_data['corrected_interest_rate'] = max(12, interest_rate)

    # If 30 > credit_rating > 10, approve loans with interest rate > 16%
    elif 10 < credit_score <= 30:
        response_data['approval'] = True
        response_data['message'] = 'Loan approved with interest rate > 16%'
        response_data['corrected_interest_rate'] = max(16, interest_rate)
    # If 10 > credit_rating, don’t approve any loans
    else:
        response_data['approval'] = False
        response_data['message'] = 'Loan not approved'
        response_data['corrected_interest_rate'] = -1

    # Check if sum of all current EMIs > 50% of monthly salary, don’t approve any loans
    current_emis_sum = customer_loans.aggregate(Sum('monthly_payment'))['monthly_payment__sum']    
    if current_emis_sum and current_emis_sum > 0.5 * customer.monthly_salary:
        response_data['approval'] = False
        response_data['message'] = 'Loan not approved due to high EMIs'
        response_data['corrected_interest_rate'] = -1

    return response_data

