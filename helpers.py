#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Various helper functions for processing CERN@school Timepix datasets.
"""

def getKlusterPropertiesJson(klusterid, k):
    """ Return a JSON containing the cluster properties. """

    # Get the line of best fit values for the cluster.
    m, c, sumR = k.getLineOfBestFitValues()

    p = {\
        "id"            : klusterid,                  \
        "size"          : k.getNumberOfPixels(),      \
        "xmin"          : k.getXMin(),                \
        "xmax"          : k.getXMax(),                \
        "ymin"          : k.getYMin(),                \
        "ymax"          : k.getYMax(),                \
        "width"         : k.getWidth(),               \
        "height"        : k.getHeight(),              \
        "x_uw"          : k.getXUW(),                 \
        "y_uw"          : k.getYUW(),                 \
        "radius_uw"     : k.getRadiusUW(),            \
        "density_uw"    : k.getDensityUW(),           \
        "totalcounts"   : k.getTotalCounts(),         \
        "maxcounts"     : k.getMaxCountValue(),       \
        "lin_m"         : m,                          \
        "lin_c"         : c,                          \
        "lin_sumofres"  : sumR,                       \
        "lin_linearity" : k.getLinearity(),           \
        "n_edgepixels"  : k.getNumberOfEdgePixels(),  \
        "edgefrac"      : k.getOuterPixelFraction(),  \
        "innerfrac"     : k.getInnerPixelFraction(),  \
        "ismc"          : k.isMC(),                   \
        "isedgekluster" : k.isEdgeCluster()           \
        #"totalenergy"   :, \
        #"maxenergy"     :, \
        #"frameid"       :\
        }

    return p
