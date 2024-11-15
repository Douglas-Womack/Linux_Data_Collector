import os
import subprocess
import shutil
import datetime

# Function to collect system configurations
def collect_system_configurations(output_dir):
    """
    Collects system configurations and writes them to a file.
    """
    output_file = os.path.join(output_dir, "collected_data", "system_configurations.txt")
    with open(output_file, "w") as f:
        # Collect basic system information
        f.write("Date and Time: {}\n".format(datetime.datetime.now()))
        f.write("Hostname: {}\n".format(os.environ.get('COMPUTERNAME') or os.uname().nodename))
        f.write("Operating System: {}\n".format(os.environ.get('OS') or os.uname().sysname))
        f.write("Architecture: {}\n".format(os.environ.get('PROCESSOR_ARCHITECTURE') or os.uname().machine))
        
        # Additional system information
        try:
            # CPU information
            cpu_info = subprocess.check_output(['lscpu']).decode()
            f.write("\nCPU Information:\n")
            f.write(cpu_info)
            
            # Memory information
            mem_info = subprocess.check_output(['free', '-h']).decode()
            f.write("\nMemory Information:\n")
            f.write(mem_info)
            
            # Disk usage
            disk_usage = subprocess.check_output(['df', '-h']).decode()
            f.write("\nDisk Usage:\n")
            f.write(disk_usage)
            
            # Installed packages (Linux only)
            if os.name != 'nt':
                installed_packages = subprocess.check_output(['dpkg', '-l']).decode()
                f.write("\nInstalled Packages:\n")
                f.write(installed_packages)
                
        except subprocess.CalledProcessError as e:
            print("Error collecting system information:", e)


# Function to collect log files
def collect_log_files(output_dir):
    """
    Collects log files and copies them to the output directory.
    """
    log_files = ['/var/log/syslog', '/var/log/auth.log']  # Example log files on Linux
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                shutil.copy(log_file, os.path.join(output_dir, "collected_data"))
            except Exception as e:
                print("Error copying log file:", e)

# Function to collect security policies
def collect_security_policies(output_dir):
    """
    Collects security policies and writes them to a file.
    """
    output_file = os.path.join(output_dir, "collected_data", "security_policies.txt")
    with open(output_file, "w") as f:
        try:
            subprocess.call(['sudo', 'sestatus'], stdout=f)  # Example command to collect SELinux status
            subprocess.call(['sudo', 'iptables-save'], stdout=f)  # Example command to collect iptables rules
            # Add more commands for collecting security policies as needed
        except subprocess.CalledProcessError as e:
            print("Error collecting security policies:", e)

# Function to collect system logs
def collect_system_logs(output_dir):
    """
    Collects system logs and writes them to files.
    """
    log_files = ['/var/log/syslog', '/var/log/auth.log']  # Example log files on Linux
    for log_file in log_files:
        output_file = os.path.join(output_dir, "collected_data", os.path.basename(log_file))
        try:
            shutil.copy(log_file, output_file)
        except Exception as e:
            print(f"Error copying {log_file}: {e}")

# Main function to orchestrate data collection
def main():
    """
    Main function to coordinate data collection.
    """
    # Define the output directory as the current directory
    output_dir = os.getcwd()

    # Create the collected_data directory if it doesn't exist
    collected_data_dir = os.path.join(output_dir, "collected_data")
    os.makedirs(collected_data_dir, exist_ok=True)

    # Collect system configurations
    collect_system_configurations(output_dir)
    print("System configurations collected.")

    # Collect log files
    collect_log_files(output_dir)
    print("Log files collected.")

    # Collect security policies
    collect_security_policies(output_dir)
    print("Security policies collected.")

    # Collect system logs
    collect_system_logs(output_dir)
    print("System logs collected.")

    print("Data collection completed. Collected data is stored in '{}' directory.".format(collected_data_dir))

if __name__ == "__main__":
    main()
