import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
GRAVITY = 2
JUMP_STRENGTH = -20
MOVE_SPEED = 10
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
NUM_PLATFORMS = 5

# Create the main application window
root = tk.Tk()
root.title("Advanced Platformer")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# Load background image
try:
    background_image = tk.PhotoImage(file="background.png")
    canvas.create_image(0, 0, anchor="nw", image=background_image)
except tk.TclError:
    print("Background image not found. Continuing without it.")

# Create the ground
ground = canvas.create_rectangle(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, WINDOW_HEIGHT, fill="green")

# Create platforms
platforms = []
for _ in range(NUM_PLATFORMS):
    x1 = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)
    y1 = random.randint(100, WINDOW_HEIGHT - 100)
    x2 = x1 + PLATFORM_WIDTH
    y2 = y1 + PLATFORM_HEIGHT
    platforms.append(canvas.create_rectangle(x1, y1, x2, y2, fill="brown"))

# Create the player
player = canvas.create_rectangle(50, WINDOW_HEIGHT - 100, 50 + PLAYER_SIZE, WINDOW_HEIGHT - 100 + PLAYER_SIZE, fill="red")

# Player movement variables
player_velocity_y = 0
player_on_ground = False
score = 0

def move_left(event):
    canvas.move(player, -MOVE_SPEED, 0)

def move_right(event):
    canvas.move(player, MOVE_SPEED, 0)

def jump(event):
    global player_velocity_y, player_on_ground
    if player_on_ground:
        player_velocity_y = JUMP_STRENGTH
        player_on_ground = False

def check_collision_with_platforms(player_coords):
    for platform in platforms:
        platform_coords = canvas.coords(platform)
        if (player_coords[2] > platform_coords[0] and player_coords[0] < platform_coords[2] and
            player_coords[3] >= platform_coords[1] and player_coords[3] <= platform_coords[3]):
            return platform_coords[1]
    return None

def update():
    global player_velocity_y, player_on_ground, score

    # Apply gravity
    player_velocity_y += GRAVITY
    canvas.move(player, 0, player_velocity_y)

    # Check for collision with the ground
    player_coords = canvas.coords(player)
    if player_coords[3] >= WINDOW_HEIGHT - 50:
        canvas.coords(player, player_coords[0], WINDOW_HEIGHT - 50 - PLAYER_SIZE, player_coords[2], WINDOW_HEIGHT - 50)
        player_velocity_y = 0
        player_on_ground = True
    else:
        player_on_ground = False

    # Check for collision with platforms
    platform_y = check_collision_with_platforms(player_coords)
    if platform_y is not None:
        canvas.coords(player, player_coords[0], platform_y - PLAYER_SIZE, player_coords[2], platform_y)
        player_velocity_y = 0
        player_on_ground = True
        score += 1

    # Update the score display
    canvas.itemconfig(score_text, text=f"Score: {score}")

    # Schedule the next update
    root.after(50, update)

# Create a score display
score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 16), fill="white")

# Bind keys to player movement
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", jump)

# Start the game loop
update()
root.mainloop()