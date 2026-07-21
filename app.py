from flask import Flask , request , redirect ,url_for ,Response ,session 

app = Flask(__name__)
app.secret_key = "supersecret"  # Set a secret key for session management

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "2005":
            session["user"] = username
            return redirect(url_for("Welcome"))
        else:
            return Response("Invalid credentials. Try again", mimetype="text/plain")

    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    '''

#welcome page(after login)
@app.route("/welcome")
def Welcome():
    if "user" in session:
        return f'''
<h2>welcome, {session["user"]}!</h2>
<a href="/logout">Logout</a>
'''
    return redirect(url_for("login"))

#logout route
@app.route("/logout")
def logout():
    session.pop("user", None) #remove user from session
    return redirect(url_for("login"))

