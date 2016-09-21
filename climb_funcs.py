from bs4 import BeautifulSoup
import os
import re
import urllib.request
from config import MP_URL


def get_destinations(url):
    page_data = get_page(url)
    soup = BeautifulSoup(page_data, "html.parser")
    dests_raw = soup.find_all('span', {"class": "destArea"})

    destinations = {}

    for dest in dests_raw:
        destinations[str(dest.a.contents)[2:-2]] = {'link': dest.a.get('href')}

    return destinations


def get_page(page_url, data_dir="data"):
    if data_dir not in os.listdir():
        os.mkdir(data_dir)

    if page_url is MP_URL:
        file_name = "mountainproject"
    else:
        file_name = page_url[-9:]

    full_file_name = os.path.join(data_dir, file_name + ".txt")

    if file_name+".txt" not in os.listdir(data_dir):
        with urllib.request.urlopen(page_url) as response:
            print("Getting {} as {}".format(page_url, full_file_name))
            with open(full_file_name, "wt") as out_file:
                file_text = response.read().decode('utf-8')
                out_file.write(file_text)

                return file_text
    else:
        #TODO: return page data if already exists
        print("{} already exists. Opening from {}".format(page_url, full_file_name))
        with open(full_file_name, "r") as existing_page:
            return existing_page.read()


def get_page_data(html_file):
    # TODO: reformat for individual get_data functions?
    lat_long = []
    pv = 0
    season_list = []

    #TODO: get rid of this and connect to soup
    data_lines = html_file.readlines()

    for line in data_lines:

        if re.search(r'<td>Location:.+;<', line):
            lat_long = get_latlong(line)
        elif re.search(r'<tr><td>Page Views:&nbsp;</td><td>.+</td></tr>', line):
            #TODO: function?
            pv = int(line[38:-11].replace(',', ''))
        elif re.search(r"\['Jan',\d+\].+\['Dec',\d+\]", line):
            #TODO: function?
            season_regex = re.compile(r"\['Jan',\d+\].+\['Dec',\d+\]")
            season_regex.match(line)
            # TODO: Figure out how to str -> list

    data_dict = {'latlong':    lat_long,
                 'pv': pv,
                 'season':     season_list,
                 }

    return data_dict


def get_latlong(input_line):
    # TODO: finish this func
    lat_long = []
    lat, long = input_line.split(',')
    lat = lat.strip()[28:]
    long = long.strip()[:-8]
    lat_long.append(float(lat))
    lat_long.append(float(long))
    return lat_long


def get_subarea(parent_url):
    sub_areas = {}

    for line in get_page(parent_url):
        if re.search(r"<span id='leftnav_\d+'", line):
            soup = BeautifulSoup(line, "html.parser")
            sub_areas[soup.a.string] = {}
            sub_areas[soup.a.string]['link'] = soup.a["href"]

    return sub_areas


