import geocoder, requests, json
import googleapiclient
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

AUTHKEY = "AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI"

class SearchFetcher():

    @classmethod
    def get_data(cls,search_string):
        return_list = []
        g = geocoder.ip('me')
        search_data = requests.get(
            'https://maps.googleapis.com/maps/api/place/nearbysearch/json?lo'
            'cation={},{}&radius=1500&feilds=formatted_address,name&type=sho'
            'p&keyword={}&key={}'.format(
                g.latlng[0], g.latlng[1], search_string, AUTHKEY)).json()
        testArr = []
        for results in search_data['results']:
            for info in results:
                if info == 'name':
                    testArr.append(results[info])

        for shop in testArr:
            test4 = requests.get(
                'https://maps.googleapis.com/maps/api/place/findplacefromtext/'
                'json?input={}&inputtype=textquery&fields=photos,formatted_'
                'address,name,opening_hours,rating&locationbias=circle:1500@{},{}&'
                'key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI'.format(shop,
                                                                     g.latlng[
                                                                         0],
                                                                     g.latlng[
                                                                         1]))


            return_list.append({test4.json()['candidates'][0]["name"]: [
                test4.json()['candidates'][0]["name"],
                test4.json()['candidates'][0][
                      "formatted_address"],
                test4.json()['candidates'][0]["rating"]

            ]})

        return return_list
