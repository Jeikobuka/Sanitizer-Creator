import os
# ------------------------------------------------
converts = {}

def getConverts(prepend_path, sanitizerConfigFile):
    with open(prepend_path+'\\'+sanitizerConfigFile, 'r') as f:
        for line in f.readlines():
            converts[line.split('->')[0].strip()] = line.split('->')[1].strip()
    return converts

def convertGCodes(content, scriptPath, sanitizerConfigFile):
    converts = getConverts(scriptPath, sanitizerConfigFile)
    newConvContent = []
    for line in content.split('\n'):
        for convert in converts:
            if convert in line:
                line = line.replace(convert, converts[convert].split('...')[0])
                if "..." in converts[convert]:
                    line += '\n'+converts[convert].split('...')[1]
                break
        newConvContent.append(line)
    return '\n'.join(newConvContent)

def main(content, sanitizerConfigFile):
    newContent = convertGCodes(content, os.path.dirname(__file__), sanitizerConfigFile)
    print(newContent)
    return newContent


with open('test.txt', 'r') as f:
    main(f.read(), 'script.txt')
