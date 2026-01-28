"""
User configuration for the photometry pipeline.
Edit this file before running the scripts.
Coordinates:
- Provide target + reference star coordinates in ICRS (J2000) degrees.
- Images MUST have a valid WCS in their FITS headers for RA/Dec -> pixel conversion. If you don't have WCS, solve astrometry first, e.g. astrometry.net.
"""
from pathlib import Path

# -------- Paths --------
main_dir = Path("20190225/")
file_dir = "20190225"  # for naming purposes

# Calibration frames (search patterns relative to main_dir = main directory)
bias_files  = "bias/*.bias*.fits"
dark_files = "dark/*dark*.fits"
flat_files = "flat/*flat*.fits"

# Science frames, calibration files should be moved to a newly created subdirectrory
sci_files = '*.fits'

# Working/output directories
cal_directory = Path("cal_phot")

MASTER_DIR = cal_directory / "masters"
CALIB_DIR = cal_directory / "calibrated"
ALIGNED_DIR = cal_directory / "aligned"
#ALIGNED_DIR = "20170421/pipelineout" #cal_directory / "aligned"
RESULTS_DIR = Path("results")

# -------- FITS header keys --------
EXPTIME_KEY = "EXPTIME"
DATE_KEYS = ("DATE","DATE-OBS")  # used for time axis

# -------- Photometry configuration --------
# good site to use: https://aladin.cds.unistra.fr/AladinLite/

target_name = "WD1145"
target_ra = 177.1401238290  # degrees
target_dec = 1.4831723463   #degrees

# 3+ reference stars for ensemble relative photometry
# Each: ("name", ra_deg, dec_deg)
ref_stars = [
            ("ref1", 177.1687809877, +1.4985451062),
            ("ref2",177.14105186066,1.51928839952),   
            ("ref3", 177.1049520744, +1.5095992521),  
]

# Subset of objects: 
file_ranges = [(1,310)]


# All objects
targets = [
    {
        "name": "WD1145",
        "ra_deg": 177.1401238290,
        "dec_deg": +1.4831723463,
        "ref_stars": [
            ("ref4", 177.1687809877, +1.4985451062), 
            ("ref3",177.14105186066,1.51928839952),
            ("ref1", 177.1049520744, +1.5095992521),
        ],
        #"file_ranges": [(36,435)],
        #"file_ranges": [(36,265)],
        #"file_ranges": [(41,240)],
        #"file_ranges": [(37,437)],
        #"file_ranges": [(85,427)],
        #"file_ranges": [(41,364)],
        "file_ranges": [(1,310)],
    }
]
'''
    {
        "name": "TargetB",
        "ra_deg": 250.0,
        "dec_deg": 36.0,
        "ref_stars": [
            ("ref1", 250.1, 36.02),
            ("ref2", 249.9, 35.98),
        ],
        "file_ranges": [(436,586)],
    },
]
'''

# Aperture/annulus radii (pixels)
aper_radius = 6.0
annulus_rin = 15.0
annulus_rout = 18.0

# Optional centroid refinement around the expected pixel location
centroid_refinement = True
centroid_box = 3  # should be an odd number

# Reject frames where any required star has sky-sub flux < MIN_FLUX
min_flux = 0.0

# Plot smoothing (median filter kernel; odd). Set 0/1 to disable.
smooth_kernel = 3 

# Alignment settings (translation-only phase correlation)
align_interp_order = 3  # spline order for shifting (0=nearest, 1=linear, 3=cubic)

# Optional cropping applied consistently to all images 
# Set to None to disable, else (y0, y1, x0, x1)
#crop = (0,1000,50,1050) 
crop = None 
