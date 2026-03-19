import time
import uuid
import json
from flask import request, jsonify, g
from werkzeug.exceptions import HTTPException

# middleware is code that runs BETWEEN the request coming in and the response going out
# think of it as a pipeline: Request → middleware → your route handler → middleware → Response
# flask gives us hooks to plug into this pipeline: before_request and after_request


def register_middleware(app):

    @app.before_request
    def start_timer():
        # before_request runs before EVERY request hits any route
        # g is flask's per-request global storage — lives only for that one request
        # uuid4() generates a random unique id, [:8] keeps it short for readable logs
        g.request_id = str(uuid.uuid4())[:8]
        g.start_time = time.time()

    @app.before_request
    def require_api_key():
        # this also runs before every request
        # but we only enforce the api key check for POST /scrape
        # because thats the only sensitive operation (triggering a scrape)
        # GET endpoints like /jobs, /stats, /scrape/status are public
        if request.method == "POST" and request.path == "/scrape":
            client_key = request.headers.get("X-API-KEY")
            # X-API-KEY is a custom header the client must send
            # e.g. curl -H "X-API-KEY: secret123" -X POST /scrape

            if client_key != app.config.get("API_KEY"):
                # if key is missing or wrong, stop here — never reaches the route
                return (
                    jsonify(
                        {
                            "error": "Unauthorized",
                            "message": "Invalid or missing API key",
                        }
                    ),
                    401,
                )

    @app.after_request
    def log_request(response):
        # after_request runs after EVERY route handler finishes
        # response is what your route returned
        # we calculate how long the request took and log it as structured JSON
        duration = 0
        if hasattr(g, "start_time"):
            duration = round((time.time() - g.start_time) * 1000, 2)

        # structured log — every field is a key, parseable by tools like Datadog, ElasticSearch
        log_entry = {
            "request_id": getattr(g, "request_id", None),
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": duration,
        }
        print(json.dumps(log_entry))

        # we MUST return the response, otherwise flask gets nothing back
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # this catches ANY unhandled exception across the entire app
        # without this, flask would return an ugly HTML error page
        # isinstance check: if its already an HTTP error (like 404), just pass it through
        if isinstance(e, HTTPException):
            return e

        # structured error log — consistent format with request logs
        error_log = {
            "request_id": getattr(g, "request_id", None),
            "error": "Internal Server Error",
            "message": str(e),
        }
        print(json.dumps(error_log))

        return (
            jsonify(
                {"error": "Internal Server Error", "message": "Something went wrong"}
            ),
            500,
        )


# /**```

# **The pipeline visually:**
# ```
# Incoming Request
#       ↓
# start_timer()        ← before_request
#       ↓
# require_api_key()    ← before_request (blocks here if invalid key)
#       ↓
# your route handler   ← actual logic
#       ↓
# log_request()        ← after_request
#       ↓
# Outgoing Response
# **

# **/
