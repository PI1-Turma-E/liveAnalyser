import socket
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Creates socket object
sniffed_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

# Initializes data vectors
image_data = [0]
control_data = [0]

# Auxiliar operator
operator = 0

# Sets initial time
current_second = datetime.datetime.now().second

# Captures packets
while True:
    try:
        # Sniffes Image server and Control server ports
        image_packet = sniffed_socket.recvfrom(8081)[0]
        control_packet = sniffed_socket.recvfrom(8080)[0]

        # If it is still the same second, adds collected data to the current data slot
        if datetime.datetime.now().second == current_second:
            image_data[operator] += len(image_packet)
            control_data[operator] += len(control_data)
        else:
            # Updates the current second and appends a new empty data slot
            current_second = datetime.datetime.now().second
            operator += 1
            image_data.append(0)
            control_data.append(0)

    except KeyboardInterrupt:
        break

## Results

# Creates file to show Image data results
image_result_file = open('image_data_result.txt', 'w')
image_data = np.array(image_data)/1000 # Bytes to Kilobytes conversion

for index, each in enumerate(image_data):
    image_result_file.write('Time: ' + str(index) + 's - Data: ' + str(each) + ' Kb' + '\n')

image_result_file.write('\nAverage: ' + str(sum(image_data)/len(image_data)) + ' kbps\n')
image_result_file.close()

# Creates file to show Control data results
control_result_file = open('control_data_result.txt', 'w')
control_data = np.array(control_data)/1000 # Bytes to Kilobytes conversion

for index, each in enumerate(control_data):
    control_result_file.write('Time: ' + str(index) + 's - Data: ' + str(each) + ' Kb' + '\n')

control_result_file.write('\nAverage: ' + str(sum(control_data)/len(control_data)) + ' kbps\n')
control_result_file.close()

# Creates file to show Total data results
total_result_file = open('total_data_result.txt', 'w')

for index, each in enumerate(control_data+image_data):
    total_result_file.write('Time: ' + str(index) + 's - Data: ' + str(each) + ' Kb' + '\n')

total_result_file.write('\nAverage: ' + str(sum(control_data+image_data)/len(control_data)) + ' kbps\n')
total_result_file.close()

## Graph plotting

# Generates linspace based on how much time was spent on the analysis
X = np.linspace(1, len(image_data), len(image_data))

# Plots data
plt.plot(X, image_data, 'r', label='Image data')
plt.plot(X, control_data, 'b', label='Control data')
plt.plot(X, image_data+control_data, 'k', label='Total data')

# Labels the graph
plt.ylabel('data quantity (kilobytes)')
plt.xlabel('time elapsed (seconds)')

# Enable label showing
plt.legend()

# Adjusts content to the frame so nothing gets cropped
plt.tight_layout()

# Saves graph to file
plt.savefig('analysis_result.png')

print("\nAnalysis finished!\n")
