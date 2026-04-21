import requests
import pybreaker
import time

# Maksimal 3x gagal, lalu sirkuit Terbuka (Open) selama 5 detik
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=5)

@breaker
def fetch_data(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url, timeout=2)
    response.raise_for_status()
    print(f"Successfully accessed {url}")

if __name__ == "__main__":
    # Kita buat looping 6 kali di dalam script
    for i in range(1, 7):
        print(f"\n--- Percobaan ke-{i} ---")
        try:
            fetch_data("http://localhost:44777")
        except Exception as e:
            # Mengambil pesan error aslinya agar lebih rapi
            print(f"Error: {e}")
        
        # Jeda 1 detik antar percobaan agar mudah diamati
        time.sleep(1)