import requests

token = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb3dpZSIsImlkIjoyLCJleHAiOjE3MjMyNjE5OTB9.C7FZIZjQiTOKJmWmBZtq2SIAeqjkothsYGSxutdFSqY",
    "token_type": "bearer",
}

response = requests.get(
    "http://127.0.0.1:8000/items/all",
    headers={"Authorization": f"Bearer {token["access_token"]}"},
)

print(response.json())
