import django
import csv

django.setup()

from api_crs.models import * 

def save_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['First Name'] == '':
                break
            # Process each row and save to the Django model
            customer_instance = Customer(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=int(row['Age']),
                phone_number=int(row['Phone Number']),
                monthly_salary=int(row['Monthly Salary']),
                approved_limit=int(row['Approved Limit']),
            )
            customer_instance.save()

if __name__ == "__main__":
    csv_file_path = 'api_crs/Copy of customer_data.csv'  # Replace with the actual path to your CSV file
    save_csv_data(csv_file_path)
    print("CSV data saved to Django models.")
