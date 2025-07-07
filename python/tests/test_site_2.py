from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.route("/")
def home():
    html = """
    <html>
      <head><title>Secure Page</title></head>
      <body>
        <h1>Welcome to a Secure Site</h1>
        <form action="/submit" method="POST">
            <input type="hidden" name="csrf_token" value="abc123">
            <input type="text" name="username">
            <input type="password" name="password" autocomplete="off">
            <input type="submit" value="Login">
        </form>
        <script src="/static/external.js"></script>
      </body>
    </html>
    """
    return make_response(html)

@app.route("/submit", methods=["POST"])
def submit():
    return "Form submitted safely."

# Optional JS file to simulate external script
@app.route("/static/external.js")
def static_js():
    return "console.log('external script');", 200, {"Content-Type": "application/javascript"}

if __name__ == "__main__":
    app.run(port=5001)
