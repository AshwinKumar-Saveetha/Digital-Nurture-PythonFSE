# Author: Ashwin Kumar A
# Project: Python Backend Frameworks Hands-On
# Hands-On: 1 - Web Framework Foundations & Django Project Setup
# Framework: Django
# File: notes.py
# Purpose: Theory notes for request-response cycle, middleware, WSGI vs ASGI, and MVC/MVT

# Hands-On 1 Notes
# Topic: Request-Response Cycle

# Example request: GET /api/courses/

# Step 1: The browser or frontend sends an HTTP GET request to Django.
# Step 2: Django receives the request and checks urls.py.
# Step 3: urls.py finds the correct URL pattern and sends the request to a view.
# Step 4: The view contains Python logic. It decides what response to return.
# Step 5: If data is needed, the view asks the Model to get data from the database.
# Step 6: The Model talks to the database and returns the data to the view.
# Step 7: The view creates an HTTP Response.
# Step 8: Django sends the response back to the browser or frontend.

# Topic: Middleware

# Middleware sits between the browser request and the Django view.
# It can check or modify the request before it reaches the view.
# It can also check or modify the response before it goes back to the browser.

# Request flow with middleware:
# Browser Request -> Middleware -> URL Router -> View -> Middleware -> Browser Response

# Example 1: django.middleware.security.SecurityMiddleware
# This middleware adds security improvements to the request and response.

# Example 2: django.contrib.sessions.middleware.SessionMiddleware
# This middleware allows Django to remember user session data between requests.

# Topic: WSGI vs ASGI

# WSGI means Web Server Gateway Interface.
# It is a standard way for a web server to talk to a Python web application.

# ASGI means Asynchronous Server Gateway Interface.
# It is a newer standard that supports normal requests and also async features.

# WSGI is mostly used for traditional request-response websites.
# ASGI is useful for real-time features like WebSockets, chat apps, live notifications, and async APIs.

# Django creates both wsgi.py and asgi.py files.
# For normal Django projects, WSGI is commonly used by default.
# We switch to ASGI when we need async features or real-time communication.

# Topic: MVC and Django MVT Mapping

# MVC means Model-View-Controller.
# It is a design pattern used to separate application code into parts.

# Model:
# The Model handles data and database logic.

# View in MVC:
# The View is what the user sees.

# Controller:
# The Controller receives the request, decides what to do, and connects Model and View.

# Django uses MVT, which means Model-View-Template.

# Model in Django:
# Same as Model in MVC. It handles database tables and data logic.

# View in Django:
# Works like the Controller in MVC. It receives the request and returns a response.

# Template in Django:
# Works like the View in MVC. It controls what the user sees on the page.

# MVC to Django MVT Mapping:
# MVC Model      -> Django Model
# MVC View       -> Django Template
# MVC Controller -> Django View