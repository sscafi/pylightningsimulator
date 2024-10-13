import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Create the main window
root = tk.Tk()
root.title("Lightning Formation Simulation")

# Create a figure for the animation
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Lightning Formation Simulation")

# Create a scatter object to represent the cumulonimbus clouds
clouds, = ax.plot([], [], 'bo')

# Create a line object to represent the leader
leader, = ax.plot([], [], 'b-', lw=2)

# Create a line object to represent the return stroke
stroke, = ax.plot([], [], 'r-', lw=2)

# Create a scatter object to represent the strike point
strike, = ax.plot([], [], 'ro')

# Initialize the data for the animation
cloud_x = np.random.rand(100) * 10
cloud_y = np.random.rand(100) * 10
leader_x = []
leader_y = []
stroke_x = []
stroke_y = []
strike_x = [5]
strike_y = [0]

# Function to update the animation
def update(frame):
    global leader_x, leader_y, stroke_x, stroke_y
    if frame < 50:  # Cumulonimbus clouds
        clouds.set_data(cloud_x, cloud_y)
    elif frame < 100:  # Separation of electrical charges
        clouds.set_data(cloud_x, cloud_y)
        leader_x.append(frame / 10)
        leader_y.append(10 - frame / 10)
        leader.set_data(leader_x, leader_y)
    elif frame < 150:  # Formation of a leader
        leader.set_data(leader_x, leader_y)
    elif frame < 200:  # Return stroke
        stroke_x.append(frame / 10)
        stroke_y.append(10 - frame / 10)
        stroke.set_data(stroke_x, stroke_y)
    else:  # Strike
        stroke.set_data(stroke_x, stroke_y)
        strike.set_data(strike_x, strike_y)
    return clouds, leader, stroke, strike

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=250, blit=True)

# Create a canvas to display the animation
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Draw the animation on the canvas
fig_canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
fig_canvas.draw()
fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Run the application
tk.mainloop()