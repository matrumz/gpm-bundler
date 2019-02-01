from gmusicapi import Mobileclient
import getpass
import re
from functools import reduce

class Session:
    # Private vars
    # _bundle_prefix = "_Bundle-"
    _bundle_prefix = "Super"

    # Public vars
    api = None
    logged_in = False

    def __init__(self, user=None, pw=None):
        self.api = Mobileclient()
        if not user:
            user = input("Please enter Google account: ")
        if not pw:
            pw = getpass.getpass("Please enter password for %s: " % user)
        print("Logging into Google Play Music as %s..." % user, end='', flush=True)
        self.logged_in = self.api.login(user, pw, Mobileclient.FROM_MAC_ADDRESS)
        if self.logged_in:
            print(" successful!")
        else:
            print(" FAILED.")

    def __del__(self):
        if self.logged_in:
            print("Logging out of Google Play Music...", end='', flush=True)
            self.api.logout()
            print(" Done!")

    def get_all_tracks(self):
        return list(set(list(map(lambda track: track["id"], self.api.get_all_songs()))))

    def get_bundled_tracks(self):
        playlists = self.api.get_all_user_playlist_contents()
        bundles = list(filter(lambda pl: re.match(self._bundle_prefix + ".*", pl["name"]), playlists))
        track_ids = []
        if len(bundles):
            tracks = reduce(lambda _tracks, bundle_x: _tracks + bundle_x["tracks"], bundles, [])
            track_ids = list(set(list(map(lambda track: track["trackId"], tracks))))
        return track_ids

    def get_unbundled_tracks(self):
        return list(set(self.get_all_tracks())-set(self.get_bundled_tracks()))
