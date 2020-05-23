import json
import re

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions

webUrl = "https://contoso.sharepoint.com"
username = "user@contoso.onmicrosoft.com"
password = "your password"

endPoints = []
uniquEndpoints = set()

# Get Rest Endpoints like "Web/Activities" from link elements.
def getEndpointsFromXML(response: str):
    return re.findall(r"href=\"(Web.*?)\"", response)


def showEndpoints(endPointsList: list):
    for ep in endPointsList:
        print(ep)


def removeNoise(s: str):
    # If retrieved endpoint contains a number, replce to 1. (e.g. "Web/SiteGroups/GetById(23)" => "Web/SiteGroups/GetById(1)")
    s = re.sub(r"[0-9]+", "1", s)

    # If retrieved endpoint contains GUID, replce to blank (e.g. "Web/ContentTypes(\'1x1C1F1FBF1A1B1A1D1AD1B1\')" => "Web/ContentTypes()"
    s = re.sub(r"\'.+\'", "", s)
    return s


def runRestQuery(ctx, endpoint: str):
    request = ClientRequest(ctx)
    options = RequestOptions("{0}/_api/{1}".format(webUrl, endpoint))
    options.set_header("Accept", "application/xml")
    options.set_header("Content-Type", "application/xml")
    data = request.execute_request_direct(options)

    endPoints = getEndpointsFromXML(str(data.content))

    for ep in endPoints:
        ep = removeNoise(ep)

        # check diff
        beforeLength = len(uniquEndpoints)
        uniquEndpoints.add(ep)

        if len(uniquEndpoints) > beforeLength:
            runRestQuery(ctx, ep)


def main():
    ctx_auth = AuthenticationContext(webUrl)
    try:
        if ctx_auth.acquire_token_for_user(username, password):
            runRestQuery(ctx_auth, "web")
        else:
            print(ctx_auth.get_last_error())

        showEndpoints(uniquEndpoints)

    except Exception as e:
        print(e)


main()
