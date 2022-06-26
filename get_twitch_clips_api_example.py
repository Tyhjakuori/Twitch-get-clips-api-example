import time
import json
import requests
import configparser
from datetime import datetime

# TODO make ratelimiting/throttling system 30 requests per minute
#limit = 30
#current = 0
config = configparser.ConfigParser()
config.read('.cfg.ini')

user = input("User login name: ")
url = 'https://api.twitch.tv/helix/users?login={}'.format(user)

response = requests.get(url, headers = {"Client-Id": config['DEFAULT']['client_id'],
        "Authorization": config['DEFAULT']['authorization']})
data = response.json()
print('User-id for {}: {}'.format(user, data['data'][0]['id']))

# Channel where you want to get clips from, must be broadcaster_id numerical string
# Just the channel name won't work
# If you don't know how to get it check out this gist:
# https://gist.github.com/Tyhjakuori/cf8d92a90c7282cb0d3726ad8a376c87
broadcaster_id = data['data'][0]['id']
# Start and end days must be in RFC3339 format
# Both of these must be specified; otherwise, the time period is ignored.
# https://dev.twitch.tv/docs/api/reference#get-clips
start_day = "2022-01-01T00:00:00Z"
#end_day = "2022-05-27T00:00:00Z"
end_day = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"
year = end_day[0:4]

url1 = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(broadcaster_id, start_day, end_day)
print(url1)
with open('{}-clips_{}.json'.format(user, year), 'w') as json_file:
    response = requests.get(url1, headers = {"Client-Id": config['DEFAULT']['client_id'],
        "Authorization": config['DEFAULT']['authorization']})
    print(response.status_code)
    data = response.json()
    json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(data)
    print(data['pagination']['cursor'])
    cursor = None
    if 'cursor' in data['pagination']:
        cursor = data['pagination']['cursor']
        while cursor:
            url2 = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&after={}".format(broadcaster_id, start_day, end_day, cursor)
            response1 = requests.get(url2, headers = {"Client-Id": config['DEFAULT']['client_id'],
                "Authorization": config['DEFAULT']['authorization']}) 
            print(response.status_code)
            data1 = response1.json()
            print(data1)
            json.dump(data1, json_file, ensure_ascii=False, indent=4)
            if 'cursor' in data1['pagination']:
                cursor = data1['pagination']['cursor']
                time.sleep(5) # muuta sekunttiin kun request limit on käytössä
            else:
                cursor = None

