import random
import string

pre_fix = ['NBL']
nums = random.randint(100,999)
ind = random.randint(0,9)

def client_uid():
    result =random.choice(pre_fix)

    return f'{result}/130/{ind}/{nums}'