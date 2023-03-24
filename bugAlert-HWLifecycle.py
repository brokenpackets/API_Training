import json
import requests
import base64

token = '<your arista.com token from user profile>'
url = 'https://www.arista.com/custom_data/bug-alert/alertBaseDownloadApi.php'

encodedtoken_bytes = token.encode("ascii")
encodedtoken = base64.b64encode(encodedtoken_bytes)
jsonpost = {'token_auth':encodedtoken.decode("ascii"),'file_version':'2'}

result = requests.post(url, data=json.dumps(jsonpost))
output = result.json()
for item in output['hardwareLifecycles']:
  print('Model: '+item['modelName'])
  print('End of Sale: '+item['endOfSale'])
  print('End of Life: '+item['endOfLife'])
  print('End of TAC Support: '+item['endOfTACSupport'])
  print('')
