# JagaFakta.ID's ML API
## Installation
```
pip install -r requirements.txt
```

## How to run?
Run this command:
```
uvicorn app:app --host 0.0.0.0 --port 8080
```
And then go to [http://localhost:8080](http://localhost:8080). 

## Using the API
Endpoint : POST /predict

Headers :

- Content-Type: application/json

Request Body :

```json
{
  "text": "Rokok Kretek Lebih Aman daripada Rokok Putih"
}
```

Response Body

```json
{
  "text": "Rokok Kretek Lebih Aman daripada Rokok Putih",
  "clean_text": "rokok kretek lebih aman daripada rokok putih",
  "is_hoax": true
}
```

More about it: [http://localhost:8080/docs](http://localhost:8080/docs)
