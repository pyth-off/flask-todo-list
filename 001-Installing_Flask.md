# Introduction to Flask: Installation Guide

In this post, we'll walk through installing Flask and setting up a virtual environment.

Flask has three primary dependencies: routing, debugging, and the Web Server Gateway Interface (WSGI) from Werkzeug; the templating engine from Jinja2; and command-line integration from Click. Additional services are available via dependencies.

> This tutorial assumes you're using a Linux-like environment with Python 3.x installed.
> We'll name our application "flask-abc".

## 1. Create the Application Directory

If you are using Git and want to clone an existing repository:

```sh
$ git clone https://<your-repo-url>
$ cd your-repo-url
```

Otherwise, create an empty directory:

```sh
$ mkdir flask-abc
$ cd flask-abc
```

## 2. Create a Virtual Environment

The `venv` package required for the next step is not included by default in Linux installations.

To install the `venv` package:

```sh
$ sudo apt-get install python3-venv
```

To create a virtual environment, type:

```sh
$ python3 -m venv flask-abc-venv
```

If successfully created, you should see the "flask-abc-venv" directory inside your working directory.

## 3. Activate / Deactivate Your Virtual Environment

To activate the virtual environment:

```sh
$ source flask-abc-venv/bin/activate
```

When a virtual environment is activated, its local Python interpreter location is added to the PATH variable. When you're done working with your virtual environment, type `deactivate` to restore the PATH value.

## 4. Install Flask

```sh
$ pip install flask
```

## 5. Check Installation and Dependency Versions

```sh
$ pip freeze
```

That's it! You can now start working on your new Flask project.
