# WhatsMyMutt
# Installation instructions
1. Download and install Android SDK from [developer.android.com/sdk](developer.android.com/sdk)
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

# How To Run
Right now this app uses a server on my computer so it cannot be run far away from my laptop

1. cd into the app
2. Install these necessary plugins:
   * cordova plugin install com.ionic.keyboard 1.0.4 "Keyboard"
            *             org.apache.cordova.camera 0.3.6 "Camera"
            *             org.apache.cordova.console 0.2.13 "Console"
            *             org.apache.cordova.device 0.3.0 "Device"
            *             org.apache.cordova.file 1.3.3 "File"
            *             org.apache.cordova.file-transfer 0.5.0 "File Transfer"
3. Run ionic build android
4. Send to Android phone by bluetooth or other means
5. Click on app
