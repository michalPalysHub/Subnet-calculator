# IP xxx.xxx.xxx.xxx/mask
#     a . b . c . d /mask

import sys


def get_network_class(IP):
    a = int(IP[0], 2)
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
    is_public = True

    if int(IP[0], 2) == 10:
        is_public = False
    elif int(IP[0], 2) == 172:
        if 16 <= int(IP[1], 2) <= 31:
            is_public = False
    elif int(IP[0], 2) == 192:
        if int(IP[1], 2) == 168:
            is_public = False

    if is_public:
        return "public"
    else:
        return "private"


def get_mask_in_binary_from_adress(mask):
    mask_binary = "1"*int(mask)
    mask_binary = mask_binary.zfill(32)[::-1]
    mask_binary = mask_binary[:8] + "." + mask_binary[8:16] + "." + mask_binary[16:24] + "." + mask_binary[24:32]
    return mask_binary.split(".")


def get_mask_in_decimal_from_adress(mask):
    mask_decimal = []
    mask_binary = get_mask_in_binary_from_adress(mask)

    for i in range(0, len(mask_binary)):
        mask_decimal.append(int(mask_binary[i], 2))

    return mask_decimal


def get_network_adress(IP, mask):
    ip = []
    mask = get_mask_in_binary_from_adress(mask)
    network_adress = []

    for i in range(0, 4):
        ip.append(IP[i])

    for i in range(0, 4):
        a = ip[i][2:].zfill(8)
        ip[i] = a

    for i in range(0, 4):
        network_adress.append(int(ip[i], 2) & int(mask[i], 2))

    return network_adress


def get_broadcast_adress(IP):
    return


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
    print("\nNetwork adress: {}".format(get_network_adress(IP, mask)))
    print("Network class: {}".format(get_network_class(IP)))
    print("This network is {}".format(public_or_private_adress(IP)))
    print("Mask in binary: {}".format(get_mask_in_binary_from_adress(mask)))
    print("Mask in decimal: {}".format(get_mask_in_decimal_from_adress(mask)))

# MAIN

subnet_calculator()
