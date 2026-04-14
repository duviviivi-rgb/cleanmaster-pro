import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def start_server():
    with socketserver.TCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving HTTP on http://localhost:{PORT}/")
        print(f"You can access the frontend at http://localhost:{PORT}/index.html")
        httpd.serve_forever()

def open_browser():
    time.sleep(1)  # Give the server time to start
    webbrowser.open(f'http://localhost:{PORT}/index.html')

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open the browser
    open_browser()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped.")
