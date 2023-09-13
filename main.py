from flask import Flask, render_template, request
import requests
import smtplib
import os

# blog_url = os.environ.get("blog_url")
blog_data = requests.get("blog_url").json()
my_email = os.environ.get("my_email")
password = os.environ.get("password")

app = Flask("__name__")


@app.route("/")
def home():
    return render_template("index.html", all_posts=blog_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        print(f"{data['name']}\n{data['phone']}\n{data['email']}\n{data['message']}")
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:post_id>")
def post(post_id):
    requested_post = None
    for blog_post in blog_data:
        if blog_post["id"] == post_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=email_message)


if "__main__" == __name__:
    app.run(debug=True)
