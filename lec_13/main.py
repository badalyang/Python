import os
import re
import time
from collections import defaultdict
from threading import Thread, Lock
from multiprocessing import Process, Manager

def generate_test_file(file_name, file_size_mb):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    with open(file_name, "w") as file:
        for _ in range(file_size_mb * 1024 * 1024 // 50): 
            file.write(" ".join(words) + ". " * 10 + "\n")

def count_words_sequentially(file_name):
    word_frequency = defaultdict(int)
    with open(file_name, "r") as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line.lower())
            for word in words:
                word_frequency[word] += 1
    return word_frequency

def count_words_with_threads(file_name):
    def thread_worker(chunk_lines, lock, shared_word_count):
        local_word_count = defaultdict(int)
        for line in chunk_lines:
            words = re.findall(r'\b\w+\b', line.lower())
            for word in words:
                local_word_count[word] += 1
        with lock:
            for word, count in local_word_count.items():
                shared_word_count[word] += count

    word_count = defaultdict(int)
    thread_lock = Lock()
    threads = []
    with open(file_name, "r") as file:
        all_lines = file.readlines()
        chunk_size = len(all_lines) // os.cpu_count()
        for start_index in range(0, len(all_lines), chunk_size):
            thread = Thread(target=thread_worker, args=(all_lines[start_index:start_index + chunk_size], thread_lock, word_count))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    return word_count

def count_words_with_processes(file_name):
    def process_worker(chunk_lines, shared_word_count):
        local_word_count = defaultdict(int)
        for line in chunk_lines:
            words = re.findall(r'\b\w+\b', line.lower())
            for word in words:
                local_word_count[word] += 1
        for word, count in local_word_count.items():
            shared_word_count[word] += count

    manager = Manager()
    word_count = manager.dict()
    processes = []
    with open(file_name, "r") as file:
        all_lines = file.readlines()
        chunk_size = len(all_lines) // os.cpu_count()
        for start_index in range(0, len(all_lines), chunk_size):
            process = Process(target=process_worker, args=(all_lines[start_index:start_index + chunk_size], word_count))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
    return dict(word_count)
def compare_execution_times(file_name):
    print("Comparing execution times...")

    start_time = time.time()
    count_words_sequentially(file_name)
    sequential_time = time.time() - start_time
    print(f"Sequential execution time: {sequential_time:.2f} seconds")


    start_time = time.time()
    count_words_with_threads(file_name)
    threading_time = time.time() - start_time
    print(f"Multithreading execution time: {threading_time:.2f} seconds")

    start_time = time.time()
    count_words_with_processes(file_name)
    processing_time = time.time() - start_time
    print(f"Multiprocessing execution time: {processing_time:.2f} seconds")

    print(f"Multithreading speedup: {sequential_time / threading_time:.2f}")
    print(f"Multiprocessing speedup: {sequential_time / processing_time:.2f}")

if __name__ == "__main__":
    test_file_name = "large_text_file.txt"
    generate_test_file(test_file_name, file_size_mb=10) 
    compare_execution_times(test_file_name)
    os.remove(test_file_name)
