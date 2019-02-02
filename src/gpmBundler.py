#!/usr/bin/env python3

import sys
import os
import json
import asyncio
import libs.GooglePlayMusicController as GPMC

# Change PWD
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load secrets
profile_name = input("Enter profile to load (matrumz): ") or "matrumz"
try:
    path = "../secrets/%s.json" % profile_name
    with open(path) as secrets_file:
        secrets = json.load(secrets_file)
except FileNotFoundError:
    print("'%s' not found" % path)
    sys.exit()

# Load GPM
gpm = GPMC.Session(secrets["GooglePlayMusic"]["user"], secrets["GooglePlayMusic"]["pass"])
while not gpm.logged_in:
    gpm = GPMC.Session()

# Run the program!
gpm.bundle_unbundled_tracks()

# Manually triggering destructor to avoid issue where encodings.ascii is removed by garbage collector before gpm.api.logout()
gpm = None
