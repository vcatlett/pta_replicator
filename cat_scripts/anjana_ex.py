from __future__ import division
import matplotlib
import matplotlib.pyplot as plt

import numpy as np, pickle
import math, sys, os, glob, json
from astropy import units as u
from sklearn.neighbors import KernelDensity

import pint
from pint import toa
from pint import models
from pint.residuals import Residuals
from pint.simulation import make_fake_toas_fromMJDs
pint.logging.setup(sink=sys.stderr, level="ERROR", usecolors=True)

import pta_replicator
from pta_replicator import simulate
from pta_replicator import white_noise
from pta_replicator import red_noise

from enterprise.pulsar import Pulsar as ePsr

import argparse
parser = argparse.ArgumentParser(
    description="I'll create a fake NG20 dataset with a EFAC, EQUAD and GWB as observed in NG15, and a FACTOR boosting the toaerrors so that the 15year slice of this NG20 dataset has a sensitivity consistent with that observed in NG15 ."
)
parser.add_argument(
    "--rngseed",
    help="Seed for GWB",
    default=404
)

args = parser.parse_args()
seed_gwb = int(args.rngseed)
seed_efac_equad = 10660+seed_gwb
seed_red = 19870+seed_gwb
print('seed_gwb=',seed_gwb)

#from plot_utils import make_residual_plot
#plotting function
def make_residual_plot(psr, save=False, simdir='pint_sims1/'):

    # switch to rainbow colormap grouped by telescopes
    colors = {
                "CHIME": "#FFA733",
                "327_ASP": "#BE0119",
                "327_PUPPI": "#BE0119",
                "430_ASP": "#FD9927",
                "430_PUPPI": "#FD9927",
                "L-wide_ASP": "#BDB6F6",
                "L-wide_PUPPI": "#BDB6F6",
                "Rcvr1_2_GASP": "#79A3E2",
                "Rcvr1_2_GUPPI": "#79A3E2",
                "Rcvr1_2_VEGAS": "#79A3E2",
                "Rcvr_800_GASP": "#8DD883",
                "Rcvr_800_GUPPI": "#8DD883",
                "Rcvr_800_VEGAS": "#8DD883",
                "S-wide_ASP": "#C4457A",
                "S-wide_PUPPI": "#C4457A",
                "1.5GHz_YUPPI": "#EBADCB",
                "3GHz_YUPPI": "#E79CC1",
                "6GHz_YUPPI": "#DB6BA1",
            }

    fig, axs = plt.subplots(1, 1)

    flags = list(np.unique(psr.toas['f']))


    for f in flags:

        idx = (psr.toas['f'] == f)

        axs.errorbar(psr.toas[idx].get_mjds(), psr.residuals.calc_time_resids()[idx],
                     yerr=psr.toas[idx].get_errors(), marker='.', ls='', alpha=0.5,
                     label=f, color=colors[f])

    plt.title('{0} -- {1} TOAs'.format(psr.name, len(psr.toas)))
    plt.xlabel('MJD')
    plt.ylabel('Residual [s]')
    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig(simdir + '/{0}.png'.format(psr.name))



#get various noise dictionaries
#Nihan's noise dict for 15yr
nihans_dict = '15yr_v1_fl_fwn_dict.json'
with open(nihans_dict,'r') as f:
    nihans_noise = json.load(f)

#NG20 real noise dict
ng20_noise_dict = 'ng20_v1p1_dmx_noise_dict.json'
#from https://drive.google.com/drive/folders/1GQXnpyRglqPHwgQs6vE8VK-6VoL9WbSj
with open(ng20_noise_dict,'r') as f:
    ng20_noise_real = json.load(f)

#make a new noise dict with only chime and vegas pulsars
chime_vegas_noise_dict = {}
for k, v in ng20_noise_real.items():
    new_key = k.replace("t2equad", "equad")
    if "CHIME" in k or "YUPPI" in k or "VEGAS" in k or "J0125-2327" in k or "J0154+1833" in k or "J0614-3329" in k or "J0621+2514" in k or "J0732+2314" in k or "J0751+1807" in k or "J1022+1001" in k or "J1803+1358" in k or "J2022+2534" in k or "J2039-3616" in k or "J2150-0326" in k:
        print(k)
        chime_vegas_noise_dict[new_key] = v

#update nihans noise dict with chime and vegas pulsars from ng20
nihans_noise.update(chime_vegas_noise_dict)

#rn_dict_file
rn_dict_file = '20yr_noisedict_rn+curn-bpl.json'
with open(rn_dict_file, 'r') as f:
    rn_dict = json.load(f)
print('Noise dicts loaded!')


datadir = './'
#Lets move on to v1p1 now
parfiles = list(np.genfromtxt(datadir + 'parfile_names_v1p1.txt', dtype='str'))
timfiles = list(np.genfromtxt(datadir + 'timfile_names_v1p1.txt', dtype='str'))


print('Making simulation with noise only...')

