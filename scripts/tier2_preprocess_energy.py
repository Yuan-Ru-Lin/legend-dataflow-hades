import json, os
import pygama.genpar_tmp.optimiser_macro as om
import pygama.analysis.peak_fitting as pgf
from collections import OrderedDict
import pickle
import argparse
import pathlib
import time
import numpy as np

argparser = argparse.ArgumentParser()
argparser.add_argument("raw_files", help="raw_files", type=str)
argparser.add_argument("output_path", help="output_path", type=str)
argparser.add_argument("--metadata", help="metadata", type=str, required=True)
argparser.add_argument("--db_dict_path", help="db_dict_path", type=str, required=True)
argparser.add_argument("--peak", help="peak", type=float, required=True)
args = argparser.parse_args()

peaks_keV = np.array([238.632,   583.191, 727.330, 860.564, 1620.5, 2614.553])
kev_widths = [(10,10), (25,40), (25,40),(25,40),(25,40), (50,50)]
funcs = [pgf.gauss_step, pgf.radford_peak, pgf.radford_peak,pgf.radford_peak,pgf.radford_peak, pgf.radford_peak]
    
peak_idx = np.where(peaks_keV == args.peak)[0][0]
func = funcs[peak_idx]
kev_width = kev_widths[peak_idx]

with open(args.raw_files) as f:
    files = f.read().splitlines()

raw_file = sorted(om.run_splitter(files), key=len)[-1]

f_config = os.path.join(f"{args.metadata}", "config_dsp.json")
with open(f_config, 'r') as config_file:
    config_dict = json.load(config_file, object_pairs_hook=OrderedDict)

with open(args.db_dict_path, 'r') as t:
    db_dict = json.load(t)

wf_idxs = om.event_selection(raw_file, config_dict, db_dict, peaks_keV, peak_idx, kev_width)

o_config = os.path.join(f"{args.metadata}", "opt_config.json")
with open(o_config, 'r') as o:
    opt_dict = json.load(o)
print('Loaded configs')

parameters=['zacEmax', 'trapEmax', 'cuspEmax']

t0 = time.time()

grid_out = om.run_optimisation_multiprocessed(raw_file, opt_dict, config_dict, db_dict = db_dict, 
            fom = om.fom_all_fit, cuts = wf_idxs, n_events=10000,
            processes=15, parameter=parameters, func=func,
            peak=args.peak, kev_width=kev_width)
    
t1 = time.time()

print(f'Calculated Grid in {t1-t0}')

save_dict = {}
for i,param in enumerate(parameters):
    save_dict[param] = grid_out[i]
    
pathlib.Path(os.path.dirname(args.output_path)).mkdir(parents=True, exist_ok=True)
with open(args.output_path,"wb") as f:
    pickle.dump(save_dict,f)