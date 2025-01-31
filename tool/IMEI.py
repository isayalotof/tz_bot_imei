import requests
import json

from config.config import imei_token

url = "https://api.imeicheck.net/v1/checks"

def real_check_imei(imei: str):
    payload = json.dumps({
      "deviceId": imei,
      "serviceId": 12
    })
    headers = {
      'Authorization': f'Bearer {imei_token}',
      'Accept-Language': 'en',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = response.json()

    # Извлекаем основную информацию о телефоне
    if data['status'] == 'successful':
        properties = data.get('properties', {})
        return properties
    return 0


