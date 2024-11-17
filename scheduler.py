
# scheduler.py test.txt 10 20
# scheduler.py test.txt 10 50
# scheduler.py question2joblist.txt 10 10
# scheduler.py bonusq3joblist.txt 20 30


# Import necessary modules
import sys
from queue import PriorityQueue

# Global clock variable
seconds = 0

# Represents a process in the scheduler
class Process:
    def __init__(self, process_name, priority, arrival_time, time_left, block_interval):
        self.process_name = process_name
        self.priority = int(priority)
        self.arrival_time = int(arrival_time)
        self.time_left = int(time_left)
        self.block_interval = int(block_interval)
        self.block_time = 0
        self.unblock_time = 0
        self.ran_without_blocking = 0
        self.time_till_block = int(block_interval)
        self.end_reason = None

    # String representation for debugging
    def __str__(self):
        return f" Process Name: {self.process_name}\n  Priority: {self.priority}\n  Arrival Time: {self.arrival_time}\n  Time Left: {self.time_left}\n  Block Interval: {self.block_interval}\n  Block Time: {self.block_time}\n  Unblock Time: {self.unblock_time}\n  Ran Without Blocking: {self.ran_without_blocking}\n  Time Till Block: {self.time_till_block}\n  End Reason: {self.end_reason}\n"

    # Comparison method for priority queue ordering
    def __lt__(self, other):
        # prioritize by time of last usage if processes have the same priority
        if self.priority != other.priority:
            return self.priority < other.priority
        if self.block_time != other.block_time:
            return self.block_time < other.block_time


# Manages the three main queues: arrival, ready, and blocked
class Queues:
    def __init__(self, time_slice, block_duration):
        self.time_slice = time_slice
        self.block_duration = block_duration
        self.ready_queue = PriorityQueue()  # For processes ready to run
        self.blocked_queue = PriorityQueue()  # For processes waiting to unblock
        self.arrival_queue = PriorityQueue()  # For processes waiting to arrive
        self.running_process = None
        self.done_list = []  # List of completed processes with turnaround times

    # Determine and set how the current process should run
    def make_running(self, process):
        global seconds

        # Case 1: Process will TERMINATE during this time slice
        # - The process has less time left than both the block interval and time slice.
        if process.time_left <= process.time_till_block and process.time_left <= self.time_slice:
            # Set the time when the process will complete
            process.block_time = seconds + process.time_left
            # Update remaining time to 0, as the process is finishing
            process.time_left = 0
            # Mark the reason for termination as "T" (Terminated)
            process.end_reason = "T"

        # Case 2: Process will BLOCK for I/O before this time slice ends
        # - The process will block sooner than the time slice allows.
        elif process.time_till_block <= self.time_slice and process.time_till_block <= process.time_left:
            # Set the block time to when the process will block
            process.block_time = seconds + process.time_till_block
            # Subtract the time the process ran before blocking from total time left
            process.time_left -= process.time_till_block
            # Mark the reason for termination as "B" (Blocked)
            process.end_reason = "B"
            # Reset the counter for time the process ran without blocking
            process.ran_without_blocking = 0
            # Reset the time until the next block interval
            process.time_till_block = process.block_interval

        # Case 3: Process runs for the FULL TIME SLICE without completing or blocking
        # - Neither blocking nor termination will occur during this time slice.
        elif self.time_slice < process.time_left and self.time_slice < process.time_till_block:
            # Set the block time to the end of the time slice
            process.block_time = seconds + self.time_slice
            # Subtract the full time slice from the total time left
            process.time_left -= self.time_slice
            # Subtract the time slice from the time until the next block interval
            process.time_till_block -= self.time_slice
            # Mark the reason for termination as "P" (Preempted)
            process.end_reason = "P"
            # Increment the counter for time the process ran without blocking
            process.ran_without_blocking += self.time_slice

        # Set the current running process to the one we just updated
        self.running_process = process

    # Add a process to the ready queue, prioritizing higher-priority processes
    def add_to_ready_queue(self, process): 
        self.ready_queue.put((-(process.priority), process))

    # Handle the process at the end of its running interval
    def handle_ending_process(self):
        global seconds

        # If no process is currently running, there's nothing to handle
        if self.running_process is None:
            return

        # Retrieve the reason why the current process ended its interval
        reason = self.running_process.end_reason
        process = self.running_process

        # Case 1: Process has TERMINATED
        if reason == "T":
            # Add the process to the done list with its turnaround time
            self.add_to_done_list(process)

        # Case 2: Process was PREEMPTED (time slice ended)
        elif reason == "P":
            # Add the process back to the ready queue for its priority level
            self.add_to_ready_queue(process)

        # Case 3: Process has BLOCKED for I/O
        elif reason == "B":
            # Calculate the unblock time by adding the block duration
            process.unblock_time = seconds + self.block_duration
            # Add the process to the blocked queue, using unblock time as the priority
            self.blocked_queue.put((process.unblock_time, process))

        # Clear the running process, as its time in the CPU is finished
        self.running_process = None

    # Add a process to the arrival queue
    def add_to_arrival_queue(self, process):
        self.arrival_queue.put((process.arrival_time, process))

    # Add a process to the done list with its turnaround time
    def add_to_done_list(self, process):
        self.done_list.append((process, seconds - process.arrival_time))

    # Debugging: Print the state of all queues and the running process
    def print_all_queues(self):
        print("Running Process:\n", self.running_process)
        print("Ready Queue:")
        for i in range(self.ready_queue.qsize()):
            print(self.ready_queue.queue[i][1])
        print("Blocked Queue:")
        for i in range(self.blocked_queue.qsize()):
            print(self.blocked_queue.queue[i][1])
        print("Arrival Queue:")
        for i in range(self.arrival_queue.qsize()):
            print(self.arrival_queue.queue[i][1])
        print("")


