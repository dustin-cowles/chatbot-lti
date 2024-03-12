"""
The main entry point for the Flask application server.
"""
from flask import make_response, render_template, request, send_from_directory

from backends.openai import OpenAi as backend
from lib.app import setup_app
from lib.cache import get_user_cache
from lib.lti import setup_lti_session, get_user_id, tool_login


app, asgi_app, launch_data_storage, cache = setup_app(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles login request from tool consumer.

    :params: None

    :return: The tool login response.
    :rtype: flask.Response
    """
    launch_data, cookie_service = setup_lti_session(launch_data_storage)

    response = tool_login(launch_data_storage)
    cookie_service.update_response(response)

    return response


@app.route("/launch", methods=["POST"])
def launch():
    """
    Handles launches from tool consumer.

    :params: None

    :return: The rendered index.html template.
    :rtype: flask.Response
    """
    launch_data, cookie_service = setup_lti_session(launch_data_storage)

    response = make_response(render_template(
        "index.html",
        launch_id=cookie_service.get_cookie("launch_id"),
        tool_host=request.host,
    ))
    cookie_service.update_response(response)

    return response


@app.route("/.well-known/<path:filename>")
def well_known(filename):
    """
    Serves files from the well-known directory to aid in tool consumer configuration.

    :param filename: The filename to serve.

    :return: The requested file.
    :rtype: flask.Response
    """

    return send_from_directory("well-known", filename, conditional=True)


@app.route("/course_materials", methods=["POST"])
def update_course_materials():
    """
    Updates the course materials.

    :param course_materials: The course materials to update.

    :return: None
    :rtype: flask.Response
    """
    launch_data, cookie_service = setup_lti_session(launch_data_storage)

    user_cache = get_user_cache(cache, get_user_id(launch_data))
    course_materials = request.get_json()

    return backend(user_cache).update_course_materials(course_materials)


@app.route("/messages", methods=["POST"])
def post_message():
    """
    Posts a message and caches response.

    :param message: The message to post.

    :return: OpenAI Message Thread formatted for frontend.
    :rtype: flask.Response
    """

    launch_data, cookie_service = setup_lti_session(launch_data_storage)
    user_cache = get_user_cache(cache, get_user_id(launch_data))
    message = request.get_json().get("content")

    return backend(user_cache).send_message(message)
