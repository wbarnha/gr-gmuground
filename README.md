# gr-gmuground
<p align="center">
  <img src=https://user-images.githubusercontent.com/25623043/75652038-193b8600-5c28-11ea-8f26-32cc496427ec.jpg>
</p>
Art produced and reused with permission from Jae Wook Choi.

Winner of the Outstanding ECE Senior Design Project Award for Spring 2020.

# Installation
If you don't already have GNU Radio, you can quickly install it using [this](https://github.com/wbarnha/grsetup) Shell script. For all scripts, it is assumed that Ubuntu 18.04 or later is being used (note that as of this commit, gr-limesdr isn't currently compatible with versions later than 18.04).

The following dependencies must be installed:

- [GNU Radio](https://github.com/gnuradio/gnuradio) (>=3.8.0)
- [gr-limesdr](https://github.com/myriadrf/gr-limesdr) (gr-3.8) 
- [gr-satellites](https://github.com/daniestevez/gr-satellites) (next)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler) (maint-3.8)
- [gr-filerepeater](https://github.com/ghostop14/gr-filerepeater)
- [gr-fosphor](https://github.com/osmocom/gr-fosphor) (beta)
- [gr-display](https://github.com/wbarnha/gr-display)
- [gr-guiextra](https://github.com/wbarnha/gr-guiextra)
- [libfec](https://github.com/quiet/libfec)
- [construct](https://construct.readthedocs.io/en/latest/) 
- [swig](http://www.swig.org/)
- [requests](https://pypi.org/project/requests/)

For CW decoding, the following must be installed:

- [gr-satnogs](https://gitlab.com/librespacefoundation/satnogs/gr-satnogs) (2.0+)
and related dependencies.

Once all dependencies are installed, run the commands:

```
git clone https://github.com/wbarnha/gr-gmuground.git
cd gr-gmuground
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

Alternatively, you can run the `setup.sh` Bash script to install the dependencies and gr-gmuground.

```
git clone https://github.com/wbarnha/gr-gmuground.git
cd gr-gmuground
./setup.sh
```
(Note: The guide for installing gr-fosphor [here](https://osmocom.org/projects/sdr/wiki/fosphor) indicates you must install the OpenCL libraries for Intel, AMD, or Nvidia. You must install the OpenCL library for your computer!)
It is recommended to setup OpenCL for Intel CPUs by installing the SDK [here](https://software.seek.intel.com/intel-opencl?os=linux). Once this is complete, running `setup.sh` will take care of everything for you.`

If you don't have a LimeSDR, feel free to install `cubicsdr` (It automatically installs most of the Soapy packages and it's useful to make sure everything is working fine), `python3-soapysdr`, and `soapysdr-tools` to expand your options to the RTL SDR, HackRF, etc., with [gr-soapy](https://gitlab.com/librespacefoundation/gr-soapy/).

# Operation

![](https://user-images.githubusercontent.com/25623043/77204143-7e1c2a80-6ac8-11ea-9cb5-ba63a1067d41.png)
To change the center frequency in real time, either double-click on the screen or enter the frequency in the upper-left corner. The center frequency is automatically shifted to process USB signals and decode these signals.

More information can be found in the Wiki.
