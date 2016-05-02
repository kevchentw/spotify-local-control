import requests as r
import json
from time import sleep


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
HEADERS = {
    "Referer": "https://open.spotify.com/browse",
    'User-Agent': USER_AGENT,
    'Accept': '*/*',
    "Connection": "keep-alive",
    "Origin": "https://open.spotify.com"
}
ORIGIN = "https://open.spotify.com"
TOKEN_URL = "https://open.spotify.com/token"
CSRF_URL = "https://ccigoebwch.spotilocal.com:4370/simplecsrf/token.json?cors=&ref="
STATUS_URL = "https://ccigoebwch.spotilocal.com:4370/remote/status.json?csrf={{csrf}}&oauth={{oauth}}&cors=&ref="
PLAY_URI_URL = "https://ulbrihaxiq.spotilocal.com:4370/remote/play.json?csrf={{csrf}}&oauth={{oauth}}&context={{context}}&uri={{uri}}&cors=&ref="
PAUSE_URL = "https://ulbrihaxiq.spotilocal.com:4370/remote/pause.json?csrf={{csrf}}&oauth={{oauth}}&pause={{pause}}&cors=&ref="
OPEN_URL = "https://ccigoebwch.spotilocal.com:4370/remote/open.json?cors=&ref="

class SpotifyLocalControl:
    def __init__(self):
        self.oauth = ""
        self.csrf = ""

    def get_url(self, url, data=[]):
        if not (self.csrf or self.oauth):
            self.get_init_data()
        url = url.replace("{{csrf}}", self.csrf).replace("{{oauth}}", self.oauth)
        for i in data:
            url = url.replace("{{" + str(i[0]) + "}}", str(i[1]))
        return url

    def get_init_data(self):
        res = r.get(TOKEN_URL, headers=HEADERS, verify=False)
        self.oauth = json.loads(res.text)['t']
        res = r.get(CSRF_URL, headers=HEADERS, verify=False)
        self.csrf = json.loads(res.text)['token']

    def open_spotify(self):
        res = r.get(OPEN_URL, headers=HEADERS, verify=False)
        sleep(5)

    def get_status(self):
        res = r.get(self.get_url(STATUS_URL), headers=HEADERS, verify=False)
        return res.text

    def play_uri(self, uri):
        data = [
            ("context", ""),
            ("uri", uri),
        ]
        url = self.get_url(PLAY_URI_URL, data)
        res = r.get(url, headers=HEADERS, verify=False)
        return res.text

    def start(self):
        data = [
            ("pause", "false"),
        ]
        url = self.get_url(PAUSE_URL, data)
        res = r.get(url, headers=HEADERS, verify=False)
        return res.text

    def pause(self):
        data = [
            ("pause", "true"),
        ]
        url = self.get_url(PAUSE_URL, data)
        res = r.get(url, headers=HEADERS, verify=False)
        return res.text

if __name__ == "__main__":
    s = SpotifyLocalControl()
    s.get_init_data()
    print(s.play_uri("spotify:track:5MChi9fdCbTIWDJPPUuuW6"))
    sleep(5)
    s.pause()
    sleep(5)
    s.start()
