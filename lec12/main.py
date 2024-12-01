import random
import time

def add_nums(name):
    file_w = open(name, "w")
    for line in range(100):
        for number in range(20):
            file_w.write(str(random.randint(0, 100)))
            file_w.write(" ")
        file_w.write("\n")
    file_w.close()

def int_arr(name):
    file_r = open(name, 'r')
    lines = file_r.readlines()
    file_r.close()
    file_w = open(name, 'w')
    for line in lines:
        arr = list(map(int, line.strip().split()))
        filtered_arr = list(filter(lambda x: x > 40, arr))
        print(filtered_arr)
        file_w.write(" ".join(map(str, filtered_arr)) + "\n")
    file_w.close()

def read_file_with_yield(name):
    with open(name, 'r') as file_r:
        for line in file_r:
            yield line.strip()
print("Reading with YEILD\n")
for line in read_file_with_yield("111.txt"):
    print(line)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
        return result
    return wrapper

@measure_time
def decorated_int_arr(name):
    int_arr(name)
    
int_arr("111.txt")

add_nums("111.txt")
