from pathlib import Path
import numpy as np
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from astropy.stats import SigmaClip
from photutils.background import Background2D, MedianBackground
from io_fits import read_image_and_header, header_date_to_num
from wcs_tools import skycoord_to_pixel

def measure_aperture_fluxes(path: Path, positions, aper_r, ann_r_in,ann_r_out,date_keys, crop=None):
    data, hdr = read_image_and_header(path)
    #bkg_est = MedianBackground()
    #sigma_clip=SigmaClip(sigma=3.0)
    #back = Background2D(data0,(20,20), filter_size=(3,3),sigma_clip=sigma_clip,bkg_estimator=bkg_est)
    #print(back.background_median,back.background_rms_median)
    #data = data - back.background_rms_median
    if crop is not None:
        y0, y1, x0, x1 = crop
        data = data[y0:y1, x0:x1]

    tnum = header_date_to_num(hdr, keys=date_keys)
    ap = CircularAperture(positions, r=aper_r)
    ann = CircularAnnulus(positions, r_in=ann_r_in, r_out=ann_r_out)
    
    phot = aperture_photometry(data, [ap, ann])
    sums = np.asarray(phot["aperture_sum_0"], dtype=float)   # RAW
    sky_mean = np.asarray(phot["aperture_sum_1"], dtype=float) / ann.area
    sky_in_ap = sky_mean * ap.area_overlap(data)
    sky_sub = sums - sky_in_ap
    return tnum, sky_sub[0], sky_sub[1:]

def compute_times_and_ratios(
    files,
    positions,
    *,
    aper_r,
    ann_r_in,
    ann_r_out,
    date_keys,
    crop=None,
):
    times, ratios = [], []
    HOT_CUT = 9e5 

    for p in files:
        try:
            tnum, target_flux, ref_fluxes = measure_aperture_fluxes(
                p, positions, aper_r,ann_r_in,ann_r_out, date_keys, crop
            )
            if target_flux <= 0 or np.any(ref_fluxes <= 0):
                print("NEG FRAME", p.name, "targ", target_flux, "refs min", ref_fluxes.min())
            else:
                times.append(tnum)
                ratios.append(target_flux/ref_fluxes)
        except Exception:
            print('Issue measuring aperture fluxes')
            continue
        if target_flux > HOT_CUT: 
           continue
    if len(times) < 5:
        raise RuntimeError("Too few usable frames after filtering")

    times = np.asarray(times)
    ratios = np.asarray(ratios)
    order = np.argsort(times)
    return times[order], ratios[order]

def compute_medians(ratios, user_medians=None):
    if user_medians is not None:
        user_medians = np.asarray(user_medians, dtype=float)
        if user_medians.shape[0] != ratios.shape[1]:
            raise ValueError("USER_MEDIANS length must match number of reference stars")
        return user_medians
    return np.nanmedian(ratios, axis=0)

def compute_relative_flux(ratios, medians):
    return np.nanmean(ratios / medians[None, :], axis=1)
