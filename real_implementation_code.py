import numpy as np

# Getting the user input
distribution = input("Choose distribution (uniform or exponential): ").strip().lower()
if distribution not in ['uniform', 'exponential']:
    raise ValueError("Wrong distribution name. ")
message_size = int(input("Enter size of the secret message (16 or 32): "))
if message_size not in [16, 32]:
    raise ValueError("Wrong message size.")
i = int(input("Enter initial buffer size i (2,6,10,14,18): "))
if i > 20:
    raise ValueError("Wrong buffer size.")

m = message_size
dist = distribution
underflow_count = 0
overflow_count = 0
success_count = 0
# i = i
# iteration = 500 # iterate 500 times
for iteration in range(500):
    bits = np.random.choice([0, 1], size=m)
    sent_time = []
    for x in range(m):
        if dist == 'uniform':
            sent_time.append(np.random.uniform(0, 1))
        elif dist == 'exponential':
            temp = np.random.exponential(1)
            while temp > 5:
                temp = np.random.exponential(1)
            sent_time.append(temp)

    sent_times = np.cumsum(sent_time)

    actual_time = []
    for bit in bits:
        if dist == 'uniform':
            if bit == 0:
                time = np.random.uniform(0, 0.5)
            else:
                time = np.random.uniform(0.5, 1)
        elif dist == 'exponential':
            if bit == 0:
                time = -np.log(1 - np.random.uniform(0, 0.5))
            else:
                time = -np.log(1 - np.random.uniform(0.5, 1))

        actual_time.append(time)
    actual_times = np.cumsum(actual_time)

    buffer_size = 20
    buffer = 0
    sent_index = 0
    actual_index = 0

    fail = False
    while sent_index < m or actual_index < m:
        if actual_index < m and actual_times[actual_index] <= sent_times[sent_index]:
            if buffer < buffer_size:
                buffer += 1
            else:
                overflow_count += 1
                fail = True
                break
            actual_index += 1
            
        else:
            if buffer > 0:
                buffer -= 1
            else:
                underflow_count += 1
                fail = True
                break
            sent_index += 1
        
    if fail == False:
        success_count += 1


underflow_rate = underflow_count / 500
overflow_rate = overflow_count / 500
success_rate = success_count / 500
print(f"{dist} {m} {i} {underflow_rate} {overflow_rate} {success_rate}")