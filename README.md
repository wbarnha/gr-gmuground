# gr-gmuground
<p align="center">
  <img src=https://user-images.githubusercontent.com/25623043/75652038-193b8600-5c28-11ea-8f26-32cc496427ec.jpg>
</p>
Art produced and reused with permission from Jae Wook Choi.

Winner of the Outstanding ECE Senior Design Project Award for Spring 2020.

The original project is committed to the [maint-3.8 branch](https://github.com/wbarnha/gr-gmuground/tree/maint-3.8) to see the full scope of the project. Future implementations of gr-gmuground are intended to be much cleaner with less linked dependencies to other GR OOT modules. `maint-3.9` is skipped due to lack of demand.

# Installation

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

If you don't have a LimeSDR, feel free to install `cubicsdr` (It automatically installs most of the Soapy packages and it's useful to make sure everything is working fine), `python3-soapysdr`, and `soapysdr-tools` to expand your options to the RTL SDR, HackRF, etc., with [gr-soapy](https://gitlab.com/librespacefoundation/gr-soapy/).

# Operation

The main feature of this library at the moment focuses on combining signals from separate Yagi antennae. TBD.

More information can be found in the Wiki.
There's a lot of missing documentation here, since I've unfortunately had to move on to other projects. If you want a long 112 page document containing everything, feel free to send me an email.
