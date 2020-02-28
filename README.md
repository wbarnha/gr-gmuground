# gr-gmuground

# Installation
The following dependencies must be installed:

- [GNU Radio](https://github.com/gnuradio/gnuradio) (>=3.8.0)
- [gr-satellites](https://github.com/daniestevez/gr-satellites) (next)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler) (maint-3.8)
- [gr-fosphor](https://github.com/osmocom/gr-fosphor) (beta)
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

# Operation
TBD

More information can be found in the Wiki.
