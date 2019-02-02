from gmusicapi import Mobileclient
import getpass
import re
from functools import reduce
from libs.Bundler import Bundler

class Session:
    # Private vars

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
            print(" done!")

    def get_all_tracks(self):
        return list(set(list(map(lambda track: track["id"], self.api.get_all_songs()))))

    def get_bundled_tracks(self):
        playlists = self.api.get_all_user_playlist_contents()
        bundles = list(filter(lambda pl: re.match(Bundler.prefix + ".*", pl["name"]), playlists))
        track_ids = []
        if len(bundles):
            tracks = reduce(lambda _tracks, bundle_x: _tracks + bundle_x["tracks"], bundles, [])
            track_ids = list(set(list(map(lambda track: track["trackId"], tracks))))
        return track_ids

    def get_unbundled_tracks(self):
        return list(set(self.get_all_tracks())-set(self.get_bundled_tracks()))

    def bundle_unbundled_tracks(self):
        created_playlists = []
        playlist = None
        for name, contents in Bundler.generate_bundles(self.get_unbundled_tracks()):
            try:
                playlist = (name, self.api.create_playlist(name, "gpmBundler generated playlist"))
            except Error as create_playlist_e:
                print(create_playlist_e)
                print("Failed to create playlist '%s'. Purging..." % name)
                self.purge_playlists(created_playlists)
                break
            else:
                created_playlists.append(playlist)
                try:
                    self.api.add_songs_to_playlist(playlist[1], contents)
                except Error as add_songs_e:
                    print(add_songs_e)
                    print("Failed to add songs to playlist '%s'" % name)
                    self.purge_playlists(created_playlists)
                    break
                else:
                    print("Playlist %s created and populated." % name)

    def purge_playlists(self, playlists):
        for p in playlists:
            try:
                self.api.delete_playlist(p[1])
            except:
                print("Failed to delete playlist '%s'" % p[0])
            else:
                print("Deleted playlist '%s'" % p[0])
