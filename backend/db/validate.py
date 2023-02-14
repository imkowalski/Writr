import re


# Validate email
def validate_mail(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True

    return False

# Validate password
def validate_pass(password: str) -> bool:
    capital = False
    for ele in password:
        if ele.isupper():
            capital = True
            break
    number = any(char.isdigit() for char in password)
    length = False
    if len(password) >= 8:
        length = True
    
    return (capital and number and length)

# Validate username
def validate_username(username: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]{3,15}\b'
    if(re.fullmatch(regex, username)):
        return True

    return False

