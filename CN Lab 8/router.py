# We must import the functions from Part 1
import ip_utils

class Router:
    """
    Implements a router with a forwarding table based on longest prefix matching.
    """
    
    def __init__(self, routes):
        """
        Initializes the router with a list of routes.
        """
        self.forwarding_table = []
        self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes):
        """
        Converts human-readable routes into an optimized internal table
        storing binary prefixes.
        """
        for cidr, link in routes:
            # Get the binary prefix for each CIDR
            prefix = ip_utils.get_network_prefix(cidr)
            self.forwarding_table.append((prefix, link))
        
        # Sort the table by prefix length, from longest to shortest.
        # This is the crucial step for the algorithm.
        self.forwarding_table.sort(key=lambda item: len(item[0]), reverse=True)

    def route_packet(self, dest_ip: str) -> str:
        """
        Finds the correct output link for a destination IP using
        the longest prefix matching algorithm.
        """
        # Convert the destination IP to its 32-bit binary form
        binary_dest_ip = ip_utils.ip_to_binary(dest_ip)
        
        # Iterate through the sorted table
        for prefix, link in self.forwarding_table:
            # Check if the destination IP starts with the prefix
            if binary_dest_ip.startswith(prefix):
                # The first match is the longest match
                return link
        
        # If no match is found, return the default route
        return "Default Gateway"


# --- Test Case ---
# This block will run only when router.py is executed directly
if __name__ == "__main__":
    # 1. Initialize the Router with the specified routes
    route_list = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    my_router = Router(route_list)

    # 2. Verify the test cases
    print(f"'223.1.1.100' -> {my_router.route_packet('223.1.1.100')}") # Expect "Link 0"
    print(f"'223.1.2.5'   -> {my_router.route_packet('223.1.2.5')}") # Expect "Link 1"
    print(f"'223.1.250.1' -> {my_router.route_packet('223.1.250.1')}") # Expect "Link 4 (ISP)"
    print(f"'198.51.100.1' -> {my_router.route_packet('198.51.100.1')}") # Expect "Default Gateway"
