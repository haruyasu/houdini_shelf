import os

def IncreaseVersion(fullPath, originalVersion=None):
    fn, ext = os.path.splitext(fullPath)
    fnreverse = fn[::-1]
    versionString = ""
    versionNumber = 0
    beginVersionString = False

    for letter in fnreverse:
        if letter.isdigit() is True:
            beginVersionString = True
            versionString += letter
        else:
            if beginVersionString is True:
                versionString = versionString[::-1]
                versionNumber = int(versionString)
                break

    if originalVersion is None:
        if versionString == '':
            originalVersion = "No Version"
        else:
            originalVersion = versionString

    versionNumber += 1
    fill_length = len(versionString)
    divider = ''

    if fill_length == 0:
        if fn[-1] != '_' or fn[-1] != '-':
            divider = '_'
        fill_length = 3
    versionStringNew = divider + str(versionNumber).zfill(fill_length)

    fnreverse = fnreverse.replace(versionString[::-1], versionStringNew[::-1], 1)
    fullPathNew = fnreverse[::-1] + ext

    if os.path.exists(fullPathNew):
        print("{0} already exists, increasing further...").format(fullPathNew, originalVersion)
        fullPathNew = IncreaseVersion(fullPathNew, originalVersion)
    else:
        print("Increased version {0} to {1}").format(originalVersion, versionStringNew)
        print("Changed path {0} to {1}").format(fullPath, fullPathNew)
    return fullPathNew

def main():
    currentPath = hou.hipFile.name()
    fullPathNew = IncreaseVersion(currentPath)
    hou.hipFile.setName(fullPathNew)
    hou.hipFile.save()
    print("Saved as {0}").format(fullPathNew)

if __name__ == '__main__':
    main()