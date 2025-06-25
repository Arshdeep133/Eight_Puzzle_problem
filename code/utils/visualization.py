import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.widgets import Button

def visualize_puzzle_solution(solution_path):
    """Visualizes and animates the solution path for the puzzle.

    Args:
        solution_path (list): A list of 2D lists representing the puzzle states.
    """
    # Define the color map for the blocks
    colors = list(mcolors.TABLEAU_COLORS.values())
    puzzle_array = np.array(solution_path[0])  # Initial state
    n, m = puzzle_array.shape

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, m)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw the initial grid
    patches = []
    for i in range(n):
        for j in range(m):
            value = puzzle_array[i][j]
            color = colors[value % len(colors)] if value != 0 else "white"
            rect = plt.Rectangle((j, n - i - 1), 1, 1, facecolor=color, edgecolor="black")
            ax.add_patch(rect)
            if value != 0:
                text = ax.text(j + 0.5, n - i - 0.5, str(value), va='center', ha='center', fontsize=16, color='black')
            else:
                text = ax.text(j + 0.5, n - i - 0.5, "", va='center', ha='center', fontsize=16, color='black')
            patches.append((rect, text))

    is_paused = False
    current_frame = [0]
    
    def update(frame):
        """Updates the grid for each frame in the animation."""
        puzzle_array = np.array(solution_path[frame])
        for i in range(n):
            for j in range(m):
                value = puzzle_array[i][j]
                rect, text = patches[i * m + j]
                rect.set_facecolor(colors[value % len(colors)] if value != 0 else "white")
                text.set_text(str(value) if value != 0 else "")

    def toggle_animation(event):
        """Toggles the animation between pause and play."""
        nonlocal is_paused
        if is_paused:
            ani.event_source.start()
            btn.label.set_text("Pause")
        else:
            ani.event_source.stop()
            btn.label.set_text("Play")
        is_paused = not is_paused
    
    def step_forward(event):
        """Moves forward by one step."""
        if current_frame[0] < len(solution_path) - 1:
            current_frame[0] += 1
            update(current_frame[0])
            fig.canvas.draw_idle()

    def step_backward(event):
        """Moves backward by one step."""
        if current_frame[0] > 0:
            current_frame[0] -= 1
            update(current_frame[0])
            fig.canvas.draw_idle()

    # Button to pause/resume the animation
    ax_button = plt.axes([0.4, 0.01, 0.2, 0.075])
    btn = Button(ax_button, "Pause", color="lightblue", hovercolor="blue")
    btn.on_clicked(toggle_animation)
    
    ax_forward = plt.axes([0.65, 0.01, 0.1, 0.075])
    btn_forward = Button(ax_forward, "Next", color="lightgreen", hovercolor="green")
    btn_forward.on_clicked(step_forward)

    ax_backward = plt.axes([0.25, 0.01, 0.1, 0.075])
    btn_backward = Button(ax_backward, "Prev", color="lightcoral", hovercolor="red")
    btn_backward.on_clicked(step_backward)

    def animate(frame):
        """Manual animation update. Only update if not paused."""
        if not is_paused:
            update(frame)

    # FuncAnimation setup
    ani = animation.FuncAnimation(fig, animate, frames=len(solution_path), interval=1000, repeat=False, blit=False)

    plt.show()