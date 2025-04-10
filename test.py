import concurrent.futures
import time
import random

def worker_process(process_id):
    """Simulates a process that takes a random amount of time to complete."""
    duration = random.uniform(1, 5)  # Random duration between 1 and 5 seconds
    print(f"Process {process_id} started, will take {duration:.2f} seconds")
    time.sleep(duration)  # Simulate work
    print(f"Process {process_id} is working...")
    time.sleep(duration)  # More simulated work
    result = f"Result from process {process_id}"
    print(f"Process {process_id} completed after {duration*2:.2f} seconds")
    return result

def main():
    # Number of processes to start
    num_processes = 5  # Change this to your desired number

    # Create a ProcessPoolExecutor to manage processes
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Start all processes and store their future objects
        future_to_id = {executor.submit(worker_process, i): i for i in range(num_processes)}
        
        print(f"Started {num_processes} processes")
        
        # Process results as they complete (in completion order)
        for future in concurrent.futures.as_completed(future_to_id):
            process_id = future_to_id[future]
            try:
                result = future.result()
                print(f"Received: {result}")
            except Exception as e:
                print(f"Process {process_id} generated an exception: {e}")

if __name__ == "__main__":
    main()