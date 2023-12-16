from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def create(self, validated_data):
        validated_data['monthly_payment'] =  int(round(validated_data['loan_amount'] * (1 + validated_data['interest_rate']/100) / int(validated_data['tenure'])))
        return super().create(validated_data)
