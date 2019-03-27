# IP xxx.xxx.xxx.xxx/mask
#     a . b . c . d /mask

import sys

def network_class(a):
    if 1 <= a <= 127:
        return 'A'
    elif 128 <= a <= 191:
        return 'B'
    elif 192 <= a <= 223:
        return 'C'
    elif 224 <= a <= 239:
        return 'D'
    elif 240 <= a <= 254:
        return 'E'

def public_or_private_adress(IP):
    isPublic = True

    if int(IP[0],2) == 10:
        isPublic = False
    elif int(IP[0],2) == 172:
        if 16 <= int(IP[1],2) <= 31:
            isPublic = False
    elif int(IP[0], 2) == 192:
        if int(IP[1], 2) == 168:
            isPublic = False

    if isPublic:
        return "public"
    else:
        return "private"


def subnet_calculator():

    if not sys.argv[1]:
        print("no IP adress passed, set default value")

    adress = sys.argv[1].split('/');
    IP = adress[0].split('.')
    mask = adress[1]

    for i in range(0, len(IP)):
        IP[i] = bin(int(IP[i]))
        if len(IP[i]) > 0b11111111:
            print("IP segment out of 0-255 range!")
            return -1

    print(sys.argv[1])
    print("\nNetwork class: {}".format(network_class(int(IP[0],2))))
    print("This network is {}".format(public_or_private_adress(IP)))


# MAIN

subnet_calculator()