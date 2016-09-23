from bs4 import BeautifulSoup
import os
import re
import urllib.request
from climb_funcs import *
from config import MP_URL

# Check to see if homepage is downloaded, if not download it

    # Extract destination areas from homepage

# For each destination area, check to see if exists, download it, and extract data


dest_areas = get_destinations(MP_URL)
mp_data = dest_areas

for area in dest_areas:
    print(area)
    page_link = MP_URL+mp_data[area]['link']
    mp_data[area] = get_page_data(page_link)
    mp_data[area]["sub_areas"] = get_subarea(page_link)
    print(mp_data[area])
    for sub_area in mp_data[area]["sub_areas"]:
        print("    ", sub_area, "  ", MP_URL+mp_data[area]["sub_areas"][sub_area]['link'])
        pass

