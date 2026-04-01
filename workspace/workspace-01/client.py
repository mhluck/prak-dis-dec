import requests

url = "http://127.0.0.1:8000/graphql"

query = """
{
  books {
    title
    author
  }
}
"""

response = requests.post(url, json={"query": query})

print(response.json())