import requests
import pandas as pd

WIKI_URL = 'https://wiki.openhumans.org/api.php'
FILE = 'QSProjects.xlsx'
FILE_MINI = 'QSProjects-mini-clean.xlsx'

def main():
    # Connecting to the wiki
    # The function 'connect' returns two variables which are needed to call 'post_to_wiki', and which are safed in 'CONNECT_RESULTS'
    CONNECT_RESULTS = connect(WIKI_URL)
    S = CONNECT_RESULTS[0]
    CSRF_TOKEN = CONNECT_RESULTS[1]
    # load cleaned dataset
    df = pd.read_excel(FILE_MINI)
    # prepare content from data and import it to wiki
    for index, row in df.iterrows():
       wiki_import(row, S, CSRF_TOKEN) 

def connect(WIKI_URL):
    S = requests.Session()

    URL = WIKI_URL

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
    return S, CSRF_TOKEN

def post_to_wiki(PAGE_CONTENT, PAGE_TITLE, S, CSRF_TOKEN):
    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": PAGE_TITLE,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": PAGE_CONTENT
    }

    R = S.post(WIKI_URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)

def wiki_import(PROJECT, S, CSRF_TOKEN):
    INFOBOX_SELFRESEARCHER = PROJECT['Presenter Name']

    INFOBOX_TOOLS = PROJECT['Tools']

    INFOBOX_TOPICS = PROJECT['Topics']

    PROJECT_ID = PROJECT['Project ID']

    DESCRIPTION = PROJECT['Project Description']

    VIDEO_ID = PROJECT['Vimeo ID']

    VIDEO_URL = PROJECT['Vimeo URL']

    TRANSCRIPT = PROJECT['Transcription']

    PAGE_CONTENT = '''{{{{Project Infobox|Self researchers= {} |Related tools= {} |Related topics= {} }}}}
This project has been imported from the [https://quantifiedself.com/show-and-tell/?project={} Quantified Self Show & Tell library]. The talk was given at EVENT on DATE.

==Description==
A description of this project as introduced by Quantified Self follows:

<blockquote>{}</blockquote>

==Video and Transcription==
{{{{#widget:Vimeo|id={}|url={}}}}}
A transcript of this talk is below:

<blockquote>{}</blockquote>
{{{{Project Queries}}}}
'''.format(INFOBOX_SELFRESEARCHER, INFOBOX_TOOLS, INFOBOX_TOPICS, PROJECT_ID, DESCRIPTION, VIDEO_ID, VIDEO_URL, TRANSCRIPT)

    PAGE_TITLE = PROJECT['Project Title']

    post_to_wiki(PAGE_CONTENT, PAGE_TITLE, S, CSRF_TOKEN)

if __name__ == "__main__":
    main()
