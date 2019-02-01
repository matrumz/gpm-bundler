from datetime import datetime
import math

class Bundler:
    prefix = "_Bundle-"
    bundle_size = 1000

    def generate_bundles(tracks):
        current_dt = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        bundle_name = Bundler.prefix + (input("Enter bundle name (%s): " % current_dt) or current_dt)

        sets = range(math.ceil(len(tracks)/Bundler.bundle_size))
        for set in sets:
            print(bundle_name + ("" if len(sets) == 1 else "-"+str(set+1)))
