import subprocess
import time
import pathlib
import os

ANDROID_SDK_PATH = os.getenv("ANDROID_SDK_PATH")
ANDROID_BUILD_TOOL_PATH = ANDROID_SDK_PATH + "/build-tools/33.0.1"
ANDROID_PLATFORM_PATH = ANDROID_SDK_PATH + "/platforms/android-33"

def do_command(c):
    start_time = time.time()
    subprocess.check_output(c)
    end_time = time.time()
    print(f"Command {c} took {end_time - start_time} secs")

if not pathlib.Path("build").exists():
    pathlib.Path("build").mkdir()

if not pathlib.Path("build/java").exists():
    pathlib.Path("build/java").mkdir()

# generate resource file R.java
do_command([
    ANDROID_BUILD_TOOL_PATH + "/aapt",
    "package", "-f", "-m",
    "-S", "resources",
    "-J", "build/java",
    "-M", "src/AndroidManifest.xml",
    "-I", ANDROID_PLATFORM_PATH + "/android.jar",
])

# compile java classes
do_command([
    "javac",
    "--release", "8",
    "-d", "build/obj",
    "-classpath", ANDROID_PLATFORM_PATH + "/android.jar",
    "src/java/com/rivten/rawandroid/StartActivity.java",
    "build/java/com/rivten/rawandroid/R.java",
])

# dexing java bytecode
do_command([
    ANDROID_BUILD_TOOL_PATH + "/d8",
    "--output", "build/",
    "--classpath", ANDROID_PLATFORM_PATH + "/android.jar",
    "build/obj/com/rivten/rawandroid/R$attr.class",
    "build/obj/com/rivten/rawandroid/R$string.class",
    "build/obj/com/rivten/rawandroid/R.class",
    "build/obj/com/rivten/rawandroid/StartActivity.class",
])

if pathlib.Path("build/rawandroid.unsigned.apk").exists():
    pathlib.Path("build/rawandroid.unsigned.apk").unlink()

# generating apk
do_command([
    ANDROID_BUILD_TOOL_PATH + "/aapt",
    "package", "-f",
    "-M", "src/AndroidManifest.xml",
    "-S", "resources",
    "-I", ANDROID_PLATFORM_PATH + "/android.jar",
    "-F", "build/rawandroid.unsigned.apk",
    "build"
])

if pathlib.Path("build/rawandroid.apk").exists():
    pathlib.Path("build/rawandroid.apk").unlink()

# align the apk
do_command([
    ANDROID_BUILD_TOOL_PATH + "/zipalign",
    "-v", "4",
    "build/rawandroid.unsigned.apk",
    "build/rawandroid.apk",
])

if not pathlib.Path("build/key.keystore").exists():
    do_command([
        "keytool", "-genkeypair",
        "-validity", "1000",
        "-dname", "CN=rivten,O=Android,C=ES",
        "-keystore", "build/key.keystore",
        "-storepass", "password",
        "-keypass", "password",
        "-alias", "rawandroidKey",
        "-keyalg", "RSA",
    ])

# sign the apk
do_command([
    ANDROID_BUILD_TOOL_PATH + "/apksigner",
    "sign",
    "--key-pass", "pass:password",
    "--ks-pass", "pass:password",
    "--ks", "build/key.keystore",
    "build/rawandroid.apk"
])
