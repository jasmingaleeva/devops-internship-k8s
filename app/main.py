#  /\_/\  
# ( o.o )  Буду рада пройти на следующий этап! (◕‿◕)
#  > ^ <

import os
import socket
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PORT = int(os.environ.get("APP_PORT", 32777))
HOST = "0.0.0.0"

class HelloWorldHandler(BaseHTTPRequestHandler):
    def _send_response_data(self, status_code, content_type, body):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        hostname = socket.gethostname()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        client_ip = self.client_address[0]

        if self.path in ["/healthz", "/readyz"]:
            response_payload = {
                "status": "healthy",
                "hostname": hostname,
                "timestamp": timestamp
            }
            self._send_response_data(200, "application/json", json.dumps(response_payload, indent=2))
            return

        if self.path == "/json":
            response_payload = {
                "message": "Hello, World!",
                "hostname": hostname,
                "client_ip": client_ip,
                "port": PORT,
                "timestamp": timestamp
            }
            self._send_response_data(200, "application/json", json.dumps(response_payload, indent=2))
            return

        # Main HTML response (Minimalist Black & White)
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Kubernetes</title>
    <style>
        body {{
            font-family: sans-serif;
            background-color: #ffffff;
            color: #000000;
            margin: 40px auto;
            max-width: 540px;
            padding: 0 16px;
            line-height: 1.5;
        }}
        .container {{
            border: 1px solid #000000;
            padding: 24px;
        }}
        h1 {{
            font-size: 22px;
            margin: 0 0 6px 0;
            border-bottom: 2px solid #000000;
            padding-bottom: 8px;
        }}
        .subtitle {{
            margin: 0 0 20px 0;
            font-size: 13px;
            color: #444444;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 0;
        }}
        th, td {{
            text-align: left;
            padding: 8px 4px;
            border-bottom: 1px solid #cccccc;
            font-size: 13px;
        }}
        th {{
            width: 35%;
            font-weight: bold;
        }}
        td {{
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
        <p class="subtitle">Kubernetes Deployment Demo</p>
        <table>
            <tr>
                <th>Статус</th>
                <td>200 OK</td>
            </tr>
            <tr>
                <th>Pod (Hostname)</th>
                <td>{hostname}</td>
            </tr>
            <tr>
                <th>Порт</th>
                <td>{PORT}</td>
            </tr>
            <tr>
                <th>Клиентский IP</th>
                <td>{client_ip}</td>
            </tr>
            <tr>
                <th>Время (UTC)</th>
                <td>{timestamp}</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""
        self._send_response_data(200, "text/html; charset=utf-8", html_content)

    def log_message(self, format, *args):
        print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}", flush=True)

def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, HelloWorldHandler)
    print(f"Starting Hello World web server on http://{HOST}:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...", flush=True)
        httpd.server_close()

if __name__ == "__main__":
    run()
