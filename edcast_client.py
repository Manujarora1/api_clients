import os
import requests
from urllib.parse import quote
import jwt
import json

class EdcastSDK:
    def __init__(self, base_org_url, api_key, payload_email):
        """
        Initialize the SDK with the required credentials.

        Args:
        - base_org_url (str): Base organization URL
        - api_key (str): API key
        - payload_email (str): Email address for user

        Returns:
        None
        """
        self.base_org_url = base_org_url
        self.api_key = api_key
        self.x_auth_token = jwt.encode(payload_email, os.environ["api_secret"])
        self.jwt_token = self.authenticate()

    def authenticate(self):
        """
        Authenticate the user with the API.

        Args:
        None

        Returns:
        str: JWT token
        """
        headers = {
            "X-AUTH-TOKEN": self.x_auth_token,
            "X-API-KEY": self.api_key
        }
        url = self.base_org_url + "/api/developer/v5/auth"
        response = requests.get(url, headers=headers)
        response = response.json()
        return response["jwt_token"]

    def get_user_details(self):
        """
        Get details of a specific user.

        Args:
        None

        Returns:
        dict: User details
        """
        headers = {
            "X-ACCESS-TOKEN": self.jwt_token,
            "X-API-KEY": self.api_key
        }
        payload = {}
        url = "https://futureskillsprime.edcastpreview.com/api/developer/v5/profiles/manuj%40edcast%2Ecom"
        response = requests.get(url, headers=headers, data=payload)
        response = response.json()
        return response

    def get_user_list(self):
        """
        Get a list of all users.

        Args:
        None

        Returns:
        dict: List of users
        """
        headers = {
            "X-ACCESS-TOKEN": self.jwt_token,
            "X-API-KEY": self.api_key,
            'content-Type': 'application/json'
        }
        payload = {}
        url = self.base_org_url + "/api/developer/v5/profiles?limit=10&offset=0"
        response = requests.get(url, headers=headers, data=payload)
        response = response.json()
        return response

    def create_user(self, email):
        """
        Create a new user.

        Args:
        - email (str): Email address for the new user

        Returns:
        dict: Details of the created user
        """
        headers = {
            "X-ACCESS-TOKEN": self.jwt_token,
            "X-API-KEY": self.api_key,
            'content-Type': 'application/json'

#to create accounts for testing
  def create_user(self,email):
    headers={
        "X-ACCESS-TOKEN":self.jwt_token,
        "X-API-KEY": self.api_key,
        'content-Type':'application/json'
    }
    first_name=email.split("@")[0]
    last_name="."
    external_id=email+first_name
    payload = json.dumps({
                          "profiles": [
                                        {
                                          "external_id": external_id,
                                          "first_name": first_name,
                                          "last_name": last_name,
                                          "name": first_name,
                                          "employee_type": "full time",
                                          "email": email,
                                          "send_email_notification": True,
                                          "status": "Active",
                                          "roles": [
                                            "member",
                                            "edgraph"
                                          ]
                                        }
                                      ]
                            })         


    url=self.base_org_url+"/api/developer/v5/profiles"
    response=requests.post(url,headers=headers,data=payload)
    response= response.json()
    return response

sdk=edcast_sdk(os.environ["base_org_url"],os.environ["api_key"],payload)

sdk.create_user("manuj.iift@gmail.com")

sdk.get_user_list()




