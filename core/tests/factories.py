import factory
import pytest
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from voucher.models import *


class PaymentRequisitionVoucherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentRequisitionVoucher 