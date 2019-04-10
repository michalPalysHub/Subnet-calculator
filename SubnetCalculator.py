# IP xxx.xxx.xxx.xxx/mask
#     a . b . c . d /mask

import sys


def is_ip_adress_valid():
    adress = sys.argv[1].split('/');
    IP = adress[0].split('.')

    if len(IP) != 4:
        print("There have to be 4 octets!")
        return False

    if len(adress) != 2:
        print("IP adress must contain the mask!")
        return False

    for i in range(0, len(IP)):
        for char in IP[i]:
            if char.isalpha():
                print("IP adress contains a letter!")
                return False

    mask = adress[1]

    for char in mask:
        if char.isalpha():
            print("Mask contains a letter!")
            return False

    for i in range(0, len(IP)):
        if int(IP[i]) < 0:
            print("IP segment out of 0-255 range!")
            return False
        if int(IP[i]) > 255:
            print("IP segment out of 0-255 range!")
            return False

    if int(mask) > 32 or int(mask) < 0:
        print("mask out of 0-32 range!")
        return False

    return True


def get_network_class(IP):
    if 1 <= IP[0] <= 127:
        print("Network class: A")
        return 'A'
    elif 128 <= IP[0] <= 191:
        print("Network class: B")
        return 'B'
    elif 192 <= IP[0] <= 223:
        print("Network class: C")
        return 'C'
    elif 224 <= IP[0] <= 239:
        print("Network class: D")
        return 'D'
    elif 240 <= IP[0] <= 254:
        print("Network class: E")
        return 'E'


def public_or_private_adress(IP):
    is_public = True

    if IP[0] == 10:
        is_public = False
    elif IP[0] == 172:
        if 16 <= IP[1] <= 31:
            is_public = False
    elif IP[0] == 192:
        if IP[1] == 168:
            is_public = False

    if is_public:
        print("This network is public")
    else:
        print("This network is private")


def get_mask_in_binary_from_adress(mask):
    mask_binary = "1"*mask
    mask_binary = mask_binary.zfill(32)[::-1]
    mask_binary = mask_binary[:8] + "." + mask_binary[8:16] + "." + mask_binary[16:24] + "." + mask_binary[24:32]
    mask_binary = mask_binary.split('.')

    for i in range(0,4):
        mask_binary[i] = "0b" + mask_binary[i]

    return mask_binary


def print_mask_in_binary(mask):
    tmp = get_mask_in_binary_from_adress(mask)
    for i in range(0,4):
        tmp[i] = tmp[i][2:]
    print("Mask in binary: {}.{}.{}.{}".format(tmp[0], tmp[1], tmp[2], tmp[3]))


def get_mask_in_decimal_from_adress(mask):
    mask_d = []
    mask_b = get_mask_in_binary_from_adress(mask)

    for i in range(0, len(mask_b)):
        mask_d.append(int(mask_b[i], 2))

    print("Mask in decimal: {}.{}.{}.{}".format(mask_d[0], mask_d[1], mask_d[2], mask_d[3]))
    return mask_d


def get_broadcast_adress_in_binary(IP, mask):
    ip = []

    for i in range(0, 4):
        ip.append(bin(IP[i]))
        ip[i] = ip[i][2:].zfill(8)

    tmp1 = ip[0] + ip[1] + ip[2] + ip[3]
    tmp2 = "1" * mask
    tmp2 = tmp2.zfill(32)[::-1]
    tmp3 = ""

    for i in range(0, 32):
        if tmp2[i] == "1":
            tmp3 = tmp3 + tmp1[i]
        else:
            tmp3 = tmp3 + "1"

    tmp3 = tmp3[:8] + "." + tmp3[8:16] + "." + tmp3[16:24] + "." + tmp3[24:32]
    print("Broadcast adress in binary: {}".format(tmp3))

    tmp3 = tmp3.split('.')
    for i in range(0,4):
        tmp3[i] = "0b" + tmp3[i]

    return tmp3


def get_broadcast_adress_in_decimal(IP, mask):
    binary = get_broadcast_adress_in_binary(IP, mask)
    decimal = []

    for i in range(0, len(binary)):
        decimal.append(int(binary[i], 2))

    print("Broadcast adress in decimal: {}.{}.{}.{}".format(decimal[0], decimal[1], decimal[2], decimal[3]))
    return decimal


def get_network_adress(IP, Mask):
    ip = []
    mask = get_mask_in_binary_from_adress(Mask)
    adress = []

    for i in range(0, 4):
        ip.append(bin(IP[i]))

    for j in range(0, 4):
        adress.append(int(ip[j],2) & int(mask[j],2))

    print("\nNetwork adress: {}.{}.{}.{}".format(adress[0], adress[1], adress[2], adress[3]))


def first_host_adress_in_binary():
    print "TODO"


def first_host_adress_in_decimal():
    print "TODO"


def last_host_adress_in_binary():
    print "TODO"


def last_host_adress_in_decimal():
    print "TODO"


def max_amount_of_hosts():
    print "TODO"



def subnet_calculator():
    if not sys.argv[1]:
        print("no IP adress passed, set default value")

    if not is_ip_adress_valid():
        print("IP adress is invalid!")
        return
    else:
        adress = sys.argv[1].split('/');
        IP = adress[0].split('.')
        mask = adress[1]

        for i in range(0, 4):
            IP[i] = int(IP[i])
        mask = int(mask)

        print(sys.argv[1])
        get_network_adress(IP, mask)
        get_network_class(IP)
        public_or_private_adress(IP)
        print_mask_in_binary(mask)
        get_mask_in_decimal_from_adress(mask)
        get_broadcast_adress_in_decimal(IP, mask)


subnet_calculator()