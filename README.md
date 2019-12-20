# Yara_appy

Implementación básica
La API deberá contar con tres métodos (Endpoints) que deben cumplir con este contrato

Add rule
Metodo: POST Path: /api/rule Body:

{
    "name":"esto no es coca papi rule",
    "rule":"rule EstoNoEsCocaPapiRule\r\n{\r\n strings:\r\n $my_text_string = \"esto no es coca papi\"\r\n condition:\r\n $my_text_string\r\n}"
}
Response Code: 201 en caso de éxito y en caso de error un status code correspondiente al tipo de error

Response Body:

{
    "id": 1,
    "name": "esto no es coca papi rule",
    "rule": "rule EstoNoEsCocaPapiRule\r\n{\r\n strings:\r\n $my_text_string = \"esto no es coca papi\"\r\n condition:\r\n $my_text_string\r\n}"
}
Curl de ejemplo:

curl --request POST \
  --url http://localhost:8080/api/rule \
  --header 'content-type: application/json' \
  --data '{
  "name":"esto no es coca papi rule",
  "rule":"rule EstoNoEsCocaPapiRule\r\n{\r\n strings:\r\n $my_text_string = \"esto no es coca papi\"\r\n condition:\r\n   $my_text_string\r\n}"
  }'
Analyze text
Metodo: POST Path: /api/analyze/text Body:

{
    "text":"esto es un texto a analizar",
    "rules": 
	    [
		    {"rule_id": 1},
		    {"rule_id": 2}
	    ]
}
Response Code: 200 en caso de éxito y en caso de error un status code correspondiente al tipo de error Response Body:

{
	"status": "ok",
	"results": [
		{
			"rule_id": 1,
			"matched": true
		},
		{
			"rule_id": 2,
			"matched": false
	    }
	]
}
Curl de ejemplo:

curl --request POST \
  --url http://localhost:8080/api/analyze/text \
  --header 'content-type: application/json' \
  --data '{
	“text”: ”estoesuntextoaanalizar”,
	"rules": [
		{
			"rule_id": 1
		},
		{
			"rule_id": 2
		}
	]
}'
Analyze file
Metodo: POST Path: /api/analyze/file Body:

multipart/form-data
rules=1,2
file=archivo.txt
Response Code: 200 en caso de éxito y en caso de error un status code correspondiente al tipo de error Response Body:

{
	"status": "ok",
	"results": [
		{
			"rule_id": 1,
			"matched": true
		},
		{
			"rule_id": 2,
			"matched": false
		}
	]
}
Curl de ejemplo:

curl -X POST \
  http://localhost:8080/api/analyze/file \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F file=@file \
  -F 'rules=1,2'
