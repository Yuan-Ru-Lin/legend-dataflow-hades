import numpy as np
import os,json
import pathlib
import argparse

from pygama.pargen.aoe_cal import cal_aoe


argparser = argparse.ArgumentParser()
argparser.add_argument("files", help="files", nargs='*',type=str)
argparser.add_argument("--detector", help="detector", type=str, required=True)
argparser.add_argument("--ecal_file", help="ecal_file",type=str, required=True)
argparser.add_argument("--plot_file", help="plot_file",type=str)
argparser.add_argument("--aoe_cal_file", help="aoe_cal_file",type=str)
args = argparser.parse_args()

with open(args.files[0]) as f:
    files = f.read().splitlines()
    files = sorted(files)

with open(args.ecal_file, 'r') as o:
    cal_dict = json.load(o)

energy_param = 'cuspEmax'
cal_energy_param = 'cuspEmax_ctc'

if args.detector == "V05266A" or args.detector=="V04549A": 
    cut_parameters = {"bl_std":4,"pz_std":4}
else:
    cut_parameters = {"bl_mean":4,"bl_std":4,"pz_std":4}

out_dict = cal_aoe(files, cal_dict, energy_param, cal_energy_param, dt_corr=False, cut_parameters=cut_parameters, plot_savepath=args.plot_file)

if args.aoe_cal_file is not None:
    pathlib.Path(os.path.dirname(args.aoe_cal_file)).mkdir(parents=True, exist_ok=True)
    with open(args.aoe_cal_file, 'w') as w:
        json.dump(out_dict,w, indent=4)