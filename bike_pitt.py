
import argparse
import collections
import csv
import json
import glob
import math
import os
import pandas
import re
import requests
import string
import sys
import time
import xml


class Bike():
    def __init__(self, baseURL, station_info, station_status):
        # initialize the instance
        pass
        station_infoURL = baseURL + '/station_information.json'
        station_statusURL = baseURL + '/station_status.json'

        self.stationinfo = requests.get(station_infoURL)
        self.stationstatus = requests.get(station_statusURL)


    def total_bikes(self):
        # return the total number of bikes available
        availablebikes = self.stationstatus.json()

        i = 0
        for station in availablebikes['data']['stations']:
            i += station['num_bikes_available']
        return i

    def total_docks(self):
        # return the total number of docks available
        availabledocks = self.stationstatus.json()

        i = 0
        for station in availabledocks['data']['stations'] :
            i += station['num_docks_available']
        return i

    def percent_avail(self, station_id):
        # return the percentage of available docks
        data = self.stationstatus.json()

        for station in data['data']['stations'] :
            if str(station_id) == station['station_id']:
                availdocks = station['num_docks_available']
                availbikes = station['num_bikes_available']
                percentavail = math.floor(availdocks / (availdocks + availbikes) * 100)
                return f"{percentavail}%"

        return ""


    def closest_stations(self, latitude, longitude):
        # return the stations closest to the given coordinates

        info = self.stationinfo.json()

        emptylist = [] # make an empty list that we will later append the list of stations into

        for station in info['data']['stations'] :
            listofstations = [station['station_id'], station['name'], self.distance(latitude, longitude, station['lat'], station['lon'])]

            emptylist.append(listofstations) # appending list of stations into empty list

        # sort by distance to get the 3 closest ones with sorted function

        emptylist.sort( key = lambda x:x[2])
        dict = {emptylist[0][0]: emptylist[0][1], emptylist[1][0]: emptylist[1][1], emptylist[2][0]: emptylist[2][1]}


        return dict

    def closest_bike(self, latitude, longitude):
        # return the station with available bikes closest to the given coordinates

        info = self.stationinfo.json()
        status = self.stationstatus.json()

        emptylist = [] # create an empty list again

        for station in info['data']['stations'] :
            listofstations = [station['station_id'], station['name'], self.distance(latitude, longitude, station['lat'], station['lon'])]
            emptylist.append(listofstations)

        #  go through station status to  find the number of available bikes
        i = 0
        for station in status['data']['stations'] :
            emptylist[i].append(station['num_bikes_available'])
            i += 1

        # find the 3 closest stations
        emptylist.sort( key = lambda x:x[2])
        

        # check which of these 3 stations have a bike available
        dict = {}

        for i in emptylist :
            if(i[3] != 0) :
                dict[i[0]] = i[1]
                break
        return dict



    def station_bike_avail(self, latitude, longitude):
        # return the station id and available bikes that correspond to the station with the given coordinates

        info =  self.stationinfo.json()
        status = self.stationstatus.json()

        emptystring = ' '

        for station in info['data']['stations'] :
            if station['lat'] == latitude and station['lon'] ==  longitude :
                emptystring = station['station_id']

        j = -1
        for station in status['data']['stations'] :
            if emptystring == station['station_id'] :
                j = station['num_bikes_available']

        if emptystring == '' :
            return {}
        elif j == -1 :
            return {}
        else :
            return {emptystring : j}


    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (
                    1 - math.cos((lon2 - lon1) * p)) / 2
        return 12742 * math.asin(math.sqrt(a))


# testing and debugging the Bike class

if __name__ == '__main__':
    instance = Bike('https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en', '/station_information.json',
                    '/station_status.json')
    print('------------------total_bikes()-------------------')
    t_bikes = instance.total_bikes()
    print(type(t_bikes))
    print(t_bikes)
    print()

    print('------------------total_docks()-------------------')
    t_docks = instance.total_docks()
    print(type(t_docks))
    print(t_docks)
    print()

    print('-----------------percent_avail()------------------')
    p_avail = instance.percent_avail(342885)  # replace with station ID
    print(type(p_avail))
    print(p_avail)
    print()

    print('----------------closest_stations()----------------')
    c_stations = instance.closest_stations(40.444618, -79.954707)  # replace with latitude and longitude
    print(type(c_stations))
    print(c_stations)
    print()

    print('-----------------closest_bike()-------------------')
    c_bike = instance.closest_bike(40.444618, -79.954707)  # replace with latitude and longitude
    print(type(c_bike))
    print(c_bike)
    print()

    print('---------------station_bike_avail()---------------')
    s_bike_avail = instance.station_bike_avail(40.438761,
                                               -79.997436)  # replace with exact latitude and longitude of station
    print(type(s_bike_avail))
    print(s_bike_avail)
