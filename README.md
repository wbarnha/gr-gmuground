# gr-gmuground

# Installation
The following dependencies must be installed:

- [GNU Radio](https://github.com/gnuradio/gnuradio) (>=3.7.11)
- [gr-satellites](https://github.com/daniestevez/gr-satellites) (maint-3.7)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler) (maint-3.7)
- [gr-limesdr](https://github.com/myriadrf/gr-limesdr/) (Optional, but our system is intended to interface with LimeSDR)
- [libfec](https://github.com/quiet/libfec)
- [construct](https://construct.readthedocs.io/en/latest/) (>=2.9)
- [swig](http://www.swig.org/)
- [requests](https://pypi.org/project/requests/)

For CW decoding, the following must be installed:

- [gr-satnogs](https://gitlab.com/librespacefoundation/satnogs/gr-satnogs/-/tree/v1.5.1) (1.5.1)
and related dependencies.

Once all dependencies are installed, run the commands:

```
git clone https://github.com/wbarnha/gr-gmuground.git
cd gr-gmuground
git checkout maint-3.7
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

# Operation
TBD

More information can be found in the Wiki.
