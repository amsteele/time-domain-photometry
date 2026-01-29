import argparse
from pathlib import Path
import config_photometry as cfg
from utils import extract_filenum, in_any_range
from phot_core import compute_times_and_ratios, compute_medians, compute_relative_flux
from phot_plotting import plot_lightcurve,save_fits

def get_target_config(name):
    for t in getattr(cfg, "targets", []):
        if t.get("name") == name:
            return t
    return {
        "name": getattr(cfg, "target_name", name),
        "ra_deg": getattr(cfg, "target_ra"),
        "dec_deg": getattr(cfg, "target_dec"),
        "ref_stars": getattr(cfg, "ref_stars"),
        "file_ranges": getattr(cfg, "file_ranges"),
        "file_dir": getattr(cfg, "file_dir")}

def select_files(aligned_dir, file_ranges):
    files = sorted(Path(aligned_dir).glob("*.fits"))
    if not file_ranges:
        return files
    out = []
    for p in files:
        n = extract_filenum(p)
        if n is not None and in_any_range(n, file_ranges):
            out.append(p)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--aligned_dir", default=cfg.ALIGNED_DIR)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    #target = get_target_config(args.target or cfg.target_name)
    target = get_target_config(cfg.targets[0]["name"])
    files = select_files(args.aligned_dir, target.get("file_ranges"))
    print(f"Using {len(files)} files for target {target['name']}")
    print("First/last file:", files[0].name, files[-1].name)
    from io_fits import read_image_and_header
    from wcs_tools import skycoord_to_pixel
    
    # Use the FIRST aligned frame as the reference
    _, ref_hdr = read_image_and_header(files[0])
    
    positions = [
    skycoord_to_pixel(ref_hdr, target["ra_deg"], target["dec_deg"])
    ]
    for _, ra, dec in target["ref_stars"]:
        positions.append(skycoord_to_pixel(ref_hdr, ra, dec))
    print('positions: ',positions)
    times, ratios = compute_times_and_ratios(
        files,
        positions,
        aper_r=getattr(cfg, "aper_radius", getattr(cfg, "APER_R", 10.0)),
        ann_r_in=getattr(cfg, "annulus_rin", getattr(cfg, "ANN_RIN", 20.0)),
        ann_r_out=getattr(cfg, "annulus_rout", getattr(cfg, "ANN_ROUT", 25.0)),
        date_keys=getattr(cfg, "DATE_KEYS", ("DATE-OBS", "DATE")),
    )
    medians = compute_medians(ratios, getattr(cfg, "USER_MEDIANS", None))
    rel = compute_relative_flux(ratios, medians)

    print("Medians used:")
    #print('Number of points: ',len(rel))
    for (name, _, _), m in zip(target["ref_stars"], medians):
        print(f"  {name}: {m:.6g}")

    out_png = args.out or getattr(cfg, "OUT_PNG", f"lightcurve_{target['name']}.png")
    plot_lightcurve(times, rel, target["name"], out_png)
    
    fname = getattr(cfg,'file_dir')
    out_fits = args.out or getattr(cfg, "OUT_FITS", f"lightcurve_data_{fname}.fits")
    save_fits(out_fits, times, rel)

if __name__ == "__main__":
    main()

