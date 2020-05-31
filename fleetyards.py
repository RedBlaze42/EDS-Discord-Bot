import requests
import urllib
import json
import dateutil.parser
import time


class FleetYardsAPI():

    def __init__(self,username,password,org_name):
        self.base_url = "https://api.fleetyards.net"
        self.token=self._login(username,password)
        self.org_name = org_name

    def _login(self,login,password):
        url=urllib.parse.urljoin(self.base_url,"/v1/sessions")
        request=requests.post(url,data={"login":login,"password":password})

        if request.status_code != 200:
            raise Exception(request.text)

        return request.json()["token"]

    def _get(self,url):
        url=urllib.parse.urljoin(self.base_url,url)
        retry=4
        while retry>0:
            request=requests.get(url, headers={'Authorization': "Bearer {}".format(self.token)})
            if request.status_code !=200:
                retry-=1
                time.sleep(1)
            else:
                try:
                    return request.json()
                except json.decoder.JSONDecodeError:
                    raise Exception("Returned to docs {}".format(url))
        raise Exception("Error url {} with text: {}".format(url,request.text))

    @property
    def members(self):
        data=self._get("v1/fleets/{}/members".format(self.org_name))
        return data

    @property
    def member_names(self):
        data=self.members
        return [member["username"] for member in data]

    def get_hangar(self,username):
        data=self._get("/v1/vehicles/{}".format(username))
        hangar=list()
        for ship in data:
            hangar.append(Vehicle(ship))
        return hangar

    def compare_hangars(self,hangar1,hangar2):
        additions,removals=list(),list()

        #Check for removals
        for ship in hangar1:
            if not ship.id in [ship2.id for ship2 in hangar2]:
                removals.append(ship)

        #Check for additions
        for ship in hangar2:
            if not ship.id in [ship2.id for ship2 in hangar1]:
                additions.append(ship)

        return additions,removals

    def compare_members(self,members1,members2):
        additions,removals=list(),list()

        #Check for removals
        for member in members1:
            if not member["username"] in [temp["username"] for temp in members2]:
                removals.append(member)

        #Check for additions
        for member in members2:
            if not member["username"] in [temp["username"] for temp in members1]:
                additions.append(member)

        return additions,removals

    def get_corp_hangar(self):
        corp_hangar = list()
        for member in self.member_names:
            corp_hangar+=self.get_hangar(member)
        return corp_hangar

    def get_all_corp_hangars(self):
        hangars=dict()
        for member in self.member_names:
            hangars[member]=self.get_hangar(member)
        return hangars

    def fleet_value(self):
        return sum([ship.value for ship in self.get_corp_hangar()])
    
    def fleet_auec_value(self):
        return sum([ship.auec_value for ship in self.get_corp_hangar()])

class Vehicle():

    def __init__(self,json_data):
        self.data = json_data
        self.id=self.data["id"]
        self.custom_name=self.data["name"]
        self.model_data=self.data["model"]
        self.model_id=self.model_data["id"]
        self.model_name=self.model_data["name"]
        self.value=int(self.model_data["pledgePrice"]) if self.model_data["pledgePrice"] is not None else 0
        self.auec_value=int(self.model_data["price"]) if self.model_data["price"] is not None else 0
        self.brand=self.model_data["manufacturer"]
        self.brand_name=self.brand["name"]
        self.cargo=int(self.model_data["cargo"])
        self.image_url=self.model_data["storeImage"]
        self.medium_image_url=self.model_data["storeImageMedium"]
        self.crew=self.model_data["maxCrew"]
        self.size=self.model_data["size"]
        self.updated_at=dateutil.parser.parse(self.data["updatedAt"])