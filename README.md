Cluster Sorter
==============
The [Timepix detector](http://medipix.web.cern.ch)
([Llopart et al. 2007](http://dx.doi.org/10.1016/j.nima.2007.08.079))
is capable of
measuring and visualising ionising radiation in a 256-by-256 grid
of **pixels**, representing the 14mm-by14-mm silicon wafer of its
sensor element.
This repository contains code for analysing, visualising and
sorting clusters of "hit" pixels by their **cluster properties**.
Further information can be found in
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193))


## Disclaimers
* _This code dates from 2015. While every attempt has been
made to ensure that it is usable, some work may be required to get it
running on your own particular system.
We recommend using a GridPP CernVM; please refer to
[this guide](http://doi.org/10.6084/m9.figshare.4552825.v1)
for further instructions.
Unfortunately CERN@school cannot guarantee further support for this code.
Please proceed at your own risk_.
* _This repository is now deprecated, and remains here for legacy purposes.
For future work regarding CERN@school, please refer to the
[Institute for Research in Schools](http://researchinschools.org) (IRIS)
[GitHub repository](https://github.com/InstituteForResearchInSchools).
Please also feel free to fork and modify this code as required for
your own research._


## Getting and running the code
To get the code, create a working directory on your CernVM and
clone it from GitHub with the following command:

```bash
$ git clone https://github.com/CERNatschool/cluster-sorter.git
```

To prepare for running, run the `setup.sh` script with the following
command:

```bash
$ source setup.sh
```

_Note: if you are not using a GridPP CernVM, the `setup.sh` script
will not work as you won't have access to the CERN@school CVMFS
repository and will have to source your own version of the Python
libraries such as `matplotlib` via e.g. the
[Anaconda Python distribution](http://anaconda.org)._


### Process the test data
To get you started, we've supplied some data to process with the
cluster finding code. 
The processing script, `process-frames.py`, runs over the data in the
`inputPath` directory and writes the results to the `outputPath` 
directory. You need to create the latter directory. Let's do this now:

```bash
$ cd cluster-sorter
$ mkdir tmp
```

You can then run the processing script with:

```bash
$ python process-frames.py testdata/crookes/ tmp/
```

After a while (depending on the speed of your computer),
you should see the following output from the terminal:

```bash
*
*======================================*
* CERN@school - local frame processing *
*======================================*
*
* Input path          : 'testdata/crookes/'
* Output path         : 'tmp/'
* Gamma candidate clusters WILL NOT be processed.
*
```

The directory `tmp` should now be full of results, which you can check with
the following command:

```bash
$ ls tmp/
clusters  frames  frames.json  klusters.json
```

The code has extracted the properties of the data frames and clusters
into the `frames.json` and `klusters.json` JSON files
(more on [JSON files here](http://www.w3schools.com/json/)) - so we
don't have to run the processing code again - and created image files
of all the frames and the clusters. so you can view them with
any standard image viewer.
On the GridPP CernVM, for example, you can use the Eye of Gnome viewer:

```bash
$ sudo yum install eog
[... say 'yes' to everything and type your password when asked ...]
$ eog tmp/frames/ &
$ eog tmp/clusters/ &
```

You can then view each image by pressing the left or right arrow keys.


### Make some plots
We can also visualise the different properties of the frames and
clusters by making **plots** of the different numbers we've
used our code to extract.
Again, we've done this for you to start with - try:

```bash
$ python make-plots.py tmp/ tmp/
*
*==============================*
* CERN@school - make the plots *
*==============================*
*
* Input path          : 'tmp/'
* Output path         : 'tmp/'
*
*
* Plotting complete.
* View your results by opening:
* 'tmp/frameplots/index.html' or 'tmp/clusterplots/index.html'
* in a browser, e.g.
* $ firefox tmp/frameplots/index.html &
* $ firefox tmp/clusterplots/index.html &
```

Follow those instructions and you should be able to see the two webpages - one
for the frames, one for the clusters - displaying the different plots 
for the Crookes dataset.

Now that we've plotted the frame and cluster properties,
let's try _sorting_ the clusters into different particle types.


### Sorting the test data's clusters

The `sort-clusters.py` Python script sorts the clusters that you've just
extracted from the test data. You can run it with the following command:

```bash
$ python sort-clusters.py tmp/ types.json tmp/
```

...and you should get the following output:

```bash
===============================
  CERN@school - Sort Clusters  
===============================
*
* Input path          : 'tmp/'
* Particle JSON       : 'types.json'
* Output file         : 'tmp/'
*
*
* Sorted 149 clusters!
*
* Sorting complete.
* View your results by opening 'tmp/sorted/index.html' in a browser, e.g.
* firefox tmp/sorted/index.html &
```

The webpage that appears in the Firefox browser should present you 
with a list of clickable particle types, each representing a particle 
type that the code has sorted the clusters into. 
Try clicking on each and looking at the different types. 
Can you spot the patterns? Once you start to look "under the hood" 
of the code, you'll see how the different types are decided upon.

Good luck!


## The data
The data in the `testdata` folder is taken from the
[Crookes dataset](http://doi.org/10.6084/m9.figshare.734262.v1),
a sample set of measurements made at the Royal Institution of
Great Britain during the BIG SCIENCE event of 18th June 2013.
The data were obtained by placing a CERN@school MX-10
detector next to the notebook of William Crookes,
the discoverer of Thallium.  You can find an image of the experimental setup
[here](https://dx.doi.org/10.6084/m9.figshare.4588300.v1).


## Acknowledgements
CERN@school was supported by
the UK [Science and Technology Facilities Council](http://www.stfc.ac.uk) (STFC)
via grant numbers ST/J000256/1 and ST/N00101X/1,
as well as a Special Award from the Royal Commission for the Exhibition of 1851.


## Useful links
* [Setting up a GridPP CernVM](http://doi.org/10.6084/m9.figshare.4552825.v1);
* [Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193) - the CERN@school _Contemporary Physics_ paper featuring a discussion of cluster properties and their use in particle identification;
* The [Crookes dataset on FigShare](http://doi.org/10.6084/m9.figshare.734262.v1);
* The [Institute for Research in Schools](http://researchinschools.org) (IRIS) homepage;
* The [IRIS CERN@school website](http://researchinschools.org/CERN);
* The [Official IRIS GitHub Organization](https://github.com/InstituteForResearchInSchools).
