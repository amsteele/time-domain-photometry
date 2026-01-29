from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from astropy.io import fits
import numpy as np

def plot_lightcurve(times, rel, title, out_png):
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot_date(times, rel, "o", ms=3)
    ax.set_xlabel("UT")
    ax.set_ylabel("Relative flux")
    ax.set_title(title)
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H:%M"))
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.show()


def save_fits(
    out_path: Path,
    times_mpl: np.ndarray,
    rel: np.ndarray,
    #target_flux: np.ndarray,
    #refs_flux: np.ndarray,
    #pcfg: PhotConfig,
    #rel_smooth: Optional[np.ndarray] = None,
) -> None:
    """Write a binary table FITS with the plotted data."""

    cols = [ 
        fits.Column(name="TIME_MPL", format="D", array=np.asarray(times_mpl, dtype=float)),
        fits.Column(name="REL_FLUX", format="D", array=np.asarray(rel, dtype=float)),
        #fits.Column(name="TARGET_FLUX", format="D", array=np.asarray(target_flux, dtype=float)),
    ]   
    #if rel_smooth is not None:
    #    cols.append(fits.Column(name="REL_FLUX_SMOOTH", format="D", array=np.asarray(rel_smooth, dtype=float)))

    #for i in range(refs_flux.shape[1]):
    #    cols.append(fits.Column(name=f"REF{i+1}_FLUX", format="D", array=np.asarray(refs_flux[:, i], dtype=float)))

    tbhdu = fits.BinTableHDU.from_columns(cols)

    hdul = fits.HDUList([fits.PrimaryHDU(), tbhdu])
    hdul.writeto(out_path, overwrite=True)
    print(f"Wrote FITS table: {out_path}  (table is in extension 1)")