psrs = []
noise_dict = {}
noise_params = nihans_noise
for ii in range(len(parfiles)):
    print('Working on {0}...'.format(parfiles[ii]))
    print(parfiles[ii], timfiles[ii])
    psr = simulate.load_pulsar(parfiles[ii], timfiles[ii], ephem='DE440')

    #function to grab white noise inputs from a noise dictionary
    p=psr.name
    noise_dict[p] = {}
    noise_dict[p]['log10_equads'] = []
    noise_dict[p]['efacs'] = []
    noise_dict[p]['log10_ecorrs'] = []
    for ky in list(noise_params.keys()):
        if p in ky:
            if 'equad' in ky:
                noise_dict[p]['log10_equads'].append([ky.replace(p + '_' , '').replace('_log10_t2equad', ''), noise_params[ky]])
            if 'efac' in ky:
                noise_dict[p]['efacs'].append([ky.replace(p + '_' , '').replace('_efac', ''), noise_params[ky]])
            if 'ecorr' in ky:
                noise_dict[p]['log10_ecorrs'].append([ky.replace(p + '_' , '').replace('_log10_ecorr', ''), noise_params[ky]])
            if 'gamma' in ky:
                noise_dict[p]['rn_gamma'] = noise_params[ky]
            if 'log10_A' in ky:
                noise_dict[p]['rn_log10_amp'] = noise_params[ky]

    noise_dict[p]['log10_equads'] = np.array(noise_dict[p]['log10_equads'])
    noise_dict[p]['efacs'] = np.array(noise_dict[p]['efacs'])
    noise_dict[p]['log10_ecorrs'] = np.array(noise_dict[p]['log10_ecorrs'])

    # remove red noise from the model (we will add it back later)
    if 'PLRedNoise' in psr.model.components.keys():
        psr.model.remove_component('PLRedNoise')

    # remove Shapiro delay parameters if they are in the binary model
    if 'BinaryDD' in psr.model.components.keys():
        if 'SINI' in psr.model.components['BinaryDD'].params:
            psr.model.components['BinaryDD'].remove_param('SINI')

        if 'M2' in psr.model.components['BinaryDD'].params:
            psr.model.components['BinaryDD'].remove_param('M2')

    elif 'BinaryELL1' in psr.model.components.keys():

        if 'SINI' in psr.model.components['BinaryELL1'].params:
            psr.model.components['BinaryELL1'].remove_param('SINI')

        if 'M2' in psr.model.components['BinaryELL1'].params:
            psr.model.components['BinaryELL1'].remove_param('M2')

    psr.generate_daily_avg_toas(FACTOR=1.6,ideal=True) #FACTOR = sqrt(2.54)
    white_noise.add_measurement_noise(psr, efac = noise_dict[psr.name]['efacs'][:,1].astype(float),
                          log10_equad = noise_dict[psr.name]['log10_equads'][:,1].astype(float),
                          flagid = 'f', flags = noise_dict[psr.name]['efacs'][:,0],
                          seed = seed_efac_equad + ii)

    for _ in range(3):
        psr.fit(fitter='gls')

    red_noise.add_red_noise(psr, log10_amplitude = rn_dict[psr.name + '_red_noise_log10_A'],
                            spectral_index = rn_dict[psr.name + '_red_noise_gamma'],
                            components = 30, seed = seed_red + ii)

    for _ in range(3):
        psr.fit(fitter='gls')

    simdirMain = '../data/NG20v1p1woGWB/'
    if not os.path.exists(simdirMain):
        os.mkdir(simdirMain)
    rln_name = 'realization_'+str(seed_gwb)
    simdir = os.path.join(simdirMain,rln_name)
    if not os.path.isdir(simdir):
        os.mkdir(simdir)

    make_residual_plot(psr, save=True, simdir=simdir)

    psr.write_partim(simdir + '/'+ psr.name + '.par', simdir + '/' + psr.name + '.tim', tempo2=False)
    newpar = simdir + '/'+ psr.name + '.par'
    newtim = simdir + '/' + psr.name + '.tim'
    psr_for_feather = ePsr(newpar, newtim)
    psr_for_feather.to_feather(simdir + '/' + psr.name + '.feather') #also make feather

    psrs.append(psr)

print('Making simulation with GWB...')
A_gwb, gamma_gwb = 6.4e-15, 3.2 #median values from ng15 evidence paper
red_noise.add_gwb(psrs, log10_amplitude = np.log10(A_gwb), spectral_index = gamma_gwb,
                  seed = seed_gwb)

simdirMain = '../data/NG20v1p1wGWB/'
if not os.path.exists(simdirMain):
    os.mkdir(simdirMain)
rln_name = 'realization_'+str(seed_gwb)
simdir = os.path.join(simdirMain,rln_name)
if not os.path.isdir(simdir):
    os.mkdir(simdir)

for psr in psrs:

    print('Refitting residuals for {0}...'.format(psr.name))

    for _ in range(3):
        try:
            psr.fit(fitter='downhill')
        except:
            print('Downhill fitter didn\'t work for {0}'.format(psr.name))
            print('Trying to fit with gls fitter...'.format(psr.name))

            try:
                psr.fit(fitter='gls')
            except:
                print('gls fitter didn\'t work either!')

    make_residual_plot(psr, save=True, simdir=simdir)

    psr.write_partim(simdir + '/' + psr.name + '.par', simdir + '/' + psr.name + '.tim', tempo2=False)
    newpar = simdir + '/'+ psr.name + '.par'
    newtim = simdir + '/' + psr.name + '.tim'
    psr_for_feather = ePsr(newpar, newtim)
    psr_for_feather.to_feather(simdir + '/' + psr.name + '.feather') #also make feather
print('Done!')