import requests
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def access_url(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url)
    response.raise_for_status()
    print(f"Successfully accessed {url}")

if __name__ == "__main__":
    try:
        access_url("http://localhost:44777")
    except Exception as e:
        print(f"Failed to access URL after multiple retries: RetryError {e}")