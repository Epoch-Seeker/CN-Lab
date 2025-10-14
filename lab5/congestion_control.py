import matplotlib.pyplot as plt
import random

class TCPCongestionControl:
    def __init__(self, max_rounds=50, loss_probability=0.1, ssthresh_initial=16):
        self.max_rounds = max_rounds
        self.loss_probability = loss_probability
        self.ssthresh = ssthresh_initial
        self.cwnd = 1  # Congestion window starts at 1
        self.cwnd_history = []
        self.round_history = []
        self.phase_history = []
        self.current_round = 0
        
    def simulate_packet_loss(self):
        """Simulate packet loss with given probability"""
        return random.random() < self.loss_probability
    
    def slow_start(self):
        """Slow Start phase - exponential growth"""
        if self.cwnd < self.ssthresh:
            self.cwnd *= 2  # Double cwnd each RTT
            return "Slow Start"
        else:
            return self.congestion_avoidance()
    
    def congestion_avoidance(self):
        """Congestion Avoidance phase - linear growth"""
        self.cwnd += 1  # Increase cwnd by 1 each RTT
        return "Congestion Avoidance"
    
    def handle_timeout(self):
        """Handle timeout - multiplicative decrease"""
        self.ssthresh = max(self.cwnd // 2, 2)  # ssthresh = cwnd/2
        self.cwnd = 1  # Reset to 1
        return "Timeout/Loss"
    
    def run_simulation(self):
        """Run the TCP congestion control simulation"""
        print("=" * 70)
        print("TCP Congestion Control Simulation")
        print("=" * 70)
        print(f"Max Rounds: {self.max_rounds}")
        print(f"Loss Probability: {self.loss_probability}")
        print(f"Initial ssthresh: {self.ssthresh}")
        print("=" * 70)
        print(f"\n{'Round':<8} {'cwnd':<10} {'ssthresh':<12} {'Phase':<25}")
        print("-" * 70)
        
        for round_num in range(self.max_rounds):
            self.current_round = round_num
            
            # Check for packet loss
            if self.simulate_packet_loss():
                phase = self.handle_timeout()
                print(f"{round_num:<8} {self.cwnd:<10} {self.ssthresh:<12} {phase:<25}")
            else:
                # No loss - continue with current phase
                if self.cwnd < self.ssthresh:
                    phase = self.slow_start()
                else:
                    phase = self.congestion_avoidance()
                print(f"{round_num:<8} {self.cwnd:<10} {self.ssthresh:<12} {phase:<25}")
            
            # Record history
            self.cwnd_history.append(self.cwnd)
            self.round_history.append(round_num)
            self.phase_history.append(phase)
        
        print("=" * 70)
        print("Simulation Complete!")
        print("=" * 70)
    
    def plot_results(self, filename="cwnd_plot.png"):
        """Plot cwnd vs transmission rounds"""
        plt.figure(figsize=(12, 7))
        
        # Plot cwnd over time
        plt.plot(self.round_history, self.cwnd_history, 'b-', linewidth=2, marker='o', markersize=4)
        
        # Mark different phases with colors
        for i in range(len(self.round_history)):
            if self.phase_history[i] == "Slow Start":
                plt.plot(self.round_history[i], self.cwnd_history[i], 'go', markersize=6)
            elif self.phase_history[i] == "Congestion Avoidance":
                plt.plot(self.round_history[i], self.cwnd_history[i], 'yo', markersize=6)
            elif self.phase_history[i] == "Timeout/Loss":
                plt.plot(self.round_history[i], self.cwnd_history[i], 'ro', markersize=8)
        
        plt.xlabel('Transmission Round', fontsize=12, fontweight='bold')
        plt.ylabel('Congestion Window (cwnd)', fontsize=12, fontweight='bold')
        plt.title('TCP Congestion Control: cwnd vs Transmission Rounds', 
                  fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='b', linewidth=2, label='cwnd'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='g', 
                   markersize=8, label='Slow Start'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='y', 
                   markersize=8, label='Congestion Avoidance'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='r', 
                   markersize=8, label='Timeout/Loss')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved as '{filename}'")
        plt.show()

if __name__ == "__main__":
    # Create and run simulation
    tcp = TCPCongestionControl(max_rounds=50, loss_probability=0.1, ssthresh_initial=16)
    tcp.run_simulation()
    tcp.plot_results("cwnd_plot.png")
