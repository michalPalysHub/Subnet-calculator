import sys
import socket

f = open("subnet_calculator.txt", "a")


def is_ip_adress_passed():
    if len(sys.argv) < 2:
        return False
    else:
        return True


def is_ip_adress_valid():
    adress = sys.argv[1].split('/');
    IP = adress[0].split('.')
    mask = adress[1]

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
        return 'A'
    elif 128 <= IP[0] <= 191:
        return 'B'
    elif 192 <= IP[0] <= 223:
        return 'C'
    elif 224 <= IP[0] <= 239:
        return 'D'
    elif 240 <= IP[0] <= 254:
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
        return "public"
    else:
        return "private"


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
    f.write("Mask in binary: {}.{}.{}.{}\n".format(tmp[0], tmp[1], tmp[2], tmp[3]))


def get_mask_in_decimal_from_adress(mask):
    mask_d = []
    mask_b = get_mask_in_binary_from_adress(mask)

    for i in range(0, len(mask_b)):
        mask_d.append(int(mask_b[i], 2))

    return mask_d


def print_mask_in_decimal(mask):
    mask_d = get_mask_in_decimal_from_adress(mask)
    print("Mask in decimal: {}.{}.{}.{}".format(mask_d[0], mask_d[1], mask_d[2], mask_d[3]))
    f.write("Mask in decimal: {}.{}.{}.{}\n".format(mask_d[0], mask_d[1], mask_d[2], mask_d[3]))


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
    tmp3 = tmp3.split('.')
    for i in range(0,4):
        tmp3[i] = "0b" + tmp3[i]

    return tmp3


def print_broadcast_adress_in_binary(IP, mask):
    tmp = get_broadcast_adress_in_binary(IP, mask)
    for i in range(0,4):
        tmp[i] = tmp[i][2:]

    print("Broadcast adress in binary: {}.{}.{}.{}".format(tmp[0], tmp[1], tmp[2], tmp[3]))
    f.write("Broadcast adress in binary: {}.{}.{}.{}\n".format(tmp[0], tmp[1], tmp[2], tmp[3]))


def get_broadcast_adress_in_decimal(IP, mask):
    binary = get_broadcast_adress_in_binary(IP, mask)
    decimal = []

    for i in range(0, len(binary)):
        decimal.append(int(binary[i], 2))

    return decimal


def print_broadcast_adress_in_decimal(IP, mask):
    tmp = get_broadcast_adress_in_decimal(IP, mask)
    print("Broadcast adress in decimal: {}.{}.{}.{}".format(tmp[0], tmp[1], tmp[2], tmp[3]))
    f.write("Broadcast adress in decimal: {}.{}.{}.{}\n".format(tmp[0], tmp[1], tmp[2], tmp[3]))


def get_network_adress(IP, Mask):
    ip = []
    mask = get_mask_in_binary_from_adress(Mask)
    adress = []

    for i in range(0, 4):
        ip.append(bin(IP[i]))

    for j in range(0, 4):
        adress.append(int(ip[j],2) & int(mask[j],2))

    return adress


def first_host_adress_in_decimal(IP, mask):
    host = get_network_adress(IP, mask)
    host[3] += 1
    return host


def first_host_adress_in_binary(IP, mask):
    tmp = first_host_adress_in_decimal(IP, mask)
    host = []
    for i in range (0, 4):
        tmp[i] = bin(tmp[i])
        host.append(tmp[i][2:].zfill(8))
    return host


def last_host_adress_in_decimal(IP, mask):
    host = get_broadcast_adress_in_decimal(IP, mask)
    host[3] -= 1
    return host


def last_host_adress_in_binary(IP, mask):
    tmp = last_host_adress_in_decimal(IP, mask)
    host = []
    for i in range(0, 4):
        tmp[i] = bin(tmp[i])
        host.append(tmp[i][2:].zfill(8))
    return host


def total_number_of_hosts(mask):
    amount = 2 ** (32 - int(mask)) - 2
    return amount


def subnet_calculator():
    if is_ip_adress_passed():
        if not is_ip_adress_valid():
            print("IP adress is invalid!")
            return
        adress = sys.argv[1].split('/');
        IP = adress[0].split('.')
        mask = adress[1]

        print(sys.argv[1])
        f.write("\n" + sys.argv[1] + "\n\n")
    else:
        print("no IP adress passed, set default value")
        IP = socket.gethostbyname(socket.gethostname())

        print(IP + "/24")
        f.write("\n" + IP + "/24" + "\n\n")

        IP = IP.split('.')
        mask = "24"

    for i in range(0, 4):
        IP[i] = int(IP[i])
    mask = int(mask)

    adress = get_network_adress(IP, mask)
    print("\nNetwork adress: {}.{}.{}.{}".format(adress[0], adress[1], adress[2], adress[3]))
    f.write("Network adress: {}.{}.{}.{}\n".format(adress[0], adress[1], adress[2], adress[3]))

    print("Network class: {}".format(get_network_class(IP)))
    f.write("Network class: {}\n".format(get_network_class(IP)))

    print("This network is {}".format(public_or_private_adress(IP)))
    f.write("This network is {}\n".format(public_or_private_adress(IP)))

    print_mask_in_binary(mask)
    print_mask_in_decimal(mask)

    print_broadcast_adress_in_binary(IP, mask)
    print_broadcast_adress_in_decimal(IP, mask)

    f_host_b = first_host_adress_in_binary(IP, mask)
    print("First host adress in binary: {}.{}.{}.{}".format(f_host_b[0], f_host_b[1], f_host_b[2], f_host_b[3]))
    f.write("First host adress in binary: {}.{}.{}.{}\n".format(f_host_b[0], f_host_b[1], f_host_b[2], f_host_b[3]))

    f_host = first_host_adress_in_decimal(IP, mask)
    print("First host adress in decimal: {}.{}.{}.{}".format(f_host[0], f_host[1], f_host[2], f_host[3]))
    f.write("First host adress in decimal: {}.{}.{}.{}\n".format(f_host[0], f_host[1], f_host[2], f_host[3]))

    l_host_b = last_host_adress_in_binary(IP, mask)
    print("Last host adress in binary: {}.{}.{}.{}".format(l_host_b[0], l_host_b[1], l_host_b[2], l_host_b[3]))
    f.write("Last host adress in binary: {}.{}.{}.{}\n".format(l_host_b[0], l_host_b[1], l_host_b[2], l_host_b[3]))

    l_host = last_host_adress_in_decimal(IP, mask)
    print("Last host adress in decimal: {}.{}.{}.{}".format(l_host[0], l_host[1], l_host[2], l_host[3]))
    f.write("Last host adress in decimal: {}.{}.{}.{}\n".format(l_host[0], l_host[1], l_host[2], l_host[3]))

    print("Total number of hosts equals {}".format(total_number_of_hosts(mask)))
    f.write("Total number of hosts equals {}\n".format(total_number_of_hosts(mask)))

subnet_calculator()