import numpy as np
import cv2


width = 1700
height = 700

num_frames = 150
velocity = 1  

num_objects = 4

centers = np.zeros((num_objects, num_frames, 2)) 

for j in range(num_objects):
    start_x = np.random.randint(0, width)  
    start_y = np.random.randint(0, height)  
        
    x_route = np.linspace(start_x, np.random.randint(0, width), num_frames)  
    y_route = np.linspace(start_y, np.random.randint(0, height), num_frames) 
    
    for i in range(num_frames):
        x = x_route[i] 
        y = y_route[i]  
        
        centers[j, i, 0] = x
        centers[j, i, 1] = y


np.save('centers.npy', centers)
print(centers)

with open('centers.txt', 'w') as file:
    for j in range(num_objects):
        tracked_route = []
        for i in range(num_frames):
            x = centers[j, i, 0]
            y = centers[j, i, 1]
            tracked_route.append((x, y))
        tracked_route_str = ', '.join([f'({x}, {y})' for x, y in tracked_route])
        file.write(tracked_route_str)
        file.write('\n')



