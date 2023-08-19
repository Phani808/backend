import yaml
import subprocess
import os, re
import wget, fileinput
from os.path import exists
import xml.etree.ElementTree as ET

working_dir = os.getcwd()

# Download Files

def downloadFile(downloadPath, destPath, fileName):
    file_exists = exists(destPath+fileName)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    if file_exists:
        os.remove(destPath+fileName)
        wget.download(downloadPath, destPath+fileName)
    else:
        wget.download(downloadPath, destPath+fileName)

# Update Google Key

def updateAPIKey(workingPath, workingFileName, elementToModify, keyValue):
    # Parse the XML file
    tree = ET.parse(working_dir+workingPath+workingFileName)

    # Get the root element of the XML tree
    root = tree.getroot()
    element_to_modify = root.find(elementToModify)

    element_to_modify.text = keyValue

    tree.write(working_dir+workingPath+workingFileName)

# Update Colors

def updateColors(workingPath, workingFileName, color, lightColor, darkColor):
    # Parse the XML file
    tree = ET.parse(working_dir+workingPath+workingFileName)
    root = tree.getroot()
    primaryColorElement = root.find("color[@name='colorPrimary']")
    primaryColorDarkElement = root.find("color[@name='colorPrimaryDark']")
    primaryColorLightElement = root.find("color[@name='colorPrimaryLight']")

    primaryColorElement.text = color
    primaryColorDarkElement.text = darkColor
    primaryColorLightElement.text = lightColor

    tree.write(working_dir+workingPath+workingFileName)

# Update App Name

def UpdateAppName(workingPath, workingFileName, keyValue):
    # Parse the XML file
    tree = ET.parse(working_dir+workingPath+workingFileName)

    # Get the root element of the XML tree
    root = tree.getroot()
    element_to_modify = root.find("string[@name='app_name']")

    element_to_modify.text = keyValue

    tree.write(working_dir+workingPath+workingFileName)

# Register XML Namespaces

def register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])

# Update Manifest File

def UpdateManifestFile(workingPath, workingFileName, keyValue):

    # Load the manifest file
    register_all_namespaces(working_dir+workingPath+workingFileName)
    tree = ET.parse(working_dir+workingPath+workingFileName)
    root = tree.getroot()

    # Find the element you want to update
    package_element = root.find('.')

    # Update the package name attribute
    package_element.set('package', keyValue)

    # Write the updated manifest file
    tree.write(working_dir+workingPath+workingFileName)

# Update Scan Library Manifest File

def UpdateScanManifestFile(workingPath, workingFileName, keyValue):

    register_all_namespaces(working_dir+workingPath+workingFileName)

    # Define the namespace
    #namespace = {'android': 'http://schemas.android.com/apk/res/android'}

    # Load the manifest file
    tree = ET.parse(working_dir+workingPath+workingFileName)
    root = tree.getroot()
    pack = keyValue+".fileprovider"

    # Find the element you want to update and update
    outerElement = root.find("application")
    innerElement = outerElement.find("provider")

    # Remove the existing android:authorities attribute
    #innerElement.attrib.pop('{android}authorities')

    innerElement.set('android:authorities', pack)

    # Write the updated manifest file
    tree.write(working_dir+workingPath+workingFileName)

# Change Package Name

def changePackageName(project_dir, old_package_name, new_package_name):
    # Traverse the directory structure of the project
    for dirpath, dirnames, filenames in os.walk(project_dir):
        for filename in filenames:
            # Check if the file is a Java file
            if filename.endswith(".java") or filename.endswith('.xml'):
                # Modify the contents of the file
                filepath = os.path.join(dirpath, filename)
                with fileinput.FileInput(filepath, inplace=True, encoding="utf-8") as file:
                    for line in file:
                        print(line.replace(old_package_name, new_package_name), end='')


#Main Module

