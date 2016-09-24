from bs4 import BeautifulSoup
import os
import re
import geojson
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
    match = {}
    re_result = re.search(r"\['Jan',\d+\].+\['Dec',\d+\]", html_line)
    if re_result:
        # print(re_result.group())
        line_match = re_result.group().split("],[")
        for month_data in line_match:
            mon = re.search(r"[A-z]{3}", month_data).group()
            num = int(re.search(r"\d{1,4}", month_data).group())
            match[mon] = num
    else:
        match = None

    return match


def get_page_data(page_url):
    lat_long = []
    pv = 0
    season_list = {}
    data_lines = get_page(page_url)

    for line in data_lines.split('\n'):
        if re.search(r'<td>Location:.+;<', line):
            lat_long = get_latlng(line)
        elif re.search(r'<tr><td>Page Views:&nbsp;</td><td>.+</td></tr>', line):
            pv = get_page_views(line)
        elif re.search(r"\['Jan',\d+\].+\['Dec',\d+\]", line):
            season_list = get_season_data(line)

    data_dict = {'latlng': lat_long,
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


def geojsonify(big_data_dict, out_file):
    features = []
    with open(out_file, 'w') as f:
        for area in big_data_dict:
            for sub_area in big_data_dict[area]['sub_areas']:
                sa_data = big_data_dict[area]['sub_areas'][sub_area]
                sa_properties = {'area': area, 'pv': sa_data['pv'], 'season': sa_data['season']}
                sa_point = geojson.Point(sa_data['latlng'])
                if sa_data['latlng']:
                    features.append(geojson.Feature(sub_area, sa_point, sa_properties))

        f.write(geojson.dumps(geojson.FeatureCollection(features)))

        print("Sucess: data written as ", out_file)
