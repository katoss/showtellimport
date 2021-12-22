import requests
import pandas as pd
import string

WIKI_URL = 'https://wiki.openhumans.org/api.php'
FILE = 'QSProjects.xlsx'
FILE_MINI = 'QSProjects-mini.xlsx'

def main():
    # Connecting to the wiki
    # The function 'connect' returns two variables which are needed to call 'post_to_wiki', and which are safed in 'CONNECT_RESULTS'
    CONNECT_RESULTS = connect(WIKI_URL)
    S = CONNECT_RESULTS[0]
    CSRF_TOKEN = CONNECT_RESULTS[1]
    # import and clean dataset
    data = import_data(FILE_MINI)

    wiki_import(data, S, CSRF_TOKEN) 

    # create the text for the wiki page from the imported data
    # PAGE_CONTENT = prepare_content()

    # Posting to the wiki
    # post_to_wiki(PAGE_CONTENT, S, CSRF_TOKEN)

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

def import_data(FILE):
    df = pd.read_excel(FILE, sheet_name='Published Projects')
    print(df.columns)

    # Clean data
    # Replace ampersands by 'and'
    df = df.replace('&', 'and', regex=True)
    # #capitalize first letter of all topics in topic list
    df['Topics'] = df.Topics.apply(lambda x: string.capwords(x, sep=', ') if pd.notnull(x) else x)
    # TODO: remove empty lines at end of transcripts
    # TODO: remove 'other' from topic lists
    # TODO: unify similar topic names

    # Create df with variables needed for wiki import
    dfw = df.drop(['Publish Status'], axis=1)
    dfw['Vimeo ID'] = df['Vimeo URL'].str.split('/').str[3]

    print(dfw.iloc[0])
    return dfw

def prepare_content():
    INFOBOX_TOPICS = "Fitness, Brain, Mood and emotion"

    INTRO = "This is the introduction"

    DESCRIPTION = "This is the description"

    VIDEO_ID = "96591409"

    VIDEO_URL = "https://vimeo.com/96591409"

    TRANSCRIPT = "This is the transcript"

    PAGE_CONTENT = '''intro text

    ==Description==
    {}

    ==Video and Transition==
    test test test

    {{{{Project Queries}}}}
    '''.format(DESCRIPTION)
    return PAGE_CONTENT

def post_to_wiki(PAGE_CONTENT, S, CSRF_TOKEN):
    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": "Project:Sandbox",
        "token": CSRF_TOKEN,
        "format": "json",
        "text": PAGE_CONTENT
    }

    R = S.post(WIKI_URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)

def wiki_import(DATA, S, CSRF_TOKEN):
    INFOBOX_TOPICS = DATA.iloc[0]['Topics']

    INTRO = "This is the introduction"

    DESCRIPTION = DATA.iloc[0]['Project Description']

    VIDEO_ID = DATA.iloc[0]['Vimeo ID']

    VIDEO_URL = DATA.iloc[0]['Vimeo URL']

    TRANSCRIPT = DATA.iloc[0]['Transcription']

    PAGE_CONTENT = '''{{{{Project Infobox|Self researchers=|Related tools=|Related topics= {} }}}}
intro text

==Description==
A description of this project as introduced by Quantified Self follows:

<blockquote>{}</blockquote>

==Video and Transcription==
{{{{#widget:Vimeo|id={}|url={}}}}}
A transcript of this talk is below:

<blockquote>{}</blockquote>
{{{{Project Queries}}}}
'''.format(INFOBOX_TOPICS, DESCRIPTION, VIDEO_ID, VIDEO_URL, TRANSCRIPT)

    post_to_wiki(PAGE_CONTENT, S, CSRF_TOKEN)

if __name__ == "__main__":
    main()
