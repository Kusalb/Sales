from django.test import TestCase

# Create your tests here.
from passlib.handlers.pbkdf2 import pbkdf2_sha256

hased=  pbkdf2_sha256.hash("password")

print(hased)