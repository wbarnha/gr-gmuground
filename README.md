# gr-gmuground

# Installation
The following dependencies must be installed:

- GNU Radio (>=3.7.11)
- [gr-satellites](https://github.com/daniestevez/gr-satellites) (maint-3.7)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler)
- [gr-limesdr](https://github.com/myriadrf/gr-limesdr/) (Optional, but our system is intended to interface with LimeSDR)
- [libfec](https://github.com/quiet/libfec)
- [construct](https://construct.readthedocs.io/en/latest/) (>=2.9)
- [swig](http://www.swig.org/)
- [requests](https://pypi.org/project/requests/)

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
