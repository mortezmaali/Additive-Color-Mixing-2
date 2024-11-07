import cv2
import numpy as np
import tkinter as tk
import random

# Get the screen size using tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Define the size of the image and stripes
height, width = screen_height, screen_width
stripe_width = width // 6  # Keeping the original stripe size
stripe_height = height // 3  # Keeping the original height

# Initialize the positions, directions, and angles of the stripes
stripes = []
colors = ["green", "red", "blue"]

for color in colors:
    for _ in range(5):  # Create 5 stripes for each color
        stripe = {
            "color": color,
            "x": random.randint(0, width - stripe_width),
            "y": random.randint(0, height - stripe_height),
            "dx": random.choice([-2, 2]),
            "dy": random.choice([-2, 2]),
            "angle": random.randint(0, 360)
        }
        stripes.append(stripe)

# Create a window to display the image in full screen
cv2.namedWindow('Stripes Animation', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Stripes Animation', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Create an empty image
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw each stripe with rotation
    for stripe in stripes:
        x, y, angle = stripe["x"], stripe["y"], stripe["angle"]
        color = stripe["color"]
        stripe_image = np.zeros((stripe_height, stripe_width, 3), dtype=np.uint8)

        if color == "green":
            stripe_image[:] = [0, 255, 0]
        elif color == "red":
            stripe_image[:] = [0, 0, 255]
        elif color == "blue":
            stripe_image[:] = [255, 0, 0]

        # Rotate the stripe
        rotation_matrix = cv2.getRotationMatrix2D((stripe_width // 2, stripe_height // 2), angle, 1)
        rotated_stripe = cv2.warpAffine(stripe_image, rotation_matrix, (stripe_width, stripe_height))

        # Calculate the region where the stripe will be drawn
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + stripe_width, width), min(y + stripe_height, height)

        # Calculate the corresponding region of the rotated stripe
        stripe_x1, stripe_y1 = x1 - x, y1 - y
        stripe_x2, stripe_y2 = stripe_x1 + (x2 - x1), stripe_y1 + (y2 - y1)

        # Ensure sizes match and overlay the rotated stripe
        image[y1:y2, x1:x2] = cv2.addWeighted(image[y1:y2, x1:x2], 1.0, rotated_stripe[stripe_y1:stripe_y2, stripe_x1:stripe_x2], 1.0, 0)

        # Update positions and angle
        stripe["x"] += stripe["dx"]
        stripe["y"] += stripe["dy"]
        stripe["angle"] += 2  # Increment angle for rotation

        # Bounce off the edges
        if stripe["x"] <= 0 or stripe["x"] >= width - stripe_width:
            stripe["dx"] = -stripe["dx"]
        if stripe["y"] <= 0 or stripe["y"] >= height - stripe_height:
            stripe["dy"] = -stripe["dy"]

    # Display the image
    cv2.imshow('Stripes Animation', image)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release resources and close the window
cv2.destroyAllWindows()
