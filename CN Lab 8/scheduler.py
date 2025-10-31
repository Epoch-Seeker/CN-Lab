class Packet:
    """
    A simple class to store packet attributes.
    """
    def __init__(self, source_ip: str, dest_ip: str, payload: str, priority: int):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.payload = payload
        self.priority = priority # 0=High, 1=Medium, 2=Low

    def __repr__(self):
        """Helper function for clean printing."""
        return f"Packet(payload='{self.payload}', priority={self.priority})"


def fifo_scheduler(packet_list: list) -> list:
    """
    Simulates a First-Come, First-Served (FCFS/FIFO) scheduler.
    The input list is already in arrival order, so the output
    order is the same. We return a copy.
    """
    return packet_list.copy()

def priority_scheduler(packet_list: list) -> list:
    """
    Simulates a Priority Scheduler.
    Packets with higher priority (lower number) are sent first.
    """
    # Sort the list based on the packet's priority attribute
    return sorted(packet_list, key=lambda packet: packet.priority)


# --- Test Case ---
# This block will run only when scheduler.py is executed directly
if __name__ == "__main__":
    # 1. Create the list of packets in arrival order
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", 2), #
        Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", 2), #
        Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", 0), #
        Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", 1), #
        Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", 0)  #
    ]

    # 2. Run the FIFO scheduler and print results
    fifo_order = fifo_scheduler(packets)
    print("--- FIFO Scheduler Output ---")
    # Expected: Data 1, Data 2, VOIP 1, Video 1, VOIP 2
    for p in fifo_order:
        print(p.payload)

    # 3. Run the Priority scheduler and print results
    priority_order = priority_scheduler(packets)
    print("\n--- Priority Scheduler Output ---")
    # Expected: VOIP 1, VOIP 2, Video 1, Data 1, Data 2
    for p in priority_order:
        print(p.payload)
