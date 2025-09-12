import socket

HOST = "127.0.0.1"  # Localhost
PORT = 9090         # Port to listen on

def handle_client(conn):
    request = conn.recv(1024).decode()
    headers = request.split("\r\n")
    
    # Debug: print incoming HTTP request
    print("=== Incoming Request ===")
    print(request)
    print("========================")
    
    # Look for the Cookie header
    cookie = None
    for h in headers:
        if h.startswith("Cookie:"):
            cookie = h.split(":", 1)[1].strip()
            break

    if cookie:
        body = f"<html><body><h1>Welcome back! Your cookie: {cookie}</h1></body></html>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n" +
            body
        )
    else:
        body = "<html><body><h1>Welcome, new user!</h1></body></html>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Set-Cookie: User=User123\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n" +
            body
        )

    conn.sendall(response.encode())
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"🍪 Cookie server running at http://{HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    start_server()

