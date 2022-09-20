import requests
import json

url = "https://api.culqi.com/v2/charges"
url1 = "https://api.culqi.com/v2/customers"
url2 =  "https://api.culqi.com/v2/cards"

header = {
    "Content-type" : "application/json",
    "Authorization": "Bearer sk_test_VFJD3bDdk6ap5yDv"
}

cargo ={
    "amount": "60000",
    "currency_code": "PEN",
    "email": "richard@piedpiper.com",
   # "source_id":"tkn_test_HPpVtqzpn1f8YowD"
    "source_id":"crd_test_VBIXBryy76OUfmFp"
}

cargo2 ={
    "amount": "50000",
    "currency_code": "PEN",
    "email": "carmen@piedpiper.com",
    "source_id":"tkn_test_DaTiC75xaLxpNeU2"
    #"source_id":"crd_test_VBIXBryy76OUfmFp"
}
 
    
cliente = {
  "first_name": "Maritza",
  "last_name": "Bailon",
  "email": "maritza@gmail.com",
  "address": "San Francisco Bay Area",
  "address_city": "Palo Alto",
  "country_code": "US",
  "phone_number": "6505434800"
}

cliente2 = {
  "first_name": "Carmen",
  "last_name": "Hendricks",
  "email": "carmen@piedpiper.com",
  "address": "San Francisco Bay Area",
  "address_city": "Palo Alto",
  "country_code": "US",
  "phone_number": "6505434800"
}

tarjeta = {
  "customer_id": "cus_test_THKkhAVVTeGBttX6",
  "token_id": "tkn_test_HpC2tPSAhuclPdzd"
}
tarjeta2 = {
  "customer_id": "cus_test_IzxjQvepGcQyAWaB",
  "token_id": "tkn_test_DaTiC75xaLxpNeU2"
}

#response= requests.post(url,data=json.dumps(cargo2), headers=header)
#response= requests.post(url1,data=json.dumps(cliente), headers=header)
response= requests.post(url2,data=json.dumps(tarjeta), headers=header)

r_json=response.json()

#print(r_json)