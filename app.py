from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Response, Header
from fastapi.staticfiles import StaticFiles

from config import APP_HOST, APP_PORT, APP_LOCATION, FB_VERIFY_TOKEN
from chatbot.bot import Bot
from parser import parse_request

webserver = FastAPI()
webserver.mount(
    path="/files",
    app=StaticFiles(directory=f"{APP_LOCATION}/files/"),
    name="files"
)
bot = Bot()


def verify_request(func):
    """
    If the user agent is not in the list of authorized user agents, return a 403 response.
    Otherwise, return the result of the decorated function.
    """
    def wrapper(request: Request, user_agent: Optional[str] = Header(None), *args, **kwargs):
        authorized_user_agents = (
            "facebookexternalua",
            "facebookplatform/1.0 (+http://developers.facebook.com)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "facebookexternalhit/1.1")
        if user_agent not in authorized_user_agents:
            return Response(content="<h1>Unauthorized</h1>", status_code=403)
        return func(request, *args, **kwargs)
    return wrapper


@webserver.get("/")
async def test_webhook(request: Request):
    """
    If the request contains a query parameter called `hub.verify_token` and its value is equal to the `FB_VERIFY_TOKEN`
    environment variable, then return the value of the `hub.challenge` query parameter
    """
    print("Verifying challenge token sent by Facebook ...")
    verify_token = request.query_params.get("hub.verify_token")

    if verify_token is not None:
        if verify_token == FB_VERIFY_TOKEN:
            print("Challenge token is matching to the App secret.")
            return Response(content=request.query_params.get("hub.challenge"), status_code=200)
        print("Challenge token doesn't match to the App secret.")
        return Response(status_code=403)
    print("Invalid request")
    return Response(status_code=403)


@webserver.post("/")
async def handle_post_request(request: Request):
    """
    It takes a request, parses it, and sends it to the bot

    Args:
      request (Request): Request - the request object

    Returns:
      A response object with a status code of 200 or 400.
    """
    request_content = await request.json()

    if request_content is not None:
        message = parse_request(request_content)
        if message is not None:
            bot.receive_message(message)
            return Response(status_code=200)
    return Response(status_code=400)

