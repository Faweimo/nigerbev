from cgitb import html
import os
from re import template
from urllib import response
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from accounts.models import User

from process.models import LeaveRequest
  
