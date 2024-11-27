import re
from datetime import datetime

def check_name(name):
    # if name.isalpha():
    #     return 'valid'
    # else:
    #     return 'error'
    
    pattern = r"^[A-Za-z0-9]{4,15}$"
    if re.match(pattern,name):
        return "Valid "
    else:
        return "Not a valid"

    

def check_phnumber(num,alternativenumb=None):
    if len(num)!=10  or num[0] not in [6,7,8,9]:
        raise ValueError
    if num == alternativenumb:
        return "Valid "
    else:
        return "Both number should be the same"

    #pattern = ^[0-9]{10}$

def email_check(email):
    pattern=r"^[A-Za-z0-9.!-].+@[A-Za-z0-9!.-$]+\.[a-zA-z]{2,}$"
    if re.match(pattern,email):
        print('valid email')
    else:
        raise ValueError

    #local--afd , domainpart--@ ,main domain--.co

    if not '@' in email or email.count('@')!=1:
        print('not a valid')
    local,domain=email.split('@')

    if not local:
        print('add local part before @ ')
    
    if not domain.startswith('.') or domain.endswith('.'):
        return('add domain name')
    domain_part=email.split('.')

    if len(domain_part)<2:
        return 'Domain should have atlease one dot'
    
    else:
        return 'valid email'
    
def check_dob(dob):
    dob<= datetime.now()
