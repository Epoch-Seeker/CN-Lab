import requests
import logging

# Configure logging
logging.basicConfig(
    filename='api_requests.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        print_response(response)
    except requests.RequestException as e:
        logging.error(f"GET request failed: {e}")
        print(f"Error occurred during GET request: {e}")

def send_post_request(url, data=None):
    try:
        response = requests.post(url, json=data)
        print_response(response)
    except requests.RequestException as e:
        logging.error(f"POST request failed: {e}")
        print(f"Error occurred during POST request: {e}")

def print_response(response):
    print("\n--- Response ---")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body:\n{response.text}")
    print("----------------\n")

def main():
    get_url = "https://jsonplaceholder.typicode.com/posts/1"
    post_url = "https://jsonplaceholder.typicode.com/posts"

    print("Sending GET request...")
    send_get_request(get_url)

    print("Sending POST request...")
    post_data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    send_post_request(post_url, data=post_data)

if __name__ == "__main__":
    main()
