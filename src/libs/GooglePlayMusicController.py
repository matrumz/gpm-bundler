from gmusicapi import Mobileclient
import getpass

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
        self.logged_in = self.api.login(user, pw, Mobileclient.FROM_MAC_ADDRESS)
        if self.logged_in:
            print("Google Play Music login successful.")
        else:
            print("Google Play Music login FAILED.")

    def __del__(self):
        if self.logged_in:
            print("Logging out of Google Play Music...")
            self.api.logout()
