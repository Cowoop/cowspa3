#!/bin/bash

download_dir="downloads"
arch=`uname -i`
arch_spec="i386"
if [ "$arch" == "x86_64" ]; then
    arch_spec="amd64"
fi

google_repo="http://wkhtmltopdf.googlecode.com/files/"
tox_src="libwkhtmltox-0.10.0_rc2-"$arch_spec".tar.bz2"
pdf_src="wkhtmltopdf-0.10.0_rc2-static-amd64.tar.bz2"

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
sudo cp -v lib/*.so* /usr/lib64
sudo ldconfig

cd py-wkhtmltox
python setup.py install
if [ ! $? -eq 0 ]; then
    if [ `which python` == "/usr/bin/python" ]; then
        echo "WARNING: Looks like you are not in virtualenv. Forgotten to run . ./bin/activate'"
    fi
fi
