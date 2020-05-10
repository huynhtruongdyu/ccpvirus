from datetime import date, datetime
from urllib.request import urlopen
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd


class County():
    def __init__(self, name, iso2="", iso3="", confirmed=0, recovered=0, deaths=0, lastUpdate=""):
        self.name = name
        self.iso2 = iso2
        self.iso3 = iso3
        self.confirmed = confirmed
        self.recovered = recovered
        self.deaths = deaths
        self.lastUpdate = lastUpdate

    def __str__(self):
        return "Name: {} - {} - {} \n  -Confirmed: {}\n  -Recovered: {}\n  -Deaths: {}\n  -Last update: {}".format(
            self.name,
            self.iso2,
            self.iso3,
            self.confirmed,
            self.recovered,
            self.deaths,
            self.lastUpdate)


countries = []


def get_data():
    print("updating...")
    url_world = "https://covid19.mathdro.id/api"
    url_countries = "https://covid19.mathdro.id/api/countries"

    url_world_json = urlopen(url_world)
    url_countries_json = urlopen(url_countries)

    word_raw_data = json.loads(url_world_json.read())

    world = County(name='World',
                   confirmed=word_raw_data['confirmed']['value'],
                   recovered=word_raw_data['recovered']['value'],
                   deaths=word_raw_data['deaths']['value'],
                   lastUpdate=word_raw_data['lastUpdate'])

    countries_raw_data = json.loads(url_countries_json.read())
    countries_list = countries_raw_data['countries']

    for item in countries_list:
        country = County(name=item.get('name'), iso2=item.get('iso2'), iso3=item.get('iso3'))
        if country.iso3 is not None:
            countries.append(country)

    index = 0
    total_countries = len(countries_list)

    for country in countries:
        base_url = "https://covid19.mathdro.id/api/countries/"
        try:
            country_url = base_url + str(country.iso3)
            url_country_json = urlopen(country_url)
            country_raw_data = json.loads(url_country_json.read())
            country.recovered = country_raw_data.get('recovered').get('value')
            country.deaths = country_raw_data.get('deaths').get('value')
            country.confirmed = country_raw_data.get('confirmed').get('value')
            country.lastUpdate = country_raw_data.get('lastUpdate')
        except:
            countries.pop(index)
        finally:
            curr = str(index) + " /"
            total = str(total_countries)
            print(curr, total)
            index += 1
    countries.append(world)


def write_data_to_file():
    with open('data/countries.txt', 'w') as f:
        for country in countries:
            f.write(country.name + "\n")

    with open('data/iso3.txt', 'w') as f:
        for country in countries:
            f.write(country.iso3 + "\n")

    with open('data/confirmed.txt', 'w') as f:
        for country in countries:
            f.write(str(country.confirmed) + "\n")

    with open('data/recovered.txt', 'w') as f:
        for country in countries:
            f.write(str(country.recovered) + "\n")

    with open('data/deaths.txt', 'w') as f:
        for country in countries:
            f.write(str(country.deaths) + "\n")

    with open('data/last_update.txt', 'w') as f:
        for country in countries:
            f.write(country.lastUpdate + "\n")


def check_update():
    url_world = "https://covid19.mathdro.id/api"
    url_world_json = urlopen(url_world)
    word_raw_data = json.loads(url_world_json.read())
    world = County(name='World',
                   confirmed=word_raw_data['confirmed']['value'],
                   recovered=word_raw_data['recovered']['value'],
                   deaths=word_raw_data['deaths']['value'],
                   lastUpdate=word_raw_data['lastUpdate'])
    confirmed = open("data/confirmed.txt").read().split('\n')
    old_confirmed = int(confirmed[-2])
    return True if world.confirmed > old_confirmed else False


def update_data():
    if check_update():
        get_data()
        write_data_to_file()

        with open('data/log.txt', 'r') as file:
            lines = file.readlines()
            time = lines[-1]
            print("Updated from last update: {}".format(time))

        with open('data/log.txt', 'a+') as file:
            file.write(str(datetime.now()) + "\n")

    else:
        with open('data/log.txt', 'r') as file:
            lines = file.readlines()
            time = lines[-1]
            print("No change from last update: {}".format(time))



update_data()

countries = open("data/countries.txt").read().split('\n')
iso3 = open("data/iso3.txt").read().split('\n')
confirmed = open("data/confirmed.txt").read().split('\n')
deaths = open("data/deaths.txt").read().split('\n')
recovered = open("data/recovered.txt").read().split('\n')
last_update = open("data/last_update.txt").read().split('\n')

if len(countries) == len(confirmed) == len(deaths) == len(recovered) == len(recovered):
    np_countries = np.array(countries[:-1])
    np_iso3 = np.array(iso3)[:-1]
    np_confirmed = np.array(confirmed[:-1]).astype(int)
    np_deaths = np.array(deaths[:-1]).astype(int)
    np_recovered = np.array(recovered[:-1]).astype(int)
    np_last_update = np.array(last_update[:-1])
    print("So lieu trung khop: {}".format(len(countries)-1))
    print()
    # world = County(np_countries[-1], 'na', 'na', np_confirmed[-1], np_recovered[-1], np_deaths[-1], np_last_update[-1])
    # index_VNM = np.where(np_countries == 'Vietnam')
    # print(np_countries[index_VNM])

    data = pd.DataFrame({
        'Country': np_countries,
        # 'ISO3': np_iso3,
        'Confirmed': np_confirmed,
        'Deaths': np_deaths,
        'Recovered': np_recovered,
        # 'Last Updated': np_last_update,
    })
    # data.index = np_iso3
    # data.index += 1
    # pd.set_option('display.max_rows', data.shape[0] + 1)

    print(data.tail())

    
else:
    print("So lieu khong trung khop")
