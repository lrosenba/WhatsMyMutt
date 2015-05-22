# WhatsMyMutt
## Installation instructions
### For Front End App.
1. Download and install Android SDK from [developer.android.com/sdk](http://developer.android.com/sdk/index.html)
2. Follow installation instructions for installing Android Studio and get the latest Android tools and API.
3. Add the sdk tools to PATH in the ~/.bash_profile file
   example: export PATH=${PATH}:/Development/adt-bundle/sdk/platform-tools:/Development/adt-bundle/sdk/tools
4. Set the ANDROID_HOME environment variable to where the Android sdk is located
   example: export ANDROID_HOME="/Development/android-sdk-macosx"
5. Install Apache Ant.
6. Set ANT_HOME environment variable to where Ant is installed
   example: export ANT_HOME="/Development/apache-ant-1.9.4"
7. Add ANT_HOME to the PATH
   export PATH=$PATH:$ANT_HOME/bin

### For Server (I used [https://github.com/BVLC/caffe/wiki/Ubuntu-14.04-VirtualBox-VM](https://github.com/BVLC/caffe/wiki/Ubuntu-14.04-VirtualBox-VM))
1. Add an Ubuntu 14.04 vagrant box:
   vagrant box add ubuntu-14.04 https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box
2. Run vagrant init
3. Run vagrant up, then run vagrant ssh
4. Install build essentials"
   sudo apt-get install build-essential
5. Install linux headers
   sudo apt-get install linux-headers-`uname -r`
6. Install curl:
   sudo apt-get install curl
7. Install CUDA:
   curl -O "http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run"
8. Make this installer runnable:
   chmod +x cuda_6.5.14_linux_64.run
9. Run CUDA installer:
   sudo ./cuda_6.5.14_linux_64.run --kernel-source-path=/usr/src/linux-headers-`uname -r`/
   *Accept the EULA
   *Do not install graphics driver
   *Install the toolkit(use default path)
   *Install symbolic link
   *Install samples(use default path)
10. Update the library path:
    * echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
    * echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/lib' >> ~/.bashrc
    * source ~/.bashrc
11. Install dependencies:
    * sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libatlas-base-dev git python-dev python-pip libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml
    * sudo easy_install pillow
12. cd ~
13. Install Caffe:
    git clone https://github.com/BVLC/caffe.git
14. cd caffe
15. Install python dependencies (you may need to sudo pip install them one at a time)
    cat python/requirements.txt | xargs -L 1 sudo pip install 
16. Create these symbolic links:
    * sudo ln -s /usr/include/python2.7/ /usr/local/include/python2.7
    * sudo ln -s /usr/local/lib/python2.7/dist-packages/numpy/core/include/numpy/ /usr/local/include/python2.7/numpy
17. Create Makefile.config:
    cp Makefile.config.example Makefile.config
18. Edit Makefile.config:
    * vim Makefile.config
    * Uncomment the line # CPU_ONLY := 1 (In a virtual machine we do not have access to the the GPU)
    * Under PYTHON_INCLUDE, replace /usr/lib/python2.7/dist-packages/numpy/core/include with /usr/local/lib/python2.7/dist-packages/numpy/core/include (i.e. add /local)
19. Compile Caffe:
    * make pycaffe
    * make all
    * make test
20. Download the ImageNet Caffe model and labels:
    * ./scripts/download_model_binary.py models/bvlc_reference_caffenet
    * ./data/ilsvrc12/get_ilsvrc_aux.sh
21. Modify python/classify.py to add the --print_results option
22. You can now test the caffe installation on a give sample:
    * cd ~/caffe
    * python python/classify.py --print_results examples/images/cat.jpg foo
    * Expected result: [('tabby', '0.27933'), ('tiger cat', '0.21915'), ('Egyptian cat', '0.16064'), ('lynx', '0.12844'), ('kit fox', '0.05155')]
23. exit vagrant box by running the command exit
24. edit vagrantfile ex: vim vagrantfile
25. uncomment this line: config.vm.network "public_network"
26. Now run vagrant ssh to go back into the vagrant box
27. cd caffe
28. You can now run the server with this command:
    python examples/web_demo/app.py

## How To Run
Right now this app uses a server on my computer so it cannot be run far away from my laptop

1. cd into the app
2. Move the response.html, responseDog.html, app.py and the dogimgs150.csv files into the virtual box (move them into the same file as the vagrantfile)
3. vagrant ssh into the vagrant box that has the server
4. The files that were just moved are now in the /vagrant folder
5. move response.html and responseDogs.html into the caffe/examples/web_demo/templates folder
6. replace the existing app.py file in the caffe/examples/web_demo folder with the app.py in the /vagrant folder
7. move the dogimgs150.csv file from the /vagrant folder to the caffe/examples/web_demo folder
8. Open new terminal and cd into frontend Android app
9. Install these necessary plugins:
   * cordova plugin install com.ionic.keyboard 1.0.4 "Keyboard" <br />
                        - org.apache.cordova.camera 0.3.6 "Camera" <br />
                        - org.apache.cordova.console 0.2.13 "Console" <br />
                        - org.apache.cordova.device 0.3.0 "Device" <br />
                        - org.apache.cordova.file 1.3.3 "File" <br />
                        - org.apache.cordova.file-transfer 0.5.0 "File Transfer" <br />
10. Run ionic build android
11. Send to Android phone by bluetooth or other means
12. make sure server is running on nearby computer
13. Click on the app on the Android phone
14. Have Fun!
