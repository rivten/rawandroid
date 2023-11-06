# Rawandroid

Ever wanted to build an andoid app without Android Studio ? Now you do.

## Why ?

- it's fun
- android studio eats a lot of my ram
- you want to organize your folder the way _you_ want, not the way gradle wants
- you just want to understand what an apk is actually made of
- in the end, it's not that much more line of code

## How to build ?

Just get the folder and run:

```
ANDROID_SDK_PATH=path-to-sdk python build.py
```

Now you have the APK.
You can install it on an emulated device with…

```
adb -e install build/rawandroid.apk
```

## Dependencies

- python
- javac
- android sdkmanager to get most build tools

## What's next ?

- native code with SDK
- a more fleshed out example (with UI and stuff)
- assets, more resources
- more aggressive zipping
- command to automatically install, like gradle does
- dynamic detection of android version targetting
- more fun !
