import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class LightningSimulation:
    def __init__(self):
        # Create the main window with a dark theme
        self.root = tk.Tk()
        self.root.title("Lightning Formation Simulation")
        self.root.configure(bg='black')
        
        # Create a figure with a dark background
        self.fig, self.ax = plt.subplots(figsize=(10, 8), facecolor='black')
        self.ax.set_facecolor('black')
        
        # Setup the plot
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_title("Lightning Formation Simulation", color='white', pad=20)
        
        # Remove grid and axis for cleaner look
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create custom colormaps
        self.cloud_colors = LinearSegmentedColormap.from_list('', ['darkgray', 'white'])
        self.lightning_colors = LinearSegmentedColormap.from_list('', ['#00FFFF', '#FFFFFF'])
        
        # Initialize plot objects
        self.clouds = self.ax.scatter([], [], c=[], cmap=self.cloud_colors, s=100, alpha=0.6)
        self.leader, = self.ax.plot([], [], color='#00FFFF', lw=2, alpha=0.6)
        self.stroke, = self.ax.plot([], [], color='white', lw=3)
        self.branches = [self.ax.plot([], [], color='#00FFFF', lw=1, alpha=0.4)[0] for _ in range(5)]
        
        # Initialize data
        self.init_data()
        
    def init_data(self):
        # Cloud formation data
        self.cloud_x = np.random.normal(5, 2, 100)
        self.cloud_y = np.random.normal(8, 1, 100)
        self.cloud_intensities = np.random.rand(100)
        
        # Lightning path using a more realistic zigzag pattern
        self.leader_x = [5]
        self.leader_y = [8]
        self.generate_lightning_path()
        
        # Branch data
        self.branch_paths = self.generate_branches()
        
    def generate_lightning_path(self):
        # Create a more realistic zigzag pattern
        current_x = 5
        current_y = 8
        while current_y > 0:
            # Random displacement for zigzag effect
            dx = np.random.normal(0, 0.3)
            dy = -np.random.uniform(0.2, 0.5)
            
            current_x += dx
            current_y += dy
            
            self.leader_x.append(current_x)
            self.leader_y.append(current_y)
    
    def generate_branches(self):
        branches = []
        for _ in range(5):
            # Select a random point along the main lightning path
            idx = np.random.randint(1, len(self.leader_x)-1)
            start_x = self.leader_x[idx]
            start_y = self.leader_y[idx]
            
            # Generate branch path
            branch_x = [start_x]
            branch_y = [start_y]
            
            # Create branching pattern
            for _ in range(np.random.randint(3, 8)):
                dx = np.random.normal(0, 0.2)
                dy = np.random.normal(-0.2, 0.2)
                branch_x.append(branch_x[-1] + dx)
                branch_y.append(branch_y[-1] + dy)
            
            branches.append((branch_x, branch_y))
        return branches
    
    def update(self, frame):
        if frame < 50:  # Cloud formation
            size = min(100, frame * 2)
            self.clouds.set_offsets(np.c_[self.cloud_x[:size], self.cloud_y[:size]])
            self.clouds.set_array(self.cloud_intensities[:size])
            
        elif frame < 100:  # Charge separation (clouds getting darker)
            self.clouds.set_offsets(np.c_[self.cloud_x, self.cloud_y])
            intensities = self.cloud_intensities * (1 - (frame-50)/50)
            self.clouds.set_array(intensities)
            
        elif frame < 150:  # Leader formation
            progress = (frame - 100) / 50
            idx = int(len(self.leader_x) * progress)
            self.leader.set_data(self.leader_x[:idx], self.leader_y[:idx])
            
            # Animate branches
            for branch, (bx, by) in zip(self.branches, self.branch_paths):
                bidx = int(len(bx) * progress)
                branch.set_data(bx[:bidx], by[:bidx])
                
        elif frame < 200:  # Return stroke
            progress = (frame - 150) / 50
            self.stroke.set_data(self.leader_x, self.leader_y)
            self.stroke.set_alpha(progress)
            
            # Flash effect
            if frame % 2 == 0:
                self.ax.set_facecolor('#1a1a1a')
            else:
                self.ax.set_facecolor('black')
                
        else:  # Fade out
            alpha = max(0, 1 - (frame-200)/50)
            self.stroke.set_alpha(alpha)
            self.ax.set_facecolor('black')
        
        return [self.clouds, self.leader, self.stroke] + self.branches
    
    def run(self):
        # Create the animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update, frames=250,
            interval=20, blit=True
        )
        
        # Create canvas and pack it
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Run the application
        self.root.mainloop()

if __name__ == "__main__":
    sim = LightningSimulation()
    sim.run()
