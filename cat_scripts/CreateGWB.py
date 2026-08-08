from glob import glob

import astropy.units as u
import discovery as ds
import numpy as np
import pandas as pd

from pta_replicator.spharmORFbasis import correlated_basis

# turnover=False,
# clm=[np.sqrt(4.0 * np.pi)],
# lmax=0,
# f0=1e-9,
# beta=1,
# power=1,
# userSpec=None,
# npts=600,
# howml=10,

N_PSR = 67
N_STAR = 200_000
N_PTS = 600
HOWML = 10

LOG10A_GWB = -15.0
AMP_GWB = 10**LOG10A_GWB
GAMMA_GWB = 13.0 / 3.0


## Load pulsars
def load_pulsars():
    FPATH = "/home/catlettv/novus/sandbox/repos/VIPER/VIPER-2026/results/A_15__gamma_13_3/feather/*.feather"
    psr_list = [ds.Pulsar.read_feather(psrfile) for psrfile in sorted(glob(FPATH))]
    return psr_list


## Set up time frame
def get_t_range():
    # [TODO] Hardcoded path!
    times_df = pd.read_csv(
        "/home/catlettv/novus/sandbox/repos/pta_replicator_fork/data/times.csv"
    )
    t0 = np.min(times_df["START_MJD"]) * u.day
    t1 = np.max(times_df["STOP_MJD"]) * u.day
    return t0.to(u.s), t1.to(u.s)


def get_ts(t0, t1, pad=1 * u.day):
    # [TODO] Add option for cadence
    pad = pad.to(u.s)
    start = (t0 - pad).value
    stop = (t1 + pad).value
    ts = np.linspace(start, stop, N_PTS)
    return ts


## Get frequencies
def get_fs(ts):
    dur = ts[-1] - ts[0]
    dt = dur / len(ts)
    step = 1 / (dur * HOWML)
    min_f = step
    max_f = 1 / (2 * dt)
    fs = np.arange(min_f, max_f, step)
    return fs


def get_w(N_FREQ):
    return np.random.randn(N_PSR, N_FREQ) + 1j * np.random.randn(N_PSR, N_FREQ)


## Get pulsar locations
def get_locs():
    # [TODO] Hardcoded path!
    locs_df = pd.read_csv(
        "/home/catlettv/novus/sandbox/repos/pta_replicator_fork/data/locs.csv"
    )
    locs = np.column_stack((locs_df["RA"], locs_df["DEC"]))
    return locs


## Compute ORF


def get_ORF(
    correlated: bool = True,
    clm: list = [np.sqrt(4.0 * np.pi)],
    lmax: int = 0,
):
    """Equation 83 of https://arxiv.org/pdf/1406.4664"""

    if not correlated:
        ORF = np.diag(np.ones(N_PSR) * 2)

    else:
        # Check that we have the correct number of clm's
        if len(clm) != lmax + 1:
            raise ValueError(
                f"Length of clm (currently {len(clm)}) must equal lmax+1 (given lmax: {lmax})"
            )
        # Get pulsar locations
        psrlocs = get_locs()
        # Correlated basis
        basis = np.array(correlated_basis(psrlocs, lmax))
        # Get ORF
        ORF = 2.0 * sum(clm[kk] * basis[kk] for kk in range(len(basis)))

    return ORF


## Get sqrt(ORF)
def get_H(ORF):
    """Eq. 63 of https://arxiv.org/pdf/1410.8256"""
    return np.linalg.cholesky(ORF)


## Get strain amplitude
def get_strain_amp(fs, dur):
    # [TODO] Add userspec stuff
    # [TODO] Add turnover option
    f1yr = (1 / (1 * u.year).to(u.s)).value
    alpha = -0.5 * (GAMMA_GWB - 3)
    hcf = AMP_GWB * (fs / f1yr) ** (alpha)
    C = 1 / 96 / np.pi**2 * hcf**2 / fs**3 * dur * HOWML
    return C


## Get residuals
def prep_residuals(H, W, C):
    return np.dot(H, W) * C ** (0.5)


def get_residuals(H, W, C, N_FREQ, dt):
    res = prep_residuals(H, W, C)
    # Now fill in bins after Nyquist (for fft data packing) and take inverse FT
    Res_f2 = np.zeros((N_PSR, 2 * N_FREQ - 2), complex)
    # Res_t = np.zeros((N_PSR, 2 * N_FREQ - 2))
    Res_f2[:, 0:N_FREQ] = res[:, 0:N_FREQ]
    Res_f2[:, N_FREQ : (2 * N_FREQ - 2)] = np.conj(res[:, (N_FREQ - 2) : 0 : -1])
    Res_t = np.real(np.fft.ifft(Res_f2) / dt)


if __name__ == "__main__":
    print("Loading pulsars...")
    load_pulsars()
    print("Loaded")
    t0, t1 = get_t_range()
    dur = (t1 - t0).value
    dt = dur / N_PTS
    ts = get_ts(t0, t1)
    fs = get_fs(ts)
    N_FREQ = len(fs)
    W = get_w(N_FREQ)
    ORF = get_ORF()
    H = get_H(ORF)
    C = get_strain_amp(fs, dur)
    get_residuals(H, W, C, N_FREQ, dt)
