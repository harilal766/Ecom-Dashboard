import requests
from datetime import datetime, timedelta, timezone
from helpers.messages import color_text
from helpers.file_ops import *
from dotenv import load_dotenv
import os
import time

success_codes = [200,202]
forbidden_codes = [403]
error_codes = [400,401,404,415,429,500,503]

load_dotenv()

# Replace these with your credentials

# find the current user and filter the credentials based on the username, the username should be unique

"""
from amazon.models import SPAPI_Credential
creds = SPAPI_Credential.objects.filter(user__username="Hari")
"""

REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SP_API_DEFAULT_MARKETPLACE = os.getenv("SP_API_DEFAULT_MARKETPLACE")

#SELLER_ID = "ACJLZEYR3QZJFCQ77FO2CO36MSZQ"
#DEVELOPER_ID = "-------"

#Oauth_authorization_URL = f"https://sellercentral.amazon.com/apps/authorize/consent?selling_partner_id={SELLER_ID}&developer_id={DEVELOPER_ID}&client_id={CLIENT_ID}"
#print(Oauth_authorization_URL)

#ORDER_ENDPOINT = "https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders"

def region_finder():
    pass
    
current_time = datetime.now()

def is_file_empty(filepath):
    data = dotenv_values(filepath)
    if len(data) == 0:
        color_text(message="This file is empty, please check",color='red')
        return True
    
def generate_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        # check if the env file exists...
        response = requests.post(url, headers= headers, data=data)
        if response.status_code in success_codes:
            color='green'
            #print(f"Response Content: {response.text}")  # Log server response
            response.raise_for_status()  # Raise error if response status isn't 200
            access_token = response.json().get("access_token")

            # Store the new token in to the env file before returning it.
            file_handler(filepath='.env',operation='update',
                field='ACCESS_TOKEN',updated_value=access_token)
            
            #color_text(message="access token -> env file",color='green')
            # request time -> json file
            filepath = dir_switch(win=win_sp_api_config,lin=lin_sp_api_config)
            field = "latest_access_token_request"
            file_handler(filepath=filepath,field=field,
                        operation='update',updated_value=current_time)
            # reading the env file 
            env_access_token = file_handler(filepath='.env',operation='read')['ACCESS_TOKEN']
            #color_text(message="access token time -> json file",color='green')
            
            if env_access_token == None:
                color_text(message="Access Token is empty.",color='red')
            else:
                color_text(message="New Access token generated.",color='green')
                print(env_access_token)
                return env_access_token
                
        else:
            color='red'
        color_text(f"Response Status Code: {response.status_code}\n{response.content}\nPaste the credentials directly from postman....",color=color)
        
        
    
    except requests.exceptions.RequestException as e:
        print(f"Access Token Error: {e}")
        return None

def get_or_generate_access_token():
    current_time = datetime.now()
    try:
        # initialization
        # Read the json file to get the time stamp
        data = file_handler(filepath=dir_switch(win=win_sp_api_config,lin=lin_sp_api_config),operation='read')
        last_request_time_str = data.get("latest_access_token_request",None)

        if last_request_time_str != None:
            last_request_time = datetime.fromisoformat(last_request_time_str)
            difference_seconds = int((current_time - last_request_time).total_seconds())
            limit = 3600

            last_request_time = last_request_time.strftime("%H:%M:%S")
            current_time = current_time.strftime("%H:%M:%S")
            color_text(message=f"{last_request_time} to {current_time} = {difference_seconds} seconds,",color='blue',end=" ")
            
            # if the access token is expired or access token field is empty.  
            delay = 2
            if (difference_seconds > limit):
                color_text(message="Access token expired.",color='red')
                # generate a new one.
                new_access_token = generate_access_token()
                return new_access_token
            else:
                if difference_seconds < 0:
                    color_text(message="-ve time difference found, refreshing access token",color="red")
                    return generate_access_token()
                else:
                    color_text(message=f"Token expiring in {limit - difference_seconds} seconds.",color='green')
                    # extract the access token value from the env file and return it
                    previous_access_token = os.getenv('ACCESS_TOKEN')
                    #color_text(message=f"ACCESS TOKEN :\n{previous_access_token}++++++",color='red')
                    # Status message for old token
                    return previous_access_token
# ERRORS --------------------------------------------------------------------------------
        else:
            color_text(message="No timestammp found in the file.",color="red")
            return None
    except Exception as e:
        better_error_handling(e)
    
def rate_limit_checker(response):
    print(response.headers)