import requests

S = requests.Session()

URL = "https://wiki.openhumans.org/api.php"

# Step 1: GET request to fetch login token
PARAMS_0 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_0)
print(R)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
PARAMS_1 = {
    "action": "login",
    "lgname": "bot_user_name",
    "lgpassword": "bot_password",
    "lgtoken": LOGIN_TOKEN,
    "format": "json"
}

R = S.post(URL, data=PARAMS_1)

# Step 3: GET request to fetch CSRF token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

INFOBOX_TOPICS = "Fitness, Brain, Mood and emotion"

INTRO = "This is the introduction"

DESCRIPTION = "This is the description"

VIDEO_ID = "96591409"

VIDEO_URL = "https://vimeo.com/96591409"

TRANSCRIPT = "This is the transcript"

PAGE_CONTENT = "{{Project Infobox|Self researchers=|Related tools=|Related topics=" + INFOBOX_TOPICS + "|Builds on projects=}}" + INTRO + "<h2>Project Description</h2>" + DESCRIPTION + "<h2>Video and Transcription</h2>" + "{{#widget:Vimeo|id=" + VIDEO_ID + "|url=" + VIDEO_URL + "}}" + TRANSCRIPT + "{{Project Queries}}" + "[[Category:QS Show & Tell]]"

# Step 4: POST request to edit a page
PARAMS_3 = {
    "action": "edit",
    "title": "Project:Sandbox",
    "token": CSRF_TOKEN,
    "format": "json",
    "appendtext": PAGE_CONTENT
}

R = S.post(URL, data=PARAMS_3)
DATA = R.json()

print(DATA)