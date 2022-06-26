Example on how to get Twitch clips from the api with python.

You will need client id, access token to use this. 
For more info https://dev.twitch.tv/docs/api

Channel where you want to get clips from must be (broadcaster id)[https://dev.twitch.tv/docs/api/reference#get-users]
If only want to know how to get it check out this gist:
https://gist.github.com/Tyhjakuori/cf8d92a90c7282cb0d3726ad8a376c87

Start and end days must be in RFC3339 format.
Both of these must be specified; otherwise, the time period is ignored.
https://dev.twitch.tv/docs/api/reference#get-clips

You will need to change start day to what you want.
You can also specify end day manually. 
Currently it gets todays day and time, so just comment it out and use the other commented variable.

End result will be written in json file, but currently it won't be valid json. But i'm working on that.
Json file will be named '(username)-clips_(year).json"