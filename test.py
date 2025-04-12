#!/usr/bin/env python3
"""
This script demonstrates how to run Python code with root privileges
and includes various tracing methods.
"""
import os
import sys
import subprocess
import logging
import traceback
import time
import tempfile
from datetime import datetime

# Set up logging
log_file = '/var/log/root_script.log'  # Requires root to write here
temp_log = os.path.join(tempfile.gettempdir(), 'root_script.log')  # Fallback location

def setup_logging():
    """Configure logging based on current privileges."""
    try:
        # Try to log to system location (requires root)
        logging.basicConfig(
            filename=log_file if check_root() else temp_log,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info(f"Logging initialized. UID: {os.geteuid()}, PID: {os.getpid()}")
    except PermissionError:
        # Fallback to temporary directory
        logging.basicConfig(
            filename=temp_log,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info(f"Logging initialized in temp directory. UID: {os.geteuid()}, PID: {os.getpid()}")

def check_root():
    """Check if the script is running with root privileges."""
    return os.geteuid() == 0

def trace_function(frame, event, arg):
    """Trace function for sys.settrace()."""
    if event == 'line':
        # Get file name and line number
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        
        # Only trace our own script, not library code
        if __file__ in filename:
            function_name = frame.f_code.co_name
            line = linecache.getline(filename, lineno).strip()
            logging.debug(f"TRACE: {function_name}:{lineno} - {line}")
    
    return trace_function

def enable_detailed_tracing():
    """Enable detailed function and line tracing."""
    import linecache  # Import here to avoid unnecessary import if not used
    sys.settrace(trace_function)
    logging.info("Detailed tracing enabled")

def run_with_root():
    """Function that contains code to be executed with root privileges."""
    logging.info("Starting root operations")
    print("Running with root privileges!")
    print(f"Effective user ID: {os.geteuid()}")
    
    # Record system info for tracing
    logging.info(f"System info - Python: {sys.version}")
    logging.info(f"Current directory: {os.getcwd()}")
    logging.info(f"Script path: {os.path.abspath(__file__)}")
    
    # Example of operations that typically require root privileges
    try:
        logging.debug("Attempting to write to system directory")
        
        # For demonstration only - this would write to a system directory
        with open('/etc/example_root_file.txt', 'w') as f:
            f.write(f'This file was created with root privileges at {datetime.now()}.\n')
        
        logging.info("Successfully wrote to /etc/example_root_file.txt")
        print("Successfully wrote to /etc/example_root_file.txt")
        
        # Example of reading a system file
        logging.debug("Attempting to read a system file")
        with open('/etc/passwd', 'r') as f:
            first_line = f.readline().strip()
        logging.info(f"First line of /etc/passwd: {first_line}")
        
    except Exception as e:
        logging.error(f"Error during root operations: {e}")
        logging.error(traceback.format_exc())
        print(f"An error occurred: {e}")
    
    logging.info("Root operations completed")

def main():
    """Main function that handles privilege escalation if needed."""
    # Initialize logging first thing
    setup_logging()
    
    # Log script start
    logging.info("=" * 50)
    logging.info(f"Script started at {datetime.now()}")
    logging.info(f"Arguments: {sys.argv}")
    
    # Check for trace flag in arguments
    enable_tracing = '--trace' in sys.argv
    if enable_tracing and '--trace' in sys.argv:
        sys.argv.remove('--trace')  # Remove from args before potential sudo relaunch
    
    if check_root():
        # Already running as root
        logging.info("Script running with root privileges")
        
        if enable_tracing:
            enable_detailed_tracing()
            
        run_with_root()
    else:
        logging.info("Script running without root privileges, attempting elevation")
        print("This script requires root privileges.")
        print("Attempting to restart with sudo...")
        
        try:
            # Re-run the script with sudo, preserving trace flag if set
            sudo_command = ['sudo', sys.executable] + sys.argv
            if enable_tracing:
                sudo_command.append('--trace')
                
            logging.info(f"Executing: {' '.join(sudo_command)}")
            subprocess.run(sudo_command, check=True)
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to run with elevated privileges: {e}")
            print("Failed to run with elevated privileges.")
            sys.exit(1)
    
    # Log script end
    logging.info(f"Script finished at {datetime.now()}")
    logging.info("=" * 50)
    
    # Print log locations for user reference
    if check_root():
        print(f"\nTrace and debug information has been logged to: {log_file}")
    else:
        print(f"\nTrace and debug information has been logged to: {temp_log}")

if __name__ == "__main__":
    main()