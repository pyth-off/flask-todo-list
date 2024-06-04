# Bootstrapping a Basic Flask Application

In this guide, we'll learn how to create and run a basic Flask application with a single route.

## 1. Create an Application Instance

Every Flask application needs an application instance. This instance is an object of the Flask class, which you can create as follows:

```python
from flask import Flask
app = Flask(__name__)
```

There are other ways to initialize a Flask app, but we'll keep it simple for now.

## 2. Create a Route and a Basic View

The most convenient way to declare a new route is by using the `@app.route` decorator. This decorator matches a URL to a view function.

```python
@app.route('/')
def index():
    return '<h1>Hello Flask, hello world!</h1>'
```

> Alternatively, you can declare a route using `app.add_url_rule('/', 'index', index)`, where `/` is the URL, `'index'` is the endpoint name, and `index` is the view function.

## 3. A Complete Application Example

Here is a complete example of a basic Flask application:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'
```

## 4. Run the Application in a Development Web Server

To run your application, use the following commands in your terminal:

```sh
(venv) $ export FLASK_APP=hello.py  # Replace 'hello.py' with the name of your script file
(venv) $ flask run
```

You should see output similar to this:

```sh
* Serving Flask app 'hello.py'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

You are now ready to start working on your Flask application.
