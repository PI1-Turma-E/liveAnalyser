import socket
import datetime
import numpy as np
import matplotlib.pyplot as plt

sniffed_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

data_size = []
data_size.append(0)
operator = 0

current_second = datetime.datetime.now().second

while True:
    try:
        packet = sniffed_socket.recvfrom(8081)[0]

        if datetime.datetime.now().second == current_second:
            data_size[operator] += len(packet)
        else:
            current_second = datetime.datetime.now().second
            operator += 1
            data_size.append(0)

    except KeyboardInterrupt:
        break

result_file = open('analysis_result.txt', 'w')

for index, each in enumerate(data_size):
    result_file.write(str(index) + ': ' + str(each) + ' bytes' + '\n')

result_file.write('\nAverage: ' + str(sum(data_size)/len(data_size)) + 'bytes/sec\n')

result_file.close()

X = np.linspace(1, len(data_size), len(data_size))

plt.plot(X, data_size)
plt.savefig('analysis_result.png')

print("\nAnalysis finished!\n")
