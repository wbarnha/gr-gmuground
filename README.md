# gr-gmuground
<p align="center">
  <img src=https://user-images.githubusercontent.com/25623043/75652038-193b8600-5c28-11ea-8f26-32cc496427ec.jpg>
</p>
Art produced and reused with permission from Jae Wook Choi.

# Installation
The following dependencies must be installed:

- [GNU Radio](https://github.com/gnuradio/gnuradio) (>=3.8.0)
- [gr-limesdr](https://github.com/myriadrf/gr-limesdr) (gr-3.8)
- [gr-satellites](https://github.com/daniestevez/gr-satellites) (next)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler) (maint-3.8)
- [gr-filerepeater](https://github.com/ghostop14/gr-filerepeater)
- [gr-fosphor](https://github.com/osmocom/gr-fosphor) (beta)
- [gr-display](https://github.com/wbarnha/gr-display)
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
(Note: The guide for installing gr-fosphor [here](https://osmocom.org/projects/sdr/wiki/fosphor) indicates you must install the OpenCL libraries for Intel, AMD, or Nvidia. You must install the OpenCL library for your computer!)

It is recommended to setup OpenCL for Intel CPUs by installing the SDK [here](https://software.seek.intel.com/intel-opencl?os=linux).

# Operation

![](https://user-images.githubusercontent.com/25623043/75466860-d3956980-5958-11ea-8152-1d64cde69500.png)
To change the center frequency in real time, either double-click on the screen or enter the frequency in the upper-left corner. The center frequency is automatically shifted to process USB signals and decode these signals.

More information can be found in the Wiki.
