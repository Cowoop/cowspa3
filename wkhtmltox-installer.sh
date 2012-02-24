#!/bin/bash

download_dir="downloads"
arch=`uname -i`
arch_spec="i386"
if [ "$arch" == "x86_64" ]; then
    arch_spec="amd64"
fi

google_repo="http://wkhtmltopdf.googlecode.com/files/"
tox_src="libwkhtmltox-0.11.0_rc1-"$arch_spec".tar.bz2"
pdf_src="wkhtmltopdf-0.11.0_rc1-static-"$arch_spec".tar.bz2"
lib_name="libwkhtmltox.so"
lib_dst=`pwd`"/lib"

mkdir -p $lib_dst
mkdir -p $download_dir
cd $download_dir

# Download begin
wget -nc $google_repo$tox_src
wget -nc $google_repo$pdf_src
git clone git://github.com/Merino/py-wkhtmltox.git --verbose

tar jxvf $tox_src
tar jxvf $pdf_src

C_INCLUDE_PATH=`pwd`/include
export C_INCLUDE_PATH
# Uncomment lines below for system wide install
#sudo cp -v lib/*.so* /usr/lib64
#sudo ldconfig
# Comment lines below not needed in system wide install
cp -v lib/$lib_name $lib_dst
ln -s $lib_dst/$lib_name $lib_dst/$lib_name.0
export LIBRARY_PATH=$lib_dst

cd py-wkhtmltox
python setup.py install
if [ ! $? -eq 0 ]; then
    if [ `which python` == "/usr/bin/python" ]; then
        echo "WARNING: Looks like you are not in virtualenv. Forgotten to run . ./bin/activate'"
    fi
fi
