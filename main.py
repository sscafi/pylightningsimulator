import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import random
from math import sin, cos, pi

class LightningSimulation:
    def __init__(self):
        # Create the main window with a dark theme
        self.root = tk.Tk()
        self.root.title("Lightning Formation Simulation")
        self.root.configure(bg='black')
        
        # Make window resizable and set minimum size
        self.root.minsize(800, 600)
        self.root.geometry("1000x800")
        
        # Create a frame for controls
        self.control_frame = tk.Frame(self.root, bg='black')
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Add control buttons
        self.add_controls()
        
        # Create a figure with a dark background
        self.fig, self.ax = plt.subplots(figsize=(10, 8), facecolor='black')
        self.ax.set_facecolor('black')
        
        # Setup the plot with dynamic limits
        self.plot_width = 10
        self.plot_height = 10
        self.ax.set_xlim(0, self.plot_width)
        self.ax.set_ylim(0, self.plot_height)
        self.ax.set_title("Lightning Formation Simulation", color='white', pad=20)
        
        # Remove grid and axis for cleaner look
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create custom colormaps
        self.cloud_colors = LinearSegmentedColormap.from_list('', ['#0a0a0a', '#4a4a4a', '#a0a0a0'])
        self.lightning_colors = LinearSegmentedColormap.from_list('', ['#00FFFF', '#00BFFF', '#FFFFFF'])
        
        # Initialize plot objects
        self.clouds = self.ax.scatter([], [], c=[], cmap=self.cloud_colors, s=100, alpha=0.8)
        self.leader, = self.ax.plot([], [], color='#00FFFF', lw=2, alpha=0.8)
        self.stroke, = self.ax.plot([], [], color='white', lw=3)
        self.secondary_strokes = [self.ax.plot([], [], color='#00FFFF', lw=1.5, alpha=0.7)[0] for _ in range(3)]
        self.branches = [self.ax.plot([], [], color='#00FFFF', lw=1, alpha=0.5)[0] for _ in range(8)]
        
        # Initialize data
        self.init_data()
        
        # Animation control
        self.is_playing = False
        self.current_frame = 0
        self.total_frames = 300
        
    def add_controls(self):
        """Add control buttons to the interface"""
        self.play_button = tk.Button(
            self.control_frame, text="Play", command=self.toggle_animation,
            bg='#333', fg='white', font=('Arial', 10), relief=tk.FLAT
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            self.control_frame, text="Reset", command=self.reset_animation,
            bg='#333', fg='white', font=('Arial', 10), relief=tk.FLAT
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(
            self.control_frame, from_=5, to=100, orient=tk.HORIZONTAL,
            label="Speed", command=self.set_speed, bg='black', fg='white',
            troughcolor='#333', highlightthickness=0
        )
        self.speed_scale.set(20)
        self.speed_scale.pack(side=tk.LEFT, padx=10)
        
    def toggle_animation(self):
        """Toggle animation play/pause"""
        self.is_playing = not self.is_playing
        self.play_button.config(text="Pause" if self.is_playing else "Play")
        
    def reset_animation(self):
        """Reset the animation to beginning"""
        self.current_frame = 0
        self.init_data()
        self.update(0)
        
    def set_speed(self, val):
        """Set animation speed"""
        if hasattr(self, 'ani'):
            self.ani.event_source.interval = 100 - int(val)
        
    def init_data(self):
        """Initialize simulation data"""
        # Cloud formation data - more realistic distribution
        self.cloud_x = np.concatenate([
            np.random.normal(3, 0.8, 40),
            np.random.normal(7, 0.8, 40),
            np.random.normal(5, 1.5, 20)
        ])
        self.cloud_y = np.concatenate([
            np.random.normal(8.5, 0.3, 40),
            np.random.normal(8.2, 0.4, 40),
            np.random.normal(7.8, 0.5, 20)
        ])
        self.cloud_intensities = np.random.rand(100) * 0.7 + 0.3
        
        # Lightning path data
        self.leader_x = [5]
        self.leader_y = [8]
        self.generate_lightning_path()
        
        # Secondary strokes (return strokes)
        self.secondary_paths = self.generate_secondary_strokes()
        
        # Branch data
        self.branch_paths = self.generate_branches()
        
    def generate_lightning_path(self):
        """Generate main lightning path with fractal-like pattern"""
        current_x, current_y = 5, 8
        segments = 50  # Increased for smoother path
        
        for i in range(segments):
            # Vary the step size based on progress
            progress = i / segments
            step_size = 0.2 + (0.5 - 0.2) * (1 - progress)
            
            # Add some randomness but generally move downward
            angle_variation = pi/4 * (1 - progress)  # Less variation as we go down
            angle = -pi/2 + random.uniform(-angle_variation, angle_variation)
            
            dx = step_size * cos(angle)
            dy = step_size * sin(angle)
            
            current_x += dx
            current_y += dy
            
            # Ensure we stay within bounds
            current_x = max(0.5, min(self.plot_width-0.5, current_x))
            current_y = max(0, current_y)
            
            self.leader_x.append(current_x)
            self.leader_y.append(current_y)
            
            # Random chance to create a sharp kink
            if random.random() < 0.1:
                kink_angle = random.uniform(-pi/3, pi/3)
                kink_length = random.uniform(0.1, 0.3)
                self.leader_x.append(current_x + kink_length * cos(angle + kink_angle))
                self.leader_y.append(current_y + kink_length * sin(angle + kink_angle))
                current_x = self.leader_x[-1]
                current_y = self.leader_y[-1]
    
    def generate_secondary_strokes(self):
        """Generate secondary return strokes that follow the main path"""
        paths = []
        for _ in range(3):
            # Select random points along the main path
            start_idx = random.randint(5, len(self.leader_x)-5)
            end_idx = random.randint(start_idx+1, len(self.leader_x)-1)
            
            # Create a path that partially follows the main stroke
            path_x = self.leader_x[start_idx:end_idx]
            path_y = self.leader_y[start_idx:end_idx]
            
            # Add some variation
            path_x = [x + random.uniform(-0.05, 0.05) for x in path_x]
            path_y = [y + random.uniform(-0.05, 0.05) for y in path_y]
            
            paths.append((path_x, path_y))
        return paths
    
    def generate_branches(self):
        """Generate more natural-looking branches"""
        branches = []
        for _ in range(8):
            # Select a random point along the main lightning path
            idx = random.randint(5, len(self.leader_x)-5)
            start_x = self.leader_x[idx]
            start_y = self.leader_y[idx]
            
            # Generate branch path with fractal-like pattern
            branch_x = [start_x]
            branch_y = [start_y]
            
            segments = random.randint(3, 10)
            current_x, current_y = start_x, start_y
            
            for _ in range(segments):
                # Branch generally moves outward from main stroke
                angle = random.uniform(-pi/2, pi/2)
                if current_x < self.leader_x[idx]:
                    angle = random.uniform(-pi/2, 0)
                else:
                    angle = random.uniform(0, pi/2)
                
                step = random.uniform(0.1, 0.3)
                current_x += step * cos(angle)
                current_y += step * sin(angle)
                
                branch_x.append(current_x)
                branch_y.append(current_y)
            
            branches.append((branch_x, branch_y))
        return branches
    
    def update(self, frame):
        """Update the animation frame"""
        self.current_frame = frame
        
        if frame < 60:  # Cloud formation and movement
            size = min(100, frame * 2)
            self.clouds.set_offsets(np.c_[self.cloud_x[:size], self.cloud_y[:size]])
            self.clouds.set_array(self.cloud_intensities[:size])
            
            # Slight movement of clouds
            if frame % 5 == 0:
                self.cloud_x += np.random.normal(0, 0.02, 100)
                self.cloud_y += np.random.normal(0, 0.01, 100)
            
        elif frame < 120:  # Charge separation (clouds pulsing)
            pulse = 0.5 * sin(frame * 0.1) + 0.5
            intensities = self.cloud_intensities * (0.7 + 0.3 * pulse)
            self.clouds.set_array(intensities)
            self.clouds.set_offsets(np.c_[self.cloud_x, self.cloud_y])
            
        elif frame < 180:  # Leader formation
            progress = (frame - 120) / 60
            idx = int(len(self.leader_x) * progress)
            self.leader.set_data(self.leader_x[:idx], self.leader_y[:idx])
            
            # Animate branches with slight delay
            for i, (branch, (bx, by)) in enumerate(zip(self.branches, self.branch_paths)):
                branch_progress = min(1, progress * 1.2 - i*0.1)
                if branch_progress > 0:
                    bidx = int(len(bx) * branch_progress)
                    branch.set_data(bx[:bidx], by[:bidx])
                    branch.set_alpha(0.5 * branch_progress)
            
        elif frame < 240:  # Return stroke and secondary strokes
            main_progress = (frame - 180) / 60
            self.stroke.set_data(self.leader_x, self.leader_y)
            self.stroke.set_alpha(main_progress)
            
            # Secondary strokes with delay
            for i, (stroke, (sx, sy)) in enumerate(zip(self.secondary_strokes, self.secondary_paths)):
                stroke_progress = min(1, max(0, main_progress * 1.5 - i*0.3 - 0.2))
                if stroke_progress > 0:
                    stroke.set_data(sx, sy)
                    stroke.set_alpha(0.7 * stroke_progress)
            
            # Flash effect - more dramatic
            flash_intensity = 0.7 * sin(frame * 5) + 0.3 if frame < 230 else 0
            self.ax.set_facecolor((flash_intensity*0.1, flash_intensity*0.1, flash_intensity*0.2))
            
        else:  # Fade out
            fade_progress = (frame - 240) / 60
            alpha = max(0, 1 - fade_progress)
            self.stroke.set_alpha(alpha)
            for stroke in self.secondary_strokes:
                stroke.set_alpha(max(0, stroke.get_alpha() - 0.02))
            self.ax.set_facecolor('black')
        
        return [self.clouds, self.leader, self.stroke] + self.secondary_strokes + self.branches
    
    def run(self):
        """Run the simulation"""
        # Create the animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update, frames=self.total_frames,
            interval=20, blit=True, repeat=True
        )
        
        # Create canvas and pack it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Bind keyboard events
        self.root.bind('<space>', lambda e: self.toggle_animation())
        self.root.bind('<r>', lambda e: self.reset_animation())
        
        # Run the application
        self.root.mainloop()

if __name__ == "__main__":
    sim = LightningSimulation()
    sim.run()
