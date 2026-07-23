from flask import Flask, render_template , request

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
        username = request.form.get("username")
        password = request.form.get("password")
        """if username == "vishal" and password == "pass":
            return render_template("welcome.html", name=username)"""

        valid_users = {
              'admin': '123',
              'vishal123': 'pass',
              'rajesh': 'raj',
        }
        if username in valid_users and password == valid_users[username]:
            return render_template("welcome.html",ame=username)
        
        else:
            return "Invalid credentials. Please try again."
        if __name__ == "__main__":
            app.run(debug=True) 
