from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from .utils import check_eligibility


# Create your views here.

@api_view(['GET'])
def index(request):
    api = {
        'register': 'http://localhost:8000/register/',
        'customers': 'http://localhost:8000/customers/',
        'create-loan': 'http://localhost:8000/create-loan/',
        'view-loan': 'http://localhost:8000/view-loan/<int:pk>/',
        'view-loan/customer': 'http://localhost:8000/view-loan/customer/<int:pk>/',        
    }
    return Response(api)

class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save(approved_limit=round(36 * int(self.request.data['monthly_salary']) / 100000) * 100000 ) 


class CustomerListAPIView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer   



class LoanCreateAPIView(APIView):
    def post(self, request, format=None):
        try:
            loan_instance = LoanSerializer(data=request.data)
            print("Loan instance: ", loan_instance)
            if loan_instance.is_valid(raise_exception=True):
                print("Loan instance: ", loan_instance)
                print(LoanSerializer.Meta.fields)
                #print("Request.data: ", request.data)
                #print("Borrower: ", request.data['borrower'])
                customer = loan_instance.validated_data['borrower']
                print("Customer: ", customer)
                loan_instance.borrower = customer  

                loan_amount = float(request.data['loan_amount'])

                credit_score, approval, message, corrected_interest_rate = check_eligibility(customer, loan_amount, int(request.data['tenure']), float(request.data['interest_rate']))

                #print("Monthly payment1:", loan_instance.monthly_payment)
                loan_instance.interest_rate = corrected_interest_rate
                monthly_payment = int(round(loan_amount * (1 + corrected_interest_rate/100) / int(request.data['tenure'])))
                #print("Monthly payment2:", loan_instance.monthly_payment)
                loan_instance.save()

                loan_response = {
                    'loan_instance': loan_instance.data,
                    'credit_score': credit_score,
                    'loan_approved': approval,
                    'message': message,
                    'corrected_interest_rate': corrected_interest_rate,
                }

                return Response(loan_response, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           


class LoanListAPIView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanDetailAPIView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CustomerLoanListAPIView(APIView):
    def get(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        loans = Loan.objects.filter(borrower=customer)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(borrower=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

