from datetime import datetime
import math

class Bundler:
    prefix = "_Bundle-"

    def generate_bundles(tracks):
        current_dt = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        bundle_name = Bundler.prefix + (input("Enter bundle name (%s): " % current_dt) or current_dt)

        sets = range(math.ceil(len(tracks)/1000))
        for set in sets:
            print(bundle_name + ("" if len(sets) == 1 else "-"+str(set+1)))
