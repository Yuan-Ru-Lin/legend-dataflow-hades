import argparse, os, pathlib

import pygama
from pygama.io.build_hit import build_hit

import json

argparser = argparse.ArgumentParser()
argparser.add_argument("input", help="input file", type=str)
argparser.add_argument("--ecal_file", help="energy calibration file for detector", type=str)
argparser.add_argument("--aoe_cal_file", help="a/e calibration file for detector", type=str)
argparser.add_argument("output", help="output file", type=str)
args = argparser.parse_args()


with open(args.ecal_file) as f:
    ecal_dict = json.load(f)


with open(args.aoe_cal_file) as f:
    aoe_dict = json.load(f)

db_dict ={}
db_dict['ecal_pars'] = ecal_dict["cuspEmax_ctc"]["Calibration_pars"]
db_dict['aoe_cut_low']=aoe_dict["Low_cut"]
db_dict['aoe_cut_high']=aoe_dict["High_cut"]
db_dict['aoe_mu_pars']=aoe_dict["Mean_pars"]
db_dict['aoe_sigma_pars']=aoe_dict["Sigma_pars"]

pathlib.Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

build_hit(args.input, db_dict, f_hit =args.output, overwrite=False)
