from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    try:
        return "<h1 style='color:blue'>Hello There! Welcome</h1>"
    except Exception as ex:
        return "<h1 style='color:red'>Hello There! Fiailed  %s" % ex


@app.route("/fs")
def hellofs():
    try:
        file = open('/fs/a.txt', 'w')
        file.write("hii")
        file.close()
        return "<h1 style='color:blue'>Hello There! File created</h1>"
    except Exception as ex:
        return "<h1 style='color:red'>Hello There! Fiailed to create file!! </h1>i %s" % ex


@app.route("/iwelcome")
def welcome():
    return "<h1 style='color:blue'>Welcome to webapp</h1>"



if __name__ == "__main__":
    app.run(host='localhost', port='8085', debug=True)

