#!/usr/bin/bash

export DJANGO_SETTINGS_MODULE=loan.settings

python save_customer.py && python save_loan.py