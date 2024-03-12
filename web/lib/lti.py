import json
import logging
import os

from flask import request, session
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.contrib.flask import (
    FlaskCookieService,
    FlaskMessageLaunch,
    FlaskOIDCLogin,
    FlaskRequest,
    FlaskCacheDataStorage
)


TOOL_CONFIG = ToolConfJsonFile(os.path.join("config", "lti_config.json"))


def export_jwks():
    """
    Exports the jwks.json file to the well-known directory.

    :param toolconf: The tool configuration.

    :returns: None
    """

    directory = os.path.join(os.path.dirname(__file__), "well-known")

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, "jwks.json"), "w", encoding="utf8") as file:
        file.write(json.dumps(TOOL_CONFIG.get_jwks()))


def tool_login(launch_data_storage):
    wrapped_flask_request = FlaskRequest(
        cookies=request.cookies,
        session=session
    )
    target_link_uri = wrapped_flask_request.get_param("target_link_uri")
    cookie_service = FlaskCookieService(wrapped_flask_request)

    return FlaskOIDCLogin(
        request=wrapped_flask_request,
        tool_config=TOOL_CONFIG,
        launch_data_storage=launch_data_storage,
        cookie_service=cookie_service
    ).enable_check_cookies().redirect(target_link_uri)


def setup_lti_session(launch_data_storage):
    """
    Retrieves the message_launch and returns it.

    :param launch_id: The original launch_id.
    :param request: The flask request.

    :returns: The message_launch.
    :rtpes: MessageLaunch
    """
    wrapped_flask_request = FlaskRequest(
        cookies=request.cookies,
        session=session
    )
    message_launch = FlaskMessageLaunch(
        request=wrapped_flask_request,
        tool_config=TOOL_CONFIG,
        launch_data_storage=launch_data_storage
    )

    # Cache the public key for the LMS.
    message_launch.set_public_key_caching(
        launch_data_storage, cache_lifetime=7200)

    launch_data = message_launch.get_launch_data()

    cookie_service = FlaskCookieService(wrapped_flask_request)
    cookie_service.set_cookie("launch_id", message_launch.get_launch_id())

    # user_id = launch_data.get("https://purl.imsglobal.org/spec/lti/claim/lti1p1").get("user_id")
    # roles = launch_data.get("https://purl.imsglobal.org/spec/lti/claim/roles")
    # context_id = launch_data.get("https://purl.imsglobal.org/spec/lti/claim/context").get("id")
    # resource_id = launch_data.get("https://purl.imsglobal.org/spec/lti/claim/resource_link").get("id")

    return launch_data, cookie_service


def get_user_id(launch_data):
    """
    Returns the user_id from the message_launch.

    :param message_launch: The message_launch.

    :returns: The user_id.
    :rtype: str
    """

    return launch_data.get(
        "https://purl.imsglobal.org/spec/lti/claim/lti1p1").get("user_id")


def get_launch_data_storage(cache):
    """
    Returns the launch data storage.

    :params: None

    :return: The launch data storage.
    :rtype: FlaskCacheDataStorage
    """

    return FlaskCacheDataStorage(cache)
