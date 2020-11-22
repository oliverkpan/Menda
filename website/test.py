from flask import Flask, Response, render_template, request, session

app = Flask(__name__,static_url_path="/static")

@app.route('/')
def index():
    return render_template('index.html')

#<form method="POST" action="{{url_for('search')}}">
#<input type="text" name="data" id="search" placeholder="Search..." />
@app.route('/search', methods =['POST'])
def search():
    data = request.form['data']
    return data

@app.route('/user')
def user_screen():
    data = "hello"
    return render_template('simple_page.html', user = data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug = True)