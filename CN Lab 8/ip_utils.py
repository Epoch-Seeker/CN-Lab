def ip_to_binary(ip_address: str) -> str:
    """
    Converts a dotted-decimal IP address string to a 32-bit binary string.
    """
    # Split the IP into its four octets
    octets = ip_address.split('.')
    # Convert each octet to an 8-bit binary string, padding with leading zeros
    binary_octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
    # Join the four 8-bit strings to create the 32-bit binary representation
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    """
    Takes a CIDR string and returns the binary network prefix.
    """
    # Split the CIDR string into the IP and the prefix length
    ip, prefix_len_str = ip_cidr.split('/')
    prefix_len = int(prefix_len_str)
    
    # Convert the IP part to its full 32-bit binary form
    binary_ip = ip_to_binary(ip)
    
    # Return only the network prefix part of the binary string
    return binary_ip[:prefix_len]
