from flask import Flask, render_template, request
import json
import requests
import re
import config

app = Flask(__name__)

TEMPLATES_AUTO_RELOAD = True

# for ease of querying ai below
API_KEY = config.API_KEY
API_GEN_URL = "https://developer.nps.gov/api/v1/"
CAMP = "campgrounds"
PARKS = "parks"
EVENTS = "events"


# removes html tags/markup from text
def clean_text(text):
    return re.sub('<[^<]+?>', '', text)


# layout (home page)
@app.route('/')
def start_page():
    return render_template('layout.html')


# park page (customized to specific park based on park code)
@app.route('/park/<park_code>')
def park(park_code):
    params = {'parkCode': park_code, 'api_key': API_KEY}

    # obtain campground data
    park_campgrounds = json.loads(requests.get(API_GEN_URL + CAMP, params).text)['data']

    # obtain events at this park
    park_events = json.loads(requests.get(API_GEN_URL + "events", params).text)['data']

    # obtain alerts and news data about this park
    park_alerts = json.loads(requests.get(API_GEN_URL + "alerts", params).text)['data']
    park_news = json.loads(requests.get(API_GEN_URL + "newsreleases", params).text)['data']

    # obtain articles and people data about this park
    park_people = json.loads(requests.get(API_GEN_URL + "people", params).text)['data']
    park_articles = json.loads(requests.get(API_GEN_URL + "articles", params).text)['data']
    park_lessons = json.loads(requests.get(API_GEN_URL + "lessonplans", params).text)['data']

    # obtain park data
    parks = json.loads(requests.get(API_GEN_URL + PARKS, params).text)['data']

    # keep in mind the original parameter was parkData = parks.copy()[parkNum-1]
    return render_template('park.html', parkData=parks[0], parkCampgrounds=park_campgrounds,
                           parkEvents=park_events, parkAlerts=park_alerts, parkNews=park_news, parkPeople=park_people,
                           parkArticles=park_articles, parkLessons=park_lessons)


# camp page
@app.route('/camp/<int:camp_num>')
def camp(camp_num):
    campground = campgrounds[camp_num - 1]
    return render_template('campground.html', campground=campground)


# event page
@app.route('/event/<int:event_num>')
def event(event_num):
    event = events[event_num - 1]
    event["description"] = clean_text(event["description"])
    return render_template('event.html', event=event)


# about page
@app.route('/about/')
def about():
    return render_template('about.html')


# display search results
@app.route('/search_results/')
def search_results():
    return render_template('search_results.html')


# based on search bar contents, send queries to API and redirect to search results page
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        search_string = request.form['search-term']
        type_filter = request.form['filter']
        state_filter = request.form['state-filter']
        params = {}
        global parks
        global campgrounds
        global events

        parks = []
        campgrounds = {}
        events = {}

        # if no search parameters are given, ask user to provide them
        if search_string == "" and type_filter == "none" and state_filter == "none":
            return render_template('layout.html', message="Please specify search requirements. Search bar is allowed to"
                                                          " be empty if state or location type is selected")

        # add keyword to parameters
        if search_string != "none":
            params['q'] = str(search_string)

        # if a filter was selected
        if type_filter != "none":
            url = API_GEN_URL + type_filter + "?api_key=" + API_KEY

            # if a state was selected (only applicable to parks) add to parameters
            # this is because you can only query by "stateCode" for parks, and not for events or campgrounds
            if type_filter == "parks" and state_filter != "none":
                params['stateCode'] = state_filter

            r = requests.get(url, params)

            # assign api response content to correct dictionary
            if type_filter == "parks":
                parks = json.loads(r.text)['data']

            elif type_filter == "events":
                events = json.loads(r.text)['data']

            else:
                campgrounds = json.loads(r.text)['data']

        # if no filter was selected, make three queries for parks, events, and campgrounds
        else:
            # search events with query string
            url = API_GEN_URL + EVENTS + "?api_key=" + API_KEY
            events = json.loads(requests.get(url, params).text)['data']

            # search campgrounds with query string
            url = API_GEN_URL + CAMP + "?api_key=" + API_KEY
            campgrounds = json.loads(requests.get(url, params).text)['data']

            # search parks with query string
            if state_filter != "none":
                params['stateCode'] = state_filter
            url = API_GEN_URL + PARKS + "?api_key=" + API_KEY
            parks = json.loads(requests.get(url, params).text)['data']

        return render_template('search_results.html', parks=parks, campgrounds=campgrounds, events=events)


# home
@app.route('/home')
def home():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()
