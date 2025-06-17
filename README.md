Client Sends Request

A user accesses your web application via a browser or API client.

The request hits the Django server (e.g., python manage.py runserver).

URL Routing

Django uses urls.py to match the request path to a specific view function or class-based view.

View Processing

The view receives the request, processes logic, accesses the database via models, and renders a response (HTML, JSON, etc.).

Template Rendering (if needed)

For HTML responses, Django renders templates using context data.

Response to Client

Django sends the final response back to the user's browser or API consumer.

Middleware (Optional in All Steps)

Middleware components can modify the request/response at different stages.
