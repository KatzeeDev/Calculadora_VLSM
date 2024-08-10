# Import necessary libraries
from math import log2
from colored import fg, attr
from textwrap import wrap

# Function to check if input text is empty
def is_empty(text):
    return text.strip() == ""

# Function to validate network address
def is_correct_network_address(address):
    octets = address.split(".")
     # Check if it has four octets
    if len(octets) != 4:
        return False
     # Check if it has four octets
    for octet in octets:
        if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
            return False
    return True

# Function to calculate Variable Length Subnet Masking (VLSM)
def is_correct_endpoint_numbers_per_network(numbers):
    endpoints = numbers.split(",")
    for endpoint in endpoints:
        if not endpoint.isdigit() or int(endpoint) <= 0:
            return False
    return True


def is_correct_prefix(prefix):
    if not prefix.isdigit() or int(prefix) < 0 or int(prefix) > 32:
        return False
    return True


def power_bit_length(x):
    return 2 ** (x - 1).bit_length()


def get_mask_from_prefix(prefix):
    subnet_mask_dec = ""
    for octet in wrap(("0" * (32 - prefix)).rjust(32, "1"), 8):
        subnet_mask_dec += f"{int(octet, 2)}."
    return subnet_mask_dec[:-1]


def get_32bit_format(ip_address):
    format_32bit = ""
    for octet in ip_address.split("."):
        format_32bit += f'{bin(int(octet)).replace("0b", "").rjust(8, "0")}'
    return format_32bit


def get_ip_from_32bit_format(format_32bit):
    ip_dec = ""
    for octet in wrap(format_32bit, 8):
        ip_dec += f"{int(octet, 2)}."
    return ip_dec[:-1]


def get_first_addressable_ip(network_ip):
    first_addressable_ip_bin_32bit = bin(int(get_32bit_format(network_ip), 2) +
                                         int("1", 2)).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(first_addressable_ip_bin_32bit)


def get_last_addressable_ip(network_ip, mask):
    broadcast_ip_32bit = get_32bit_format(get_broadcast_ip(network_ip, mask))
    last_addressable_ip_bin_32bit = bin(int(broadcast_ip_32bit, 2) -
                                        int("1", 2)).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(last_addressable_ip_bin_32bit)


def get_broadcast_ip(network_ip, mask):
    broadcast_ip_32bit = f"{get_32bit_format(network_ip)[:-get_32bit_format(mask).count('0')]}" \
                         f"{'1' * get_32bit_format(mask).count('0')}"
    return get_ip_from_32bit_format(broadcast_ip_32bit)


def get_next_network_ip(network_ip, mask):
    broadcast_ip_32bit = get_32bit_format(get_broadcast_ip(network_ip, mask))
    next_network_ip_32bit = bin(int(broadcast_ip_32bit, 2) +
                                int("1", 2)).replace("0b", "").rjust(32, "0")
    return get_ip_from_32bit_format(next_network_ip_32bit)


def calculate_vlsm(network_ip, endpoint_numbers_per_network, prefix):
    subnets = []
    network_hosts = endpoint_numbers_per_network.split(",")
    length_of_subnets = []

    for hosts in network_hosts:
        if int(hosts) > 0:
            hosts = int(hosts) + 2
            length_of_subnets.append(power_bit_length(int(hosts)))

    length_of_subnets.sort(reverse=True)
    sum_all_hosts = sum(length_of_subnets)

    if is_empty(prefix):
        first_octet = int(network_ip.split(".")[0])

        if 1 <= first_octet < 128:
            if sum_all_hosts <= pow(2, 24):
                inject_data_to_dict(network_ip, length_of_subnets, subnets)
            else:
                print("El maximo de host excede el limite para una Red de Clase A (The number of hosts exceeds the maximum limit for Class A network.)")

        elif 128 <= first_octet < 192:
            if sum_all_hosts <= pow(2, 16):
                inject_data_to_dict(network_ip, length_of_subnets, subnets)
            else:
                print("El maximo de host excede el limite para una Red de Clase B  (The number of hosts exceeds the maximum limit for Class B network.)")

        elif 192 <= first_octet < 224:
            if sum_all_hosts <= pow(2, 8):
                inject_data_to_dict(network_ip, length_of_subnets, subnets)
            else:
                print("El maximo de host excede el limite para una Red de Clase C (The number of hosts exceeds the maximum limit for Class C network.)")

    else:
        if sum_all_hosts <= pow(2, 32 - int(prefix)):
            inject_data_to_dict(network_ip, length_of_subnets, subnets)
        else:
            print("The number of hosts exceeds the maximum limit for the specified prefix length.")

    return subnets

# Function to inject calculated data into a dictionary
def inject_data_to_dict(network_ip, length_of_subnets, subnets):
    for network in length_of_subnets:
        # Calculate the number of host bits and prefix
        hostbits = int(log2(network))
        prefix = 32 - hostbits
        # Calculate subnet mask
        mask = get_mask_from_prefix(prefix)

        # Append the subnet information to the list
        subnets.append({
            "Network Address": network_ip,
            "IP Range": f"{get_first_addressable_ip(network_ip)} - {get_last_addressable_ip(network_ip, mask)}",
            "Broadcast Address": get_broadcast_ip(network_ip, mask),
            "Subnet Mask": mask,
            "Prefix": f"/{prefix}",
            "Addressable Hosts": pow(2, hostbits) - 2
        })
         # Get the IP address of the next network
        network_ip = get_next_network_ip(network_ip, mask)


# Main function
def main():
    # Take user inputs
    network_ip = input(f'{fg(2)}Ingrese la dirección de red inicial: (Enter the initial network address:) {attr(0)}')
    endpoint_numbers_per_network = input(f'{fg(2)}Ingrese el número de hosts por red: (Enter the number of hosts per network:) {attr(0)}')
    prefix = input(f'{fg(2)}Ingrese el prefijo de la máscara de subred (deje vacío para el valor predeterminado según la dirección de red): (Enter the subnet mask prefix (leave blank for the default value based on the network address) {attr(0)}')

    # Check if user inputs are valid    
    if is_correct_network_address(network_ip) and is_correct_endpoint_numbers_per_network(endpoint_numbers_per_network):
          
        # Calculate VLSM
        subnets = calculate_vlsm(network_ip, endpoint_numbers_per_network, prefix)

        for subnet in subnets:
            print(f'\n{fg(2)}Información de la subred (Subnet Information)')
            print(f'{fg(1)}Dirección de Red (Network Address):', subnet["Network Address"])
            print(f'{fg(5)}Prefijo (Prefix):', subnet["Prefix"])
            print(f'{fg(4)}Rango IP (IP Range):', subnet["IP Range"])
            print(f'{fg(6)}Dirección de Broadcast (Broadcast Address):', subnet["Broadcast Address"])
            print(f'{fg(7)}Máscara de Subred (Subnet Mask):', subnet["Subnet Mask"])
            print(f'{fg(8)}Hosts direccionables (Addressable Hosts):', subnet["Addressable Hosts"])
            print(attr(0))
    else:
        print("Invalid input.")

if __name__ == "__main__":
    main()