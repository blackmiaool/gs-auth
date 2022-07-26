import platform
ua = {
    'isGS': platform.release().find("clockworkpi") != -1
}


navCodeMap = {
    314: True,
    315: True,
    316: True,
    317: True
}
keyCodeMap = {
    27: 'Menu',
    315: "Up",
    317: "Down",
    314: "Left",
    316: "Right",
    74: ua["isGS"] and 'A' or 'J',
    75: ua["isGS"] and 'B' or 'K',
    85: ua["isGS"] and 'X' or 'U',
    73: ua["isGS"] and 'Y' or 'I',
    32: ua["isGS"] and 'Select' or 'Space',
    13: ua["isGS"] and 'Start' or 'Enter',
    72: 'Shift+A',
    76: 'Shift+B',
    89: 'Shift+X',
    79: 'Shift+Y',
    390: 'Shift+Select',
    388: 'Shift+Start',
}
gsKeyNameMap = {
    'Menu': 27,
    "Up": 315,
    "Down": 317,
    "Left": 314,
    "Right": 316,
    'A': 74,
    'B': 75,
    'X': 85,
    'Y': 73,
    'Select': 32,
    'Start': 13,
    'Shift+A': 72,
    'Shift+B': 76,
    'Shift+X': 89,
    'Shift+Y': 79,
    'Shift+Select': 390,
    'Shift+Start': 388
}
gsKeyCodeMap = {}
for keyName in gsKeyNameMap:
    gsKeyCodeMap[keyName] = keyCodeMap[gsKeyNameMap[keyName]]


funcKey = {
    'Menu': True,
    'Start': True,
    'Select': True,
    'Enter': True,
    'Space': True
}
dataFileName = "data.json"
