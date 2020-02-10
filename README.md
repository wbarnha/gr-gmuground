# gr-gmuground

# Installation
The following dependencies must be installed:

- [GNU Radio](https://github.com/gnuradio/gnuradio) (>=3.8.0)
- [gr-satellites](https://github.com/wbarnha/gr-satellites) (maint-3.8)
- [gr-gpredict-doppler](https://github.com/ghostop14/gr-gpredict-doppler) (maint-3.8)
- [libfec](https://github.com/quiet/libfec)
- [construct](https://construct.readthedocs.io/en/latest/) 
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

# Operation
TBD

More information can be found in the Wiki.
