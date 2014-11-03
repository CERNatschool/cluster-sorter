#!/usr/bin/env python

"""

 CERN@school - Sorting Clusters

 See the README.md and GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, inspect, glob, argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree, copyfile

# Import the JSON library.
import json

# Import the plotting libraries.
import pylab as plt

#from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

# Get the path of the current directory
#path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#
# The main program.
#
if __name__=="__main__":

    print("===============================")
    print("  CERN@school - Sort Clusters  ")
    print("===============================")

    # Get the datafile path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",  help="Path to the input dataset.")
    parser.add_argument("typePath",   help="Path to the particle type JSON.")
    parser.add_argument("outputPath", help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    ## The path to the particle type JSON.
    typepath = args.typePath

    ## The output path.
    outputpath = args.outputPath

    # Set the logging level to DEBUG.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename='log_sort-clusters.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Particle JSON       : '%s'" % (typepath))
    print("* Output file         : '%s'" % (outputpath))
    print("*")

    ## The cluster properties JSON file - FIXME: check it exists...
    kf = open(datapath + "/klusters.json", "r")
    #
    kd = json.load(kf)
    kf.close()

    ## The cluster types specification JSON file - FIXME: check it exists...
    tf = open(typepath, "r")
    #
    types = json.load(tf)
    tf.close()


    # Create the sorting directories.

    ## The path to the sorted cluster directory.
    sortedpath = "%s/sorted" % (outputpath)
    #
    if os.path.isdir(sortedpath):
        rmtree(sortedpath)
        lg.info(" * Removing directory '%s'..." % (sortedpath))
    os.mkdir(sortedpath)
    lg.info(" * Creating directory '%s'..." % (sortedpath))

    ## Dictionary of the clusters { id:type }.
    ks = {}

    ## Dictionary of the cluster sizes { id:size }.
    ksizes = {}

    ## Dictionary of the cluster radii { id:radius }.
    krads = {}

    ## Dictionary of the cluster densities { id:density }.
    kdens = {}

    ## Dictionary of the cluster linearity { id:linearity }.
    klins = {}

    ## List of the cluster types.
    alltypes = ["None", "Edge"]

    # Add the types from the input types JSON file.
    for t in types:
        for typename, vals in t.iteritems():
            alltypes.append(typename)

    # Loop over the klusters.
    for k in kd:

        ksizes[k["id"]] = k["size"]
        krads[k["id"]]  = k["radius_uw"]
        kdens[k["id"]]  = k["density_uw"]
        klins[k["id"]]  = k["lin_linearity"]

        lg.info(" *")
        lg.info(" * Cluster ID: '%s'." % (k["id"]))
        lg.info(" *")
        lg.info(" *--> Size          : % 5d    [pixels]" % (k["size"]))
        lg.info(" *--> Radius        : %8.2f [pixels]" % (k["radius_uw"]))
        lg.info(" *--> Density       : %8.2f [pixels^-1]" % (k["density_uw"]))
        lg.info(" *--> Linearity     : %8.2f" % (k["lin_linearity"]))
        lg.info(" *")

        # Check if the cluster is on the edge of the frame.
        if k["xmin"] <= 0.1 or k["xmax"] >= 254.9 or k["ymin"] <= 0.1 or k["ymax"] >= 254.9:
            ks[k["id"]] = "Edge"
            continue

        # Loop over the types and check for a match.
        for t in types:
            for typename, vals in t.iteritems():

                size_min = vals["size_min"]
                size_max = vals["size_max"]

                rad_min = vals["rad_min"]
                rad_max = vals["rad_max"]

                rho_min = vals["rho_min"]
                rho_max = vals["rho_max"]

                lin_min = vals["lin_min"]
                lin_max = vals["lin_max"]

                #
                # If it isn't, check if it matches the current type.
                if (k["size"] >= size_min) and (k["size"] <= size_max) and \
                   (k["radius_uw"] >= rad_min) and (k["radius_uw"] <= rad_max) and \
                   (k["lin_linearity"] >= lin_min) and (k["lin_linearity"] <= lin_max) and \
                   (k["density_uw"] >= rho_min) and (k["density_uw"] <= rho_max):
                    lg.info(" *==> Cluster ID '%s' is of type: '%s'." % (k["id"], typename))
                    lg.info(" *")

                    if k["id"] in ks.keys():
                        raise Exception("* ERROR! Cluster already sorted - your types.json contains overlapping definitions.")

                    # Assign the cluster to the current type.
                    ks[k["id"]] = typename

    # Find un-identified, non-edge klusters.
    for k in kd:
        if k["id"] not in ks.keys():
            ks[k["id"]] = "None"


    lg.info(" *")
    lg.info(" * SUMMARY:")
    lg.info(" *")
    for cid, ctype in ks.iteritems():
        lg.info(" * %s is '%s'." % (str(cid), str(ctype)))
    print("*")
    print("* Sorted %d clusters!" % (len(ks)))

    ## Path to the sorting HTML page.
    homepagename = sortedpath + "/index.html"

    ## The index page for the sorted clusters.
    pg = ""

    pg += "<!DOCTYPE html>\n"
    pg += "<html>\n"
    pg += "  <head>\n"
    pg += "    <link rel=\"stylesheet\" type=\"text/css\" "
    pg += "href=\"assets/css/style.css\">\n"
    pg += "  </head>\n"
    pg += "  <body>\n"
    pg += "    <h1>CERN@school: Cluster Sorting</h1>\n"
    pg += "    <h2>Dataset summary</h2>\n"
    pg += "    <p>\n"
    pg += "      <ul>\n"
    pg += "        <li>Dataset path = '%s'</li>\n" % (datapath)
    pg += "        <li>Number of clusters = %d</li>\n" % (len(kd))
    pg += "      </ul>\n"
    pg += "    </p>\n"
    pg += "    <h2>Cluster types</h2>\n"

    pg += "    <p>\n"
    pg += "      <ul>\n"

    # Loop over the cluster types.
    for typename in sorted(alltypes):

        ## The cluster type page name.
        kpgname = "%s/%s.html" % (sortedpath, typename)

        pg += "        <li><a href=\"%s.html\">%s</a></li>\n" % (typename, typename)

        kpg = ""
        kpg += "<!DOCTYPE html>\n"
        kpg += "<html>\n"
        kpg += "  <head>\n"
        kpg += "    <link rel=\"stylesheet\" type=\"text/css\" "
        kpg += "href=\"assets/css/style.css\">\n"
        kpg += "  </head>\n"
        kpg += "  <body>\n"
        kpg += "    <h1>CERN@school: '%s' Clusters</h1>\n" % (typename)
        kpg += "    <p>Back to the <a href=\"index.html\">cluster types</a> page.</p>\n"
        kpg += "    <table>\n"
        for kl, ktype in ks.iteritems():
            if ktype == typename:
                kpg += "      <tr>\n"
                kpg += "      <td><img src=\"../clusters/%s.png\" style=\"width:256px\"/></td>\n" % (kl)
                kpg += "      <td>ID:<br />Size:<br />Radius:<br />Density:<br />Linearity:<br /></td>\n"
                kpg += "      <td>%s<br />%d<br />%8.2f<br />%8.2f<br />%8.2f<br /></td>\n" % (kl,ksizes[kl],krads[kl],kdens[kl],klins[kl])
                kpg += "      </tr>\n"
        kpg += "    </table>\n"

        kpg += "      </ul>\n"
        kpg += "    </p>\n"
        kpg += "  </body>\n"
        kpg += "</html>"

        kf = open(kpgname, "w")
        kf.write(kpg)
        kf.close()

    pg += "  </body>\n"
    pg += "</html>"


    ## The text file for the HTML page.
    f = open(homepagename, "w")
    f.write(pg)
    f.close()

    # Now you can view "index.html" to see your results!
    print("*")
    print("* Sorting complete.")
    print("* View your results by opening '%s' in a browser, e.g." % (homepagename))
    print("* firefox %s &" % (homepagename))
