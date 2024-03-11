import json
import requests


class WebServerAccess:
    def __init__(self):
        self.password = "surelynooneguessesthisitskindalong"
        self.read_link = "https://rebornwebserver.pages.dev/box"
        self.import_link = "https://import-test.idkup137.workers.dev/api/import"
        self.export_link = "https://import-test.idkup137.workers.dev/api/export"

    def import_call(self, imports):
        i = 0
        fields = {}
        data = {"auth": self.password,
                "fields": fields}
        for line in imports:
            line = line.strip("\n")
            keys = line.split("|")
            mon = {"name": keys[0], "species": int(keys[1]), "speciesname": keys[2], "lvl": int(keys[3]),
                   "ability": int(keys[4]),
                   "nature": int(keys[5]), "moves": keys[6], "ivs": keys[7], "evs": keys[8], "shiny": int(keys[9]),
                   "ot": keys[10], "gender": int(keys[11]), "caughtloc": keys[12], "form": int(keys[13])}
            fields[f"{keys[9]}{i}"] = mon
            i += 1
        return requests.post(self.import_link, json=data, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}).status_code

    def export_call(self, targetid):
        data = {"auth": self.password,
                "targetid": targetid}
        response = requests.post(self.export_link, json=data,
                                 headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
        return response.status_code

    def read_call(self):
        return json.loads(requests.get(self.read_link).content)
