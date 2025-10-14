import random
import time

class GoBackNARQ:
    def __init__(self, total_frames, window_size, loss_probability=0.2):
        self.total_frames = total_frames
        self.window_size = window_size
        self.loss_probability = loss_probability
        self.base = 0  # Base of the window
        self.next_seq_num = 0  # Next sequence number to send
        self.frames_sent = 0
        self.frames_retransmitted = 0
        
    def simulate_frame_loss(self):
        """Simulate frame loss with given probability"""
        return random.random() < self.loss_probability
    
    def send_window(self):
        """Send all frames in current window"""
        window_end = min(self.base + self.window_size, self.total_frames)
        
        if self.base < self.total_frames:
            frame_range = f"{self.base}-{window_end - 1}" if window_end - self.base > 1 else f"{self.base}"
            print(f"\nSending frames {frame_range}")
        
        lost_frame = -1
        
        # Send frames in the window
        for i in range(self.base, window_end):
            if self.simulate_frame_loss():
                lost_frame = i
                print(f"Frame {i} lost")
                break
            else:
                self.frames_sent += 1
        
        return lost_frame
    
    def run(self):
        """Run the Go-Back-N ARQ simulation"""
        print("=" * 60)
        print("Go-Back-N ARQ Simulation")
        print("=" * 60)
        print(f"Total Frames: {self.total_frames}")
        print(f"Window Size: {self.window_size}")
        print(f"Loss Probability: {self.loss_probability}")
        print("=" * 60)
        
        start_time = time.time()
        
        while self.base < self.total_frames:
            # Send frames in current window
            lost_frame = self.send_window()
            
            if lost_frame != -1:
                # Frame lost - retransmit from lost frame
                window_end = min(self.base + self.window_size, self.total_frames)
                retrans_end = window_end - 1
                
                if retrans_end > lost_frame:
                    print(f"Retransmitting frames {lost_frame}-{retrans_end}")
                else:
                    print(f"Retransmitting frame {lost_frame}")
                
                # Count retransmissions
                for i in range(lost_frame, window_end):
                    if i > lost_frame:  # Don't double count the lost frame
                        self.frames_retransmitted += 1
                
                time.sleep(0.3)  # Simulate timeout
            else:
                # All frames in window received successfully
                window_end = min(self.base + self.window_size, self.total_frames)
                last_ack = window_end - 1
                
                if last_ack >= self.base:
                    print(f"ACK {last_ack} received")
                    
                    # Slide window
                    old_base = self.base
                    self.base = window_end
                    
                    if self.base < self.total_frames:
                        new_window_end = min(self.base + self.window_size - 1, self.total_frames - 1)
                        print(f"Window slides to {self.base}-{new_window_end}")
                
                time.sleep(0.2)
        
        end_time = time.time()
        
        # Display statistics
        print("\n" + "=" * 60)
        print("Transmission Complete!")
        print("=" * 60)
        print(f"Total Frames Successfully Sent: {self.frames_sent}")
        print(f"Frames Retransmitted: {self.frames_retransmitted}")
        print(f"Total Transmissions: {self.frames_sent + self.frames_retransmitted}")
        print(f"Time Taken: {end_time - start_time:.2f}s")
        print(f"Efficiency: {(self.total_frames / (self.frames_sent + self.frames_retransmitted)) * 100:.2f}%")
        print("=" * 60)

if __name__ == "__main__":
    # Create and run simulation
    # Parameters: total_frames, window_size, loss_probability
    arq = GoBackNARQ(total_frames=10, window_size=4, loss_probability=0.2)
    arq.run()