# Read and parse the input file to create Process objects
def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    returned_lines = []
    for line in lines:
        if line[0] != "#":  # Ignore comment lines
            line = line.strip().split(" ")
            returned_lines.append(Process(line[0], line[1], line[2], line[3], line[4]))
    return returned_lines


# Main simulation loop
def main():
    global seconds 

    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python3 scheduler.py <joblist_file> <time_slice> <block_duration>")
        sys.exit(1)

    # Retrieve arguments from the command line
    joblist_file = "project3/" + sys.argv[1]
    time_slice = int(sys.argv[2])  
    block_duration = int(sys.argv[3])  

    # Initialize queues and parse input file
    output = f"timeSlice: {time_slice}     blockDuration: {block_duration}\n"
    queues = Queues(time_slice, block_duration)

    try:
        jobs = readFile(joblist_file)
    except FileNotFoundError:
        print(f"Error: File '{joblist_file}' not found.")
        sys.exit(1)

    # Add processes to the arrival queue
    for job in jobs:
        queues.add_to_arrival_queue(job)
    job_number = len(jobs)    

    # Simulation variables
    was_idle = False
    idle_seconds = 0

    # Main simulation loop runs until all processes are complete
    while len(queues.done_list) < job_number:
        
        # Handle process transitions at the end of its interval
        if queues.running_process is None or queues.running_process.block_time == seconds:

            # Add newly arrived processes to the ready queue
            while queues.arrival_queue.qsize() > 0 and queues.arrival_queue.queue[0][1].arrival_time <= seconds:
                arrival_time, process = queues.arrival_queue.get()
                queues.add_to_ready_queue(process)

            # Move blocked processes back to the ready queue if unblocked
            if queues.blocked_queue.qsize() > 0 and queues.blocked_queue.queue[0][1].unblock_time <= seconds:
                priority, process = queues.blocked_queue.get()
                queues.add_to_ready_queue(process)
            
            # Handle the running process and move it to the appropriate queue
            queues.handle_ending_process() 

            # Handle idle time if no process is ready
            if queues.ready_queue.qsize() == 0:
                was_idle = True
                idle_seconds += 1
            else:
                # Process is ready to run
                if was_idle:
                    output += f"{seconds - idle_seconds}\tidle\t{idle_seconds}\tI\n"
                    idle_seconds = 0
                    was_idle = False
                priority, process = queues.ready_queue.get()
                queues.make_running(process)
                output += f"{seconds}\t{queues.running_process.process_name}\t{queues.running_process.block_time - seconds}\t{queues.running_process.end_reason}\n"
        seconds += 1  # Increment global time
        
    # Output simulation results
    print(output)   
    total_time = 0
    for process, time in queues.done_list:
        total_time += time
        print(f"{process.process_name} {time}")
    print(f"Average turnaround time: {total_time / job_number}")


# Entry point
if __name__ == "__main__":
    main()


# /opt/homebrew/bin/python3 "/Users/kragenwild/Documents/CODING/Junior Year/Quarter 1/Systems 2/project3/scheduler.py" test.txt 10 20
# /opt/homebrew/bin/python3 "/Users/kragenwild/Documents/CODING/Junior Year/Quarter 1/Systems 2/project3/scheduler.py" test.txt 10 50
# /opt/homebrew/bin/python3 "/Users/kragenwild/Documents/CODING/Junior Year/Quarter 1/Systems 2/project3/scheduler.py" question2joblist.txt 10 10
# /opt/homebrew/bin/python3 "/Users/kragenwild/Documents/CODING/Junior Year/Quarter 1/Systems 2/project3/scheduler.py" bonusq3joblist.txt 20 30