def apkGenerator(yaml_path, aId):
    # Define the path of the yaml file

    yaml_file_path = f"{working_dir}/{yaml_path}"

    # Load the contents of the YAML file
    with open(yaml_file_path, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # Extract the package name, APK name and other information  from the YAML data
    package_name = yaml_data["PackageName"]
    app_name = yaml_data["AppName"]
    version_no = yaml_data["VersionCode"]
    version_name = yaml_data["VersionName"]
    debug_mode = yaml_data["DebugMode"]
    app_type = yaml_data["AppType"]
    app_id = yaml_data["APPID"]

    service_url = yaml_data["ServiceURL"]
    user_login_type = yaml_data["UserLoginType"]

    try:
        user_login_Details_Authentication_type = yaml_data["UserLoginDetails"]["BhargoAuthenticationType"]
    except KeyError:
        user_login_Details_Authentication_type = ""

    try:
        user_login_details_userid = yaml_data["UserLoginDetails"]["UserIDs"]
    except KeyError:
        user_login_details_userid = ""

    try:
        user_login_details_userType = yaml_data["UserLoginDetails"]["UserTypes"]
    except KeyError:
        user_login_details_userType = ""

    try:
        user_login_details_userPosts = yaml_data["UserLoginDetails"]["UserPosts"]
    except KeyError:
        user_login_details_userPosts = ""

    try:
        post_login_page = yaml_data["PostLoginPage"]
    except KeyError:
        post_login_page = ""

    try:
        apiDetails = yaml_data["UserLoginDetails"]["APIBasicDetails"]
    except KeyError:
        apiDetails = ""

    try:
        captchaRequired = yaml_data["UserLoginDetails"]["IsCaptchaRequired"]
    except KeyError:
        captchaRequired = ""

    try:
        openURLOptions = yaml_data["OptionalLinks"]
    except KeyError:
        openURLOptions = ""

    # Extract Image Path to replace from the YAML Data
    app_icon = yaml_data["AppIconImage"]
    # logo_img = yaml_data["AppIconImage"]
    # title_img = yaml_data["TitleImage"]

    # Extract color code to replace from the YAML Data
    primary_color = yaml_data["PrimaryColorCode"]
    primary_light = yaml_data["LightPrimaryColorCode"]
    primary_dark = yaml_data["DarkPrimaryColorCode"]

    # Extract API to replace from the YAML Data
    google_api = yaml_data["GoogleAPIKey"]
    google_service_json = yaml_data["GoogleServicesJSONFile"]

    # Extract Default Home Page Options from the YAML Data
    try:
        default_page_options = yaml_data["DefaultHomePageOptions"]
    except KeyError:
        default_page_options = ""

    try:
        socialMediaOptions = yaml_data["SocialMediaOptions"]["SocialMediaItems"]
    except KeyError:
        socialMediaOptions = ""

    # Git Details of the Master User
    repo_name = "user4.0newdesign"
    repo_url = "bitbucket.org/bhargoplatform-android/user4.0newdesign.git"
    repo_user = "x-token-auth"
    repo_password = "ATCTT3xFfGN0DZdD_hdMKl9PKF0n5117Ql3PWl923yUuzY48rYBd7YkpGATj9eTyQCUaS4ZNMg2ca0jVvLErJ5fjAuL2BUe57GBo04WpZ-bSw-UrirRb1bFKHWIL5Y8PLdLUcG4T8xQVt_X5pmlC81XJAlxNp29eVgf5AJ0w0Z5mVv2diP-_Mpg=CF119162"

    # Construct the Git clone command with authentication credentials
    clone_command = f"git clone -b UserApp1.0 https://{repo_user}:{repo_password}@{repo_url}"

    # Directories Initialization
    app_path = f"/{repo_name}/app/"
    file_path = f"{repo_name}/app/src/main/java/com/bhargo/user/utils/"
    drawable_path = f"/{repo_name}/app/src/main/res/drawable/"
    manifest_path = f"/{repo_name}/app/src/main/"
    manifest_scanlib_path = f"/{repo_name}/scanlibrary/src/main/"
    colors_path = f"/{repo_name}/app/src/main/res/values/"
    api_path = f"/{repo_name}/app/src/main/res/values/"
    string_path = f"/{repo_name}/app/src/main/res/values/"
    apk_path = f"{repo_name}/app/build/outputs/apk/debug"

    output_path = f"{aId}/apk/"

    # Define the file names
    file_name = "CustomAPK.java"
    class_name = "CustomAPK"
    manifest_file = "AndroidManifest.xml"
    colors_file = "colors.xml"
    api_file = "google_maps_api.xml"
    app_icon_image = "icon_bhargo_user.png"
    app_icon_image_rounded = "icon_bhargo_user_rounded.png"
    string_file = "strings.xml"
    gradle_file = "build.gradle"

    # Clone the repository using Git with authentication credentials
    subprocess.call(clone_command.split())

    # -----------------------------
    # Modify App Constants Java File
    # ------------------------------

    # JAVA Statements

    java_app_id = f'public static String appId = "{app_id}";'
    java_app_type = f'public static String appType = "{app_type}";'
    java_service_url = f'public static String serviceURL = "{service_url}";'
    java_userLogin_type = f'public static String userLoginType = "{user_login_type}";'
    java_userAuthenticationType = f'public static String userAuthenticationType = "{user_login_Details_Authentication_type}";'
    java_userId = f'public static String userID = "{user_login_details_userid}";'
    java_userType = f'public static String userType = "{user_login_details_userType}";'
    java_userPosts = f'public static String userPosts = "{user_login_details_userPosts}";'
    java_defaultPageOptions = f'public static String defaultPageOptions = "{default_page_options}";'
    java_socialMediaOptions = f'public static String socialMediaOptions = "{socialMediaOptions}";'
    java_postLoginPage = f'public static String postLoginPage = "{post_login_page}";'
    java_apiDetails = f'public static String apiDetails = "{apiDetails}";'
    java_captchaRequired = f'public static String captchaRequired = "{captchaRequired}";'
    java_openURLOptions = f'public static String openURLOptions = "{openURLOptions}";'


    customAPKContent = """
    package com.bhargo.user.utils;

    public class  CustomAPK{
    """


    # Open the file for reading
    with open(os.path.join(working_dir, file_path, file_name), "w") as file:
        file.write(customAPKContent)
        file.write("\n")
        file.write(java_app_id)
        file.write("\n")
        file.write(java_app_type)
        file.write("\n")
        file.write(java_service_url)
        file.write("\n")
        file.write(java_userLogin_type)
        file.write("\n")
        file.write(java_userAuthenticationType)
        file.write("\n")
        file.write(java_userId)
        file.write("\n")
        file.write(java_userType)
        file.write("\n")
        file.write(java_userPosts)
        file.write("\n")
        file.write(java_defaultPageOptions)
        file.write("\n")
        file.write(java_socialMediaOptions)
        file.write("\n")
        file.write(java_postLoginPage)
        file.write("\n")
        file.write(java_apiDetails)
        file.write("\n")
        file.write(java_captchaRequired)
        file.write("\n")
        file.write(java_openURLOptions)
        file.write("\n")
        file.write("}")


    # Download the Firebase JSON File, App Logo, Logo file and title Image

    downloadFile(google_service_json, working_dir+app_path, "google-services.json")
    downloadFile(app_icon, working_dir+drawable_path, app_icon_image)
    downloadFile(app_icon, working_dir+drawable_path, app_icon_image_rounded)

    # Update Google API Key

    updateAPIKey(api_path, api_file, "string", google_api)

    # Update Main Colors

    updateColors(colors_path, colors_file, primary_color, primary_light, primary_dark)

    # Update App Name

    UpdateAppName(string_path, string_file, app_name)

    # Update Manifest File

    UpdateManifestFile(manifest_path, manifest_file, package_name)

    # Update Provider element in Manifest File

    #UpdateScanManifestFile(manifest_path, manifest_file, package_name)

    #UpdateScanManifestFile(manifest_scanlib_path, manifest_file, package_name)

    # Update Gradle File

    # Open the Gradle build file in read mode
    with open(working_dir + app_path + gradle_file, 'r') as f:
        # Read the file contents
        file_contents = f.read()

    # Use regex to find and update the version code
    new_file_contents = re.sub(
        r'versionCode\s+\d+', f'versionCode {version_no}', file_contents)

    # Use regex to find and update the version name
    new_file_contents = re.sub(r'versionName\s+".*?"',
                               f'versionName "{version_name}"', new_file_contents)

    # Use regex to find and update the application name
    new_file_contents = re.sub(r'applicationId\s+".*?"',
                               f'applicationId "{package_name}"', new_file_contents)


    # Open the Gradle build file in write mode and write the updated contents
    with open(working_dir + app_path + gradle_file, 'w') as f:
        f.write(new_file_contents)

    # Change Package Name in Andriod Project

    if(package_name != "com.bhargo.user"):
        changePackageName(working_dir+"/"+repo_name, "com.bhargo.user", package_name)

    # Make a directory with new Package Name

    packageArray =  package_name.split(".")
    newPath = ""

    for p in packageArray:
        newPath += p + "/"


    # Create File Structure by new Path and Remove the old File Structure

    if(package_name != "com.bhargo.user"):
        print("Not a default Package" + "\n")

        subprocess.call(f"mkdir {newPath}", cwd=f"{working_dir}/{repo_name}/app/src/androidTest/java", shell=True)

        subprocess.call(f"cp -r {working_dir}/{repo_name}/app/src/androidTest/java/com/bhargo/user//* {working_dir}/{repo_name}/app/src/androidTest/java/{newPath}/* /s /e /i /Y", cwd=f"{working_dir}/{repo_name}/app/src/androidTest/java/com/bhargo/user", shell=True)

        subprocess.call(f"rm -r {working_dir}/{repo_name}/app/src/androidTest/java/com/bhargo/user", shell=True)

        subprocess.call(f"mkdir {newPath}", cwd=f"{working_dir}/{repo_name}/app/src/main/java", shell=True)

        subprocess.call(f"cp -r {working_dir}/{repo_name}/app/src/main/java/com/bhargo/user/* {working_dir}/{repo_name}/app/src/main/java/{newPath}/* /s /e /i /Y", cwd=f"{working_dir}/{repo_name}/app/src/main/java/com/bhargo/user", shell=True)

        subprocess.call(f"rm -r {working_dir}/{repo_name}/app/src/main/java/com/bhargo/user", shell=True)

        subprocess.call(f"mkdir {newPath}", cwd=f"{working_dir}/{repo_name}/app/src/test/java", shell=True)

        subprocess.call(f"cp -r {working_dir}/{repo_name}/app/src/test/java/com/bhargo/user/* {working_dir}/{repo_name}/app/src/test/java/{newPath}/* /s /e /i /Y", cwd=f"{working_dir}/{repo_name}/app/src/test/java/com/bhargo/user", shell=True)

        subprocess.call(f"rm -r {working_dir}/{repo_name}/app/src/test/java/com/bhargo/user", shell=True)

    subprocess.call(f"cp -r {working_dir}/local.properties {working_dir}/{repo_name}/", shell=True)

    subprocess.call(f"cp -r {working_dir}/gradle-wrapper.jar {working_dir}/{repo_name}/gradle/wrapper/", shell= True)

    # Build Gradle

    subprocess.call(f"{working_dir}/{repo_name}/./gradlew assembleDebug", cwd=f"{working_dir}/{repo_name}/", shell=True)

#  subprocess.call(f"mkdir {output_path}", cwd=f"{working_dir}", shell=True)

# subprocess.call(f"copy {working_dir}\\{apk_path}\\app-debug.apk {working_dir}\\{output_path}\\", shell=True)

# subprocess.call(f"rmdir /Q /S {working_dir}\\user4.0newdesign", shell=True)

#print(f"copy {working_dir}\\{apk_path}\\app-debug.apk {working_dir}\\{output_path}\\")

#    subprocess.call(f"cp -r {working_dir}/{repo_name}/app/build/outputs/apk/debug/app-arm64-v8a-debug.apk {working_dir}/{output_path}/", shell=True)

apkGenerator("config.yaml", "app4")
