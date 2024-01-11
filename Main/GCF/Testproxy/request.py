from urllib import response
import requests

url='https://europe-north1-mainproject-01.cloudfunctions.net/test-test'
file_path='/home/devboy/Downloads/waterDat.zip'

#open the file in the binary mode and send it within the payload
try:
    with open(file_path,'rb') as file:
        files={'file':(file.name,file,'application/zip')}
        response=requests.post(url,files=files)
        response.raise_for_status()
        #print the response from the function
        print(response.text)

#handles errors related to the HTTP request
except requests.exceptions.RequestException as e:
    print(f'HTTP Request Error {url}')


#Handles errors related to file operations
except IOError as e:
    print(f'An error occurred trying to read the file {file_path}')
