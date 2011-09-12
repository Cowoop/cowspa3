#!/bin/bash -

# Text color variables
txtund=$(tput sgr 0 1)    # Underline
txtbld=$(tput bold)       # Bold
txtred=$(tput setaf 1)    # Red
txtgrn=$(tput setaf 2)    # Green
txtylw=$(tput setaf 3)    # Yellow
txtblu=$(tput setaf 4)    # Blue
txtpur=$(tput setaf 5)    # Purple
txtcyn=$(tput setaf 6)    # Cyan
txtwht=$(tput setaf 7)    # White
txtrst=$(tput sgr0)       # Text reset

# OS Type
OSTYPE=`uname`

# Get Absolute File Path
# if the call came via symlink, then use its target instead:
arg=$0; [[ -L $0 ]] && arg=$(stat -f '%Y' "$0")

# now do exactly as chriswaco + LN2 said (minor syntax tweaks by me):
script=$(2>/dev/null cd "${arg%/*}" >&2; echo "`pwd -P`/${arg##*/}")
path=$(dirname "$script")
#project=$(dirname "$script"../../)
#echo $project
#" Download Files "
#
#curl "http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.10.0_rc2-static-i386.tar.bz2"
#curl "http://wkhtmltopdf.googlecode.com/files/libwkhtmltox-0.10.0_rc2-i386.tar.bz2"


echo ""
echo "Installing PDF render engine"
echo "-----------------------------"

# Static
wkhtmltopdf_installation="bin/wkhtmltopdf"
wkhtmltopdf_filename="wkhtmltopdf-0.10.0_rc2"
libwkhtmltox_installation="include/wkhtmltox"
libwkhtmltox_installation_lib="lib"
libwkhtmltox_filename="libwkhtmltox-0.10.0_rc2"
py_wkhtmltox_filename="py-wkhtmltox"


# Installing Wkhtmltopdf
if [ -f $wkhtmltopdf_installation ]
then 
    echo "wkhtmltopdf:     [${txtgrn}installed${txtrst}]"
else 
    echo "wkhtmltopdf:     [${txtred}installed${txtrst}]"
    echo "   ---------------"
    
    download=$path"/downloads/"$wkhtmltopdf_filename".tar.bz2"
    
    # Download
    if [ -f $download ]
    then
        echo "   [${txtgrn}oke${txtrst}]  : download"
    else
        echo "   downloading"
        curl -# -C - -o $download "http://wkhtmltopdf.googlecode.com/files/"$wkhtmltopdf_filename"-static-i386.tar.bz2"
    fi
    
    # Extracing
    if [ ! -f $download ]
    then
        tar xjf $download -C $path"/downloads/"
        echo "   [${txtgrn}oke${txtrst}]  : extracted "
    fi
    
    # Copying
    cp $path"/downloads/wkhtmltopdf-i386" $wkhtmltopdf_installation
    echo "   [${txtgrn}oke${txtrst}]  : copy files "
    
    # Clean up
    rm $download
    rm $path"/downloads/wkhtmltopdf-i386"
    
fi

# Installing libwkhtmltox
if [ -d $libwkhtmltox_installation ]
then 
    echo "libwkhtmltox:    [${txtgrn}installed${txtrst}]"
else 
    echo "libwkhtmltox:    [${txtred}installed${txtrst}]"
    echo "   ---------------"
    
    # Download
    download=$path"/downloads/"$libwkhtmltox_filename".tar.bz2"
    
    # Download
    if [ -f $download ]
    then
        echo "   [${txtgrn}oke${txtrst}]  : download"
    else
        echo "   downloading"
        curl -# -C - -o $download "http://wkhtmltopdf.googlecode.com/files/"$libwkhtmltox_filename"-i386.tar.bz2"
    fi
    
    # Extracing
    if [ -f $download ]
    then
        mkdir $path"/downloads/"$libwkhtmltox_filename
        tar xjf $download -C $path"/downloads/"$libwkhtmltox_filename
        echo "   [${txtgrn}oke${txtrst}]  : extracted "
    fi
    
    # Copy
    cp -R $path"/downloads/"$libwkhtmltox_filename"/include/wkhtmltox" $libwkhtmltox_installation
    cp -R $path"/downloads/"$libwkhtmltox_filename"/lib/libwkhtmltox.so" $libwkhtmltox_installation_lib
    ln -sf $libwkhtmltox_installation_lib"/libwkhtmltox.so" $libwkhtmltox_installation_lib"/libwkhtmltox.so.0"
    ln -sf $libwkhtmltox_installation_lib"/libwkhtmltox.so" $libwkhtmltox_installation_lib"/libwkhtmltox.so.0.10"

    echo "   [${txtgrn}oke${txtrst}]  : copy files "
    
    # Clean up
    rm $download
    rm -R $path"/downloads/"$libwkhtmltox_filename
fi

# Updating libs for linux
export LD_LIBRARY_PATH=lib:$LD_LIBRARY_PATH

sudo ldconfig

# Installing py-wkhtmltox
# Download
download=$path"/downloads/"$py_wkhtmltox_filename

if [ -d $download ]
then
    #git pull $download --verbose
    echo "py-libwkhtmltox: [${txtgrn}installed${txtrst}]"
else
    echo "py-libwkhtmltox: [${txtred}installed${txtrst}]"
    # git clone https://Merino@github.com/Merino/py-wkhtmltox.git $download --verbose
    git clone git://github.com/Merino/py-wkhtmltox.git $download --verbose
fi

# Install
C_INCLUDE_PATH=`pwd`/include
LD_LIBRARY_PATH=`pwd`/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH
sudo cp lib/*.so /usr/lib
cd downloads/py-wkhtmltox
python setup.py install

# Clean up
#rm -R $download

echo ""
