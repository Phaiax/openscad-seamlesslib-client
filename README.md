openscad-seamlesslib-client
===========================

Python programm which pre-compiles .scad files, so that they can use modules online seamless



==How to make the windows package==

* You need to have a windows machine (virtual is ok)
* Download and install python 2.7.5 (http://python.org/download/). Choose 'Windows Installer' for 32 bit systems and 'Windows X86-64 Installer' for 64 bit systems.
* Download and unzip Pyinstaller 2.0 (http://www.pyinstaller.org/).
* Download and unzip git, eg: http://msysgit.github.io/
* Download and install wxPython (http://wxpython.org/download.php) Unicode version, FOR PYTHON 2.7 !! (make shure that you install python first)
* Download ez_setup.py from https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py (or copy'n'paste it)
* Download and install pywin32: (http://sourceforge.net/projects/pywin32/)
 * Pay attention to not click any of the fake download buttons in the advertisements.
 * Instead click on the small 'Browse All Files' link
 * Click on the pywin32 folder
 * Select the latest build folder (Build 218 currently)
 * Download the correct file: win32 or amd64 for 32 or 64 bit systems, and the file for python 2.7
 * Install it

* We now need to install easy_install and then some python libraries.
 * Open a command line: Win + R, type 'cmd' and hit enter. Enter the following commands
  * set PATH=%PATH%;C:\Python27;C:\Python27\Scripts
 * If you have saved ez_setup.py to your Desktop, then enter these commands
  * cd Desktop
  * python ez_setup.py
 * Now we can install some required libraries, enter these commands:
  * easy_install mock
  * easy_install watchdog
  * easy_install simplejson

* Start Git Bash
* Execute the following commands (and modify them if you know what to do)
 * cd Desktop
 * git clone https://github.org/Phaiax/openscad-seamlesslib-client.git
* Open a command line: Win + R, type 'cmd' and hit enter. Enter the following commands
 * set PATH=%PATH%;C:\Python27;C:\Python27\Scripts
* now we can run tests
 * cd Desktop/openscad-seamlesslib-client
 * cd src
 * python runtests.py
* look at the test results. All tests should run fine.
* We do now create a distributable package.
 * go to the openscad-seamlesslib-client folder:
  * cd ..
 * start package generation:
  * python C:\Users\<<<your user folder>>>\Desktop\pyinstaller-2.0\pyinstaller-2.0\pyinstaller.py --buildpath=dist src\seamless_compiler.py
 * if all is done correctly, you now have a distributable folder: openscad-seamlesslib-client\dist\seamless_compiler
 * This folder contains a stand-alone executable: No need to install python or anything we have done above. Just this folder is enought.
 * The folder contains an executable named seamless_compiler.exe. Currently it's only a commandline application. You need to start it via commandline with the folder you want to watch as parameter.
