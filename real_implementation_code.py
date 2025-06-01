import numpy as np

def simulate_covert_channel(distribution='uniform', m=16, i=10, B=20, iteration=500):
    underflow_count = 0
    overflow_count = 0
    success_count = 0

    for _ in range(iteration):
        buffer_size = 0
        buffer_limit = B

        bits = np.random.randint(0, 2, m) # not using the previous random_message_bits is because the size aren't the same

        # delays if distribution
        if distribution == 'uniform':
            delay = np.random.uniform(0, 1, m * 10)
        elif distribution == 'exponential':
            delay = np.random.exponential(1, m * 10)
        
        arrival_times = np.cumsum(delay) # IPD

        # setting up the current time 
        arrival_index = 0
        current_time = 0
        while buffer_size < i and arrival_index < len(arrival_times):
            if arrival_times[arrival_index] <= current_time:
                buffer_size += 1
                arrival_index += 1
            else:
                current_time = arrival_times[arrival_index]


        failed = False
        for bit in bits:
            # delay if bit if distribution
            if distribution == 'uniform':
                if bit == 0:
                    delay = np.random.uniform(0, 0.5)
                else:
                    delay = np.random.uniform(0.5, 1.0)
            else: #if distribution == 'exponential'
                if bit == 0:
                    delay = np.random.uniform(0, np.log(2))
                else:
                    delay = np.random.uniform(np.log(2), 5)

            current_time += delay

            # when new package comes in
            while arrival_index < len(arrival_times) and arrival_times[arrival_index] <= current_time:
                # if there are packages left         and are within the current time
                if buffer_size < buffer_limit: # if buffer is still enough
                    buffer_size += 1
                    arrival_index += 1
                else:                          # buffer is not enough, we are having more input than reserved
                    failed = True              # overflow
                    overflow_count += 1
                    break
            if failed:
                break

            # Transmit a packet
            if buffer_size > 0:                # tansmit a packet, or we have to have at least one buffer to tansimit a packet
                buffer_size -= 1
            else:                              # if we don't
                failed = True                  # underflow
                underflow_count += 1
                break

        if not failed:
            success_count += 1


    print(f"Results after {iteration} iterations:")
    print(f"Underflow Probability: {underflow_count / iteration:.3f}")
    print(f"Overflow Probability: {overflow_count / iteration:.3f}")
    print(f"Success Probability: {success_count / iteration:.3f}")

if __name__ == '__main__':
    dist = input("Choose distribution (uniform or exponential): ").strip().lower()
    if dist not in ['uniform', 'exponential']:
        raise ValueError("Wrong distribution name. ")
    m = int(input("Enter size of the secret message (16 or 32): "))
    if m not in [16, 32]:
        raise ValueError("Wrong message size.")
    i = int(input("Enter initial buffer size i (2,6,10,14,18): "))
    if i > 20:
        raise ValueError("Wrong buffer size.")

    simulate_covert_channel(distribution=dist, m=m, i=i)
