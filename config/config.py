import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.user_name = os.getenv("USER_NAME")
        self.user_password = os.getenv("USER_PASSWORD")
        self.t_wait = float(os.getenv("T_WAIT", 10)) # Default to 10 seconds if not set
        self.rh_online_url = "https://rhonline.msgas.com.br/#/login"

config = Config()
