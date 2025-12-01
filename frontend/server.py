import http.server
import socketserver
import sys

PORT = 8000

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Only log errors (status code >= 400)
        if int(args[1]) >= 400:
            sys.stderr.write("%s - - [%s] %s\n" %
                             (self.client_address[0],
                              self.log_date_time_string(),
                              format%args))

print(f"✨ Frontend running at http://localhost:{PORT}")
print("   (Access logs are hidden, only errors will be shown)")
print("   Press Ctrl+C to stop.")

# Allow address reuse to prevent "Address already in use" errors on restart
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
