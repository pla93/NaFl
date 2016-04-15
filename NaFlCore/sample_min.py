#
# this script is minimizing the corpus of sample files keeping the code coverage of the corpus
#

import os
import copy
import random
import shutil
from NaFlCore import run_under_pin, doInitStuff, initialize_logging


doInitStuff()
ml = initialize_logging()
samples_dir = os.path.join(os.getcwd(), 'samples')
min_samples_dir = os.path.join(os.getcwd(), 'min_samples')
max_coverage = set()

sample_files = [os.path.join(samples_dir, f) for f in os.listdir(samples_dir) if os.path.isfile(os.path.join(samples_dir, f))]

cov_map = {}

ml.info("[*] Starting sample corpus minimization process...")

if len(sample_files) == 0:
    ml.error("[-] No files in %s found." % (samples_dir))

for sample_file in sample_files:
    ml.info("[*] Processing %s" % (sample_file))
    set_bits = set()
    sample_bitmap = run_under_pin(sample_file)

    # maybe deal with hit count here?
    for index, value in enumerate(sample_bitmap):
        if value > 0:
            set_bits.add(index)

    cov_map[sample_file] = copy.copy(set_bits)
    max_coverage.update(set_bits)

while len(cov_map) > 0:
    max_coverage_value = max([len(s) for s in cov_map.values()])
    files_max_coverage = [file for file, coverage_set in cov_map.items() if len(coverage_set) == max_coverage_value]

    rfile_selected = random.choice(files_max_coverage)
    selected_set = cov_map.pop(rfile_selected)

    for file, coverage_set in cov_map.items():
        tmp = coverage_set - selected_set
        if len(tmp) == 0:
            del cov_map[file]
        else:
            coverage_set = tmp

    shutil.copy(rfile_selected, min_samples_dir)

old_count = len(os.listdir(samples_dir))
new_count = len(os.listdir(min_samples_dir))

print "### Reduced samples from %s files to %s files keeping code coverage of %s / 64k covered paths. ###" % (old_count, new_count, len(max_coverage))






