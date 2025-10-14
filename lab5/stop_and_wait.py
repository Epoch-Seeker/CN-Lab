import random
import time

class StopAndWaitARQ:
    def __init__(self, total_frames, loss_probability=0.3, timeout=2):
        self.total_frames = total_frames
        self.loss_probability = loss_probability
        self.timeout = timeout
        self.frames_sent = 0
        self.frames_retransmitted = 0
        
    def simulate_frame_transmission(self, frame_num):
        """Simulate frame transmission with random loss"""
        return random.random() > self.loss_probability
    
    def simulate_ack_transmission(self):
        """Simulate ACK transmission with random loss"""
        return random.random() > self.loss_probability
    
    def send_frame(self, frame_num):
        """Send a frame and wait for acknowledgment"""
        print(f"\nSending Frame {frame_num}")
        self.frames_sent += 1
        
        while True:
            # Simulate frame transmission
            frame_received = self.simulate_frame_transmission(frame_num)
            
            if not frame_received:
                print(f"Frame {frame_num} lost, retransmitting...")
                self.frames_retransmitted += 1
                time.sleep(0.5)  # Simulate timeout
                continue
            
            # Simulate ACK transmission
            ack_received = self.simulate_ack_transmission()
            
            if not ack_received:
                print(f"ACK {frame_num} lost, retransmitting Frame {frame_num}...")
                self.frames_retransmitted += 1
                time.sleep(0.5)  # Simulate timeout
                continue
            
            # Both frame and ACK successful
            print(f"ACK {frame_num} received")
            break
    
    def run(self):
        """Run the Stop-and-Wait ARQ simulation"""
        print("=" * 50)
        print("Stop-and-Wait ARQ Simulation")
        print("=" * 50)
        print(f"Total Frames: {self.total_frames}")
        print(f"Loss Probability: {self.loss_probability}")
        print(f"Timeout: {self.timeout}s")
        print("=" * 50)
        
        start_time = time.time()
        
        for frame_num in range(self.total_frames):
            self.send_frame(frame_num)
        
        end_time = time.time()
        
        # Display statistics
        print("\n" + "=" * 50)
        print("Transmission Complete!")
        print("=" * 50)
        print(f"Total Frames Sent: {self.frames_sent}")
        print(f"Frames Retransmitted: {self.frames_retransmitted}")
        print(f"Total Transmissions: {self.frames_sent + self.frames_retransmitted}")
        print(f"Time Taken: {end_time - start_time:.2f}s")
        print(f"Efficiency: {(self.frames_sent / (self.frames_sent + self.frames_retransmitted)) * 100:.2f}%")
        print("=" * 50)

if __name__ == "__main__":
    # Create and run simulation
    # Parameters: total_frames, loss_probability, timeout
    arq = StopAndWaitARQ(total_frames=5, loss_probability=0.3, timeout=2)
    arq.run()
