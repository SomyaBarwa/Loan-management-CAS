import django
import csv
import datetime

django.setup()

from api_crs.models import * 

def save_csv_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Customer ID'] == '':
                break
            # Process each row and save to the Django model
            loan_instance = Loan(
                borrower=Customer.objects.get(id=row['Customer ID']),
                id=row['Loan ID'],
                loan_amount=int(row['Loan Amount']),
                tenure=int(row['Tenure']),
                interest_rate=float(row['Interest Rate']),
                monthly_payment=int(row['Monthly payment']),
                emis_paid_on_time=int(row['EMIs paid on Time']),
                date_of_approval=datetime.datetime.strptime(row['Date of Approval'], '%d-%m-%Y').strftime('%Y-%m-%d'),
                end_date=datetime.datetime.strptime(row['End Date'], '%d-%m-%Y').strftime('%Y-%m-%d'),
            )
            loan_instance.save()

if __name__ == "__main__":
    csv_file_path = 'api_crs/Copy of loan_data.csv'  # Replace with the actual path to your CSV file
    save_csv_data(csv_file_path)
    print("CSV data saved to Django models.")
