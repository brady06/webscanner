from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Welcome</h1>
            <form action="/submit" method="post">
                <input type="text" name="username">
                <input type="password" name="password" autocomplete="on">
                <input type="submit" value="Login">
            </form>
            <!-- password=admin123 -->
            <script>alert("inline JS")</script>
            <p><a href="/search?q=test">Search something</a></p>
        </body>
    </html>
    """

@app.route("/submit", methods=["POST"])
def submit():
    return f"Hello, {request.form.get('username')}"

@app.route("/xss")
def xss():
    val = request.args.get("xss_test", "")
    return f"<div>You said: {val}</div>"

@app.route("/redirect")
def redirect_test():
    url = request.args.get("redirect", "https://example.com")
    return redirect(url)

@app.route("/error")
def error():
    raise Exception("Test stack trace")

@app.route("/admin")
def admin():
    return "<h1>Admin panel</h1>"

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"""
    <html>
        <head><title>Search Results</title></head>
        <body>
            <h1>Search Results</h1>
            <p>You searched for: {query}</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
