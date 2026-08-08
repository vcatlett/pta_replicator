import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA_15YR_ROOT = Path(os.getenv("DATA_15YR_ROOT"))
# DATA_15YR_RES = DATA_15YR_ROOT / "residuals"
DATA_15YR_PAR = DATA_15YR_ROOT / "narrowband/par"
DATA_15YR_TIM = DATA_15YR_ROOT / "narrowband/tim"

print(DATA_15YR_PAR)


def get_locs():
    # [TODO] Use Astropy for this
    locs = pd.read_csv(
        "/home/catlettv/novus/sandbox/repos/pta_replicator_fork/data/locs.csv"
    )
    epochs = []
    ras = []
    decs = []
    for pi, p in enumerate(locs["name"]):
        if p.startswith("B"):
            epoch = "1950"
        else:
            epoch = "2000"
        epochs.append(epoch)
        coords = ephem.Equatorial(
            ephem.Ecliptic(str(locs["ELONG"][pi]), str(locs["ELAT"][pi])), epoch=epoch
        )
        ra = float(repr(coords.ra))
        dec = np.pi / 2.0 - float(repr(coords.dec))
        ras.append(ra)
        decs.append(dec)
    # locs["epoch"] = epochs
    locs["RA"] = ras
    locs["DEC"] = decs
    locs.to_csv(
        "/home/catlettv/novus/sandbox/repos/pta_replicator_fork/data/locs_new.csv",
        index=False,
    )


get_locs()
