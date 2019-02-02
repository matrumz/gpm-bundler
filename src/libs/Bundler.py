from datetime import datetime
import math

class Bundler:
    prefix = "_Bundle-"
    bundle_size = 1000

    def generate_bundles(tracks):
        current_dt = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        bundle_base_name = Bundler.prefix + (input("Enter bundle name (%s): " % current_dt) or current_dt)

        sets = range(math.ceil(len(tracks)/Bundler.bundle_size))
        for set in sets:
            bundle_name = bundle_base_name + ("" if len(sets) == 1 else "-"+str(set+1))
            bundle_contents = tracks[set*Bundler.bundle_size : ((set+1)*Bundler.bundle_size)]
            yield bundle_name, bundle_contents
