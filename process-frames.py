#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Processing Frames

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for processing the datasets.
from cernatschool.dataset import Dataset

#...for the histograms.
from plotting import Hist, Hist2D

#...for making the frame image.
from visualisation import makeFrameImage, makeKlusterImage

#...for getting the cluster properties JSON.
from helpers import getKlusterPropertiesJson


if __name__ == "__main__":

    print("*")
    print("*======================================*")
    print("* CERN@school - local frame processing *")
    print("*======================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    ## The output path.
    outputpath = args.outputPath

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_process-frames.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")


    # Set up the directories
    #------------------------

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Create the subdirectories.

    ## The path to the frame images.
    frpath = outputpath + "/frames/"
    #
    if os.path.isdir(frpath):
        rmtree(frpath)
        lg.info(" * Removing directory '%s'..." % (frpath))
    os.mkdir(frpath)
    lg.info(" * Creating directory '%s'..." % (frpath))
    lg.info("")

    ## The path to the frame plots.
    fppath = outputpath + "/frameplots/"
    #
    if os.path.isdir(fppath):
        rmtree(fppath)
        lg.info(" * Removing directory '%s'..." % (fppath))
    os.mkdir(fppath)
    lg.info(" * Creating directory '%s'..." % (fppath))
    lg.info("")

    ## The path to the cluster images.
    klpath = outputpath + "/clusters/"
    #
    if os.path.isdir(klpath):
        rmtree(klpath)
        lg.info(" * Removing directory '%s'..." % (klpath))
    os.mkdir(klpath)
    lg.info(" * Creating directory '%s'..." % (klpath))
    lg.info("")

    ## The path to the cluster plots.
    kppath = outputpath + "/clusterplots/"
    #
    if os.path.isdir(kppath):
        rmtree(kppath)
        lg.info(" * Removing directory '%s'..." % (kppath))
    os.mkdir(kppath)
    lg.info(" * Creating directory '%s'..." % (kppath))
    lg.info("")

    ## The dataset to process.
    ds = Dataset(datapath)

    ## Latitude of the test dataset [deg.].
    lat = 51.509915

    ## Longitude of the test dataset [deg.].
    lon = -0.142515 # [deg.]

    ## Altitude of the test dataset [m].
    alt = 34.02

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt))

    lg.info("* Found %d datafiles:" % (len(frames)))

    ## A list of frames.
    mds = []

    ## The number of clusters per frame.
    ncs = []

    ## The number of non-gamma clusters per frame.
    nlcs = []

    ## The number of gamma candidates per frame.
    ngs = []

    # Clusters
    #----------

    ## A list of clusters.
    klusters = []

    # Create container lists for the cluster properties.
    cluster_size      = []
    cluster_counts    = []
    cluster_radius_u  = []
    cluster_density_u = []
    cluster_linearity = []

    # Loop over the frames and upload them to the DFC.
    for f in frames:

        ## The basename for the data frame, based on frame information.
        bn = "%s_%d-%06d" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create the frame image.
        makeFrameImage(bn, f.getPixelMap(), frpath)

        # Get the frame's cluster properties.
        ncs.append( f.getNumberOfKlusters())
        nlcs.append(f.getNumberOfNonGammas())
        ngs.append( f.getNumberOfGammas())

        # Create the metadata dictionary for the frame.
        metadata = {
            "id"          : bn,
            #
            "chipid"      : f.getChipId(),
            "hv"          : f.getBiasVoltage(),
            "ikrum"       : f.getIKrum(),
            #
            "lat"         : f.getLatitude(),
            "lon"         : f.getLongitude(),
            "alt"         : f.getAltitude(),
            #
            "start_time"  : f.getStartTimeSec(),
            "end_time"    : f.getEndTimeSec(),
            "acqtime"     : f.getAcqTime(),
            #
            "n_pixel"     : f.getNumberOfUnmaskedPixels(),
            "occ"         : f.getOccupancy(),
            "occ_pc"      : f.getOccupancyPc(),
            #
            "n_kluster"   : f.getNumberOfKlusters(),
            "n_gamma"     : f.getNumberOfGammas(),
            "n_non_gamma" : f.getNumberOfNonGammas(),
            #
            "ismc"        : int(f.isMC())
            }

        # Add the frame metadata to the list of frames.
        mds.append(metadata)

        # The cluster analysis
        #----------------------

        # Loop over the clusters.
        for i, kl in enumerate(f.getKlusterFinder().getListOfKlusters()):

            ## The kluster ID.
            klusterid = bn + "_k%05d" % (i)

            # Get the cluster properties.
            cluster_size.append(     kl.getNumberOfPixels() )
            cluster_counts.append(   kl.getTotalCounts()    )
            cluster_radius_u.append( kl.getRadiusUW()       )
            cluster_density_u.append(kl.getDensityUW()      )
            cluster_linearity.append(kl.getLinearity()      )

            # Get the cluster properties JSON entry and add it to the list.
            klusters.append(getKlusterPropertiesJson(klusterid, kl))

            # Make the cluster image.
            makeKlusterImage(klusterid, kl, klpath)

        #break # TMP - uncomment to only process the first frame.

    # Write out the frame information to a JSON file.
    with open(outputpath + "/frames.json", "w") as jf:
        json.dump(mds, jf)

    # Write out the cluster information to a JSON file.
    with open(outputpath + "/klusters.json", "w") as jf:
        json.dump(klusters, jf)

    ## The number of clusters plot.
    nlcsplot = Hist("nlc", 101, ncs, -1, "Number of clusters", "Number of frames", fppath)

    ## The number of non-gamma clusters plot.
    ncsplot = Hist("ncs", 102, nlcs, -1, "Number of non-gamma clusters", "Number of frames", fppath)

    ## The number of gamma clusters plot.
    ngsplot = Hist("ngs", 103, ngs, -1, "Number of gamma clusters", "Number of frames", fppath)

    # Cluster plots
    #---------------

    ksplot = Hist("kls", 1001, cluster_size,       -1, "$N_{h}$",   "Number of clusters", kppath)
    kcplot = Hist("klc", 1002, cluster_counts,    100, "$N_{C}$",   "Number of clusters", kppath)
    krplot = Hist("klr", 1003, cluster_radius_u,  100, "$r$",       "Number of clusters", kppath)
    kdplot = Hist("kld", 1004, cluster_density_u, 100, "$\\rho$",   "Number of clusters", kppath)
    klplot = Hist("kll", 1005, cluster_linearity, 100, "Linearity", "Number of clusters", kppath)

    # Figure - hits vs radius.
    hits_vs_rad = Hist2D(201, "hvr", cluster_size,     "$N_h$", max(cluster_size), \
                                     cluster_radius_u, "$r$",   100,               \
                                     kppath)

    # Figure - hits vs counts.
    hits_vs_counts = Hist2D(202, "hvc", cluster_size,   "$N_h$", max(cluster_size), \
                                        cluster_counts, "$N_c$", 100,               \
                                        kppath)

    # Figure - hits vs linearity.
    hits_vs_lin = Hist2D(203, "hvl", cluster_size,      "$N_h$", max(cluster_size), \
                                     cluster_linearity, "Linearity", 100,           \
                                     kppath)
    # Figure - radius vs linearity.
    rad_vs_lin = Hist2D(204, "rvl", cluster_radius_u, "$r$", 100,        \
                                    cluster_linearity, "Linearity", 100, \
                                    kppath)

    # Figure - density vs linearity.
    rho_vs_lin = Hist2D(205, "dvl", cluster_density_u, "$\\rho$", 100,   \
                                    cluster_linearity, "Linearity", 100, \
                                    kppath)

    # ToDo - add an index.html to display the frame and cluster
    # property histograms.
