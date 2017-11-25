import socket
import datetime
import numpy as np
import matplotlib.pyplot as plt

sniffed_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

image_data = [0]
control_data = [0]

operator = 0

current_second = datetime.datetime.now().second

while True:
    try:
        image_packet = sniffed_socket.recvfrom(8081)[0]
        control_packet = sniffed_socket.recvfrom(8080)[0]

        if datetime.datetime.now().second == current_second:
            image_data[operator] += len(image_packet)
            control_data[operator] += len(control_data)
        else:
            current_second = datetime.datetime.now().second
            operator += 1
            image_data.append(0)
            control_data.append(0)

    except KeyboardInterrupt:
        break

image_result_file = open('image_data_result.txt', 'w')
image_data = np.array(image_data)/1000

for index, each in enumerate(image_data):
    image_result_file.write('Time: ' + str(index) + 's - Data: ' + str(each) + ' Kb' + '\n')

image_result_file.write('\nAverage: ' + str(sum(image_data)/len(image_data)) + ' kbps\n')

control_result_file = open('control_data_result.txt', 'w')
control_data = np.array(control_data)/1000

for index, each in enumerate(control_data):
    control_result_file.write('Time: ' + str(index) + 's - Data: ' + str(each) + ' Kb' + '\n')

control_result_file.write('\nAverage: ' + str(sum(control_data)/len(control_data)) + ' kbps\n')

image_result_file.close()
control_result_file.close()

X = np.linspace(1, len(image_data), len(image_data))

plt.plot(X, image_data, 'r', label='Image data')
plt.plot(X, control_data, 'b', label='Control data')

plt.ylabel('data quantity (kilobytes)')
plt.xlabel('time elapsed (seconds)')

plt.legend()

plt.tight_layout()

plt.savefig('analysis_result.png')

print("\nAnalysis finished!\n")
