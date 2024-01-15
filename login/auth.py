import requests
from utilities.api import Api

class Login(Api):
    def __init__(self, email, password):
        super().__init__()

        self.email = "manoj@gmail.com"#email
        self.password = "md"#password
       
        self.api = self.login_api

    def login(self):
        data = {
            'email': self.email,
            'password': self.password
        }

        response = requests.post(self.api, data=data)
        if response.status_code == 200:
            json_data = response.json()
            json_data['status'] = True
            self.user_data = json_data
            return json_data
            access_token = json_data.get('access_token')
            user_data = json_data.get('data')

            # Process the access_token and user_data as needed
            print("Access Token:", access_token)
            print("User Data:", user_data)
        else:
            json_data = response.json()
            json_data['status'] = False
            return json_data