from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
tg_token = os.getenv('TG_KEY')
first_admin_id = os.getenv('FIRST_ADMIN_ID')
imei_token = os.getenv('IMEI_TOKEN')