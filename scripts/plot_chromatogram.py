#!/usr/bin/env python

import os
import sys
import numpy as np
import pymzml
import matplotlib
import matplotlib.pyplot as plt

class msData:
    def __init__(self, mzml_file,min_rt=0,min_mz=0,max_mz=0):
        print("Loading mzML")
        self.level = list()
        self.bp = list()
        self.scan_id = list()
        self.scan_rt = list()
        self.mzml_file = mzml_file
        self.run = pymzml.run.Reader(mzml_file)

        for n, spec in enumerate(self.run):

            scan_start = spec['scan start time']

            if scan_start < min_rt:
                print(scan_start)
                continue
            else:
                self.scan_id.append(spec.ID)
                self.level.append(spec['ms level'])
                self.scan_rt.append(scan_start)

                scan_bp = spec['base peak intensity']
                self.bp.append(scan_bp)

        self.num_scans = len(self.scan_id)


msdata = msData(sys.argv[1])
msdata_bp  = np.asarray(msdata.bp)
msdata_scan_rt = np.asarray(msdata.scan_rt)

plt.gcf().clear()
plt.plot(msdata.scan_rt,msdata.bp)
plt.xlabel("retention time")
plt.ylabel("BP Intensity")
plt.savefig("{}.{}".format(sys.argv[1],'bpplot.pdf'))
