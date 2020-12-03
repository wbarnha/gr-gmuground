#!/bin/bash
#For setting up dependencies to use gr-gmuground

sudo apt install -y \
      libboost-dev \
      libboost-date-time-dev \
      libboost-filesystem-dev \
      libboost-program-options-dev \
      libboost-system-dev \
      libboost-thread-dev \
      libboost-regex-dev \
      libboost-test-dev \
      libboost-all-dev \
      swig \
      cmake \
      build-essential \
      pkg-config \
      libconfig++-dev \
      libgmp-dev \
      liborc-0.4-0 \
      liborc-0.4-dev \
      liborc-0.4-dev-bin \
      libjsoncpp-dev \
      libpng++-dev \
      libvorbis-dev \
      git \
      ocl-icd-opencl-dev \
      opencl-clhpp-headers \
      opencl-headers \
      libogg-dev \
      libvorbis-dev \
      xorg-dev \
      libglu1-mesa-dev \
      libsoapysdr-dev \
      libi2c-dev \
      libusb-1.0-0-dev \
      g++ \
      libsqlite3-dev \
      libwxgtk3.0-dev \
      freeglut3-dev \
      python3-pip \
      nlohmann-json-dev

if cat /proc/cpuinfo | grep 'vendor' | grep -q 'GenuineIntel'; then
   echo "Intel Processor Detected"
   sudo add-apt-repository ppa:intel-opencl/intel-opencl
   sudo apt-get update
   sudo apt-get install intel-opencl-icd
fi

pip3 install requests construct matplotlib

cd ~/
git clone https://github.com/quiet/libfec
cd libfec
./configure
make
sudo make install
sudo ldconfig
cd

#sudo add-apt-repository -y ppa:myriadrf/drivers
#sudo apt-get update
#sudo apt-get install limesuite liblimesuite-dev limesuite-udev limesuite-images
#sudo apt-get install soapysdr-tools soapysdr-module-lms7

#soapysdr-tools use to be called just soapysdr on older packages
#sudo apt-get install soapysdr soapysdr-module-lms7

git clone https://github.com/myriadrf/LimeSuite.git
cd LimeSuite
git checkout stable
mkdir builddir && cd builddir
cmake ../
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd ~/LimeSuite/udev-rules
sudo ./install.sh
cd

#rm -rf gr-limesdr
git clone https://github.com/myriadrf/gr-limesdr
cd gr-limesdr
git checkout gr-3.8
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

#rm -rf gr-satnogs
git clone https://gitlab.com/librespacefoundation/satnogs/gr-satnogs.git
cd gr-satnogs
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

#rm -rf gr-satellites
#Remove --recursive to not download satellite-recordings
git clone https://github.com/daniestevez/gr-satellites
cd gr-satellites
git checkout next
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd 
rm -rf gr-satellites
git clone --recursive https://github.com/wbarnha/gr-satellites
git checkout maint-3.8
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd ..
./compile.sh
cd

#rm -rf gr-gpredict-doppler
git clone https://github.com/ghostop14/gr-gpredict-doppler
cd gr-gpredict-doppler
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

#rm -rf gr-display
git clone https://github.com/wbarnha/gr-display
cd gr-display
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd ..
for file in examples/*.grc
do grcc $file
done
cd

git clone https://github.com/glfw/glfw
cd glfw
mkdir build
cd build
cmake ../ -DBUILD_SHARED_LIBS=true
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

#rm -rf gr-fosphor
git clone git://git.osmocom.org/gr-fosphor
cd gr-fosphor
git checkout -b test 6f3a8de592e181e9ac2e76800e50df427827ba5b
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd
cd gr-fosphor/lib/fosphor
make LDFLAGS=-L/opt/intel/opencl-1.2-4.5.0.8/lib64
cd

#rm -rf gr-filerepeater
git clone https://github.com/ghostop14/gr-filerepeater
cd gr-filerepeater
git checkout maint-3.8
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

#rm -rf gr-guiextra
git clone https://github.com/wbarnha/gr-guiextra
cd gr-guiextra
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd

cd ~/gr-gmuground
mkdir build
cd build
cmake ../
make -j $(nproc --all)
sudo make install
sudo ldconfig
cd ..
for file in apps/*.grc
do grcc $file
done
cd
