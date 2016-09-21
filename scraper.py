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
    mp_data[area]["sub_areas"] = get_subarea(MP_URL+dest_areas[area]['link'])
    print(area, ' ', MP_URL+dest_areas[area]['link'])
    for sub_area in mp_data[area]["sub_areas"]:
        print("    ", sub_area, "  ", MP_URL+mp_data[area]["sub_areas"][sub_area]['link'])


print(len(dest_areas))
print(mp_data["Tennessee"]['link'])
print(mp_data["Tennessee"]['pv'])
print(mp_data["Tennessee"]['latlong'])
