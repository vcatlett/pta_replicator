import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import pint.toa as toa
from pint.residuals import Residuals
from pint.models import get_model, get_model_and_toas
from pint.simulation import zero_residuals
import pint.logging
pint.logging.setup(level="WARNING")

load_dotenv()

PSR_NAME = "J1312+0051"

DATA_15YR_ROOT = Path(os.getenv("DATA_15YR_ROOT"))
# DATA_15YR_RES = DATA_15YR_ROOT / "residuals"
DATA_15YR_PAR = DATA_15YR_ROOT / "narrowband/par"
DATA_15YR_TIM = DATA_15YR_ROOT / "narrowband/tim"

# all_residuals = [ar for ar in DATA_15YR_RES.glob("*full.res")]
all_pars = [ap for ap in DATA_15YR_PAR.glob(f"{PSR_NAME}*.par")]
all_tims = [at for at in DATA_15YR_TIM.glob(f"{PSR_NAME}*.tim")]

# test_res = all_residuals[0]
# column_labels = ["MJD", "frequency_MHz", "residual_us", "uncertainty_us", "chi2", "flag"]
# test_df = pd.read_csv(test_res, sep='\s+', skiprows=3, header=None, names=column_labels)
# print(test_df.info())

# ## FIGURE
# fig, ax = plt.subplots(1)

# # OG residuals
# cax = ax
# cax.errorbar(
#     test_df["MJD"], test_df["residual_us"], 
#     yerr=test_df["uncertainty_us"],
#     color="k",
#     fmt='.', 
#     linestyle='none',
#     )
# cax.set_xlabel("MJD")
# cax.set_ylabel(r"Residual ($\mu s$)")

# plt.savefig("testfig.png")

## ZERO RESIDUALS
test_tim = all_tims[0]
test_par = all_pars[0]
m, t_all = get_model_and_toas(test_par, test_tim)
xt = t_all.get_mjds()
rs_og = Residuals(t_all, m).phase_resids

## Zero Residuals
zero_residuals(t_all, m)
t_all.print_summary()
rs_new = Residuals(t_all, m).phase_resids

## PLOT
fig, ax = plt.subplots(ncols=2, sharey=True, gridspec_kw={'wspace': 0})

# Original
cax = ax[0]
cax.scatter(xt, rs_og, color="k", marker=".")
cax.set_xlabel("MJD")
cax.set_ylabel("Residual (Phase)")
cax.set_title("Original Residuals")

# Zeroed
cax = ax[1]
cax.scatter(xt, rs_new, color="k", marker=".")
cax.set_xlabel("MJD")
cax.set_title("Residuals After Zeroing")

# Save figure
plt.suptitle(f"{PSR_NAME} Residuals")
# plt.savefig(f"{PSR_NAME}_zero_res.png")
plt.show()