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


def get_latlng(input_line):
    # TODO: finish this func
    lat_lng = []
    lat, long = input_line.split(',')
    lat = lat.strip()[28:]
    long = long.strip()[:-8]
    lat_lng.append(float(lat))
    lat_lng.append(float(long))
    return lat_lng


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
            # print("Getting {} as {}".format(page_url, full_file_name))
            with open(full_file_name, "wt") as out_file:
                file_text = response.read().decode('utf-8')
                out_file.write(file_text)
                return file_text
    else:
        # print("{} already exists. Opening from {}".format(page_url, full_file_name))
        with open(full_file_name, "r") as existing_page:
            lines = existing_page.read()
            return lines


def get_page_views(html_line):
    pv = int(html_line[38:-10].replace(',', ''))
    return pv


def get_season_data(html_line):
    season_regex = re.compile(r"\['Jan',\d+\].+\['Dec',\d+\]")
    season_regex.match(line)
    # TODO: Figure out how to str -> list

    return season_data


def get_page_data(page_url):
    lat_long = []
    pv = 0
    season_list = []
    data_lines = get_page(page_url)

    for line in data_lines.split('\n'):
        if re.search(r'<td>Location:.+;<', line):
            lat_long = get_latlng(line)
        elif re.search(r'<tr><td>Page Views:&nbsp;</td><td>.+</td></tr>', line):
            pv = get_page_views(line)
        elif re.search(r"\['Jan',\d+\].+\['Dec',\d+\]", line):
            #TODO: function?
            season_list = get_season_data(line)

    data_dict = {'latlong': lat_long,
                 'pv':      pv,
                 'season':  season_list,
                 }

    return data_dict


def get_subarea(parent_url):
    sub_areas = {}

    for line in get_page(parent_url).split('\n'):
        if re.search(r"<span id='leftnav_\d+'", line):
            soup = BeautifulSoup(line, "html.parser")
            sub_areas[soup.a.string] = {}
            sub_areas[soup.a.string]['link'] = soup.a["href"]

    return sub_areas


