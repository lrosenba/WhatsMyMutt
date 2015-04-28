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
1. cd into the app
2. Run ionic build android
