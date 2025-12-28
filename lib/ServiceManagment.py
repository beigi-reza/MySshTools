#!/usr/bin/env python3
"""
Linux Service Manager - Manage systemd services
Requires: Python 3.6+, root privileges for most operations
"""

import subprocess
import sys
import os
from pathlib import Path


class ServiceManager:
    """Manage systemd services on Linux"""
    
    def __init__(self):
        self.service_path = Path("/etc/systemd/system")
    
    def _run_command(self, cmd, check=True):
        """Execute shell command and return result"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr, e.returncode
    
    def _check_root(self):
        """Check if running with root privileges"""
        if os.geteuid() != 0:
            print("⚠️  Warning: This operation typically requires root privileges")
            return False
        return True
    
    def create_service(self, name, description, exec_start, 
                      user=None, working_dir=None, restart="on-failure"):
        """
        Create a systemd service file
        
        Args:
            name: Service name (without .service extension)
            description: Service description
            exec_start: Command to execute
            user: User to run service as (optional)
            working_dir: Working directory (optional)
            restart: Restart policy (default: on-failure)
        """
        service_file = self.service_path / f"{name}.service"
        
        service_content = f"""[Unit]
Description={description}
After=network.target

[Service]
Type=simple
ExecStart={exec_start}
Restart={restart}
"""
        
        if user:
            service_content += f"User={user}\n"
        
        if working_dir:
            service_content += f"WorkingDirectory={working_dir}\n"
        
        service_content += """
[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open(service_file, 'w') as f:
                f.write(service_content)
            print(f"✓ Service file created: {service_file}")
            return True
        except PermissionError:
            print(f"✗ Permission denied. Run with sudo to create service files.")
            return False
        except Exception as e:
            print(f"✗ Error creating service: {e}")
            return False
    
    def install_service(self, name):
        """Reload systemd daemon to recognize new service"""
        self._check_root()
        stdout, stderr, code = self._run_command("systemctl daemon-reload")
        
        if code == 0:
            print(f"✓ Service '{name}' installed (daemon reloaded)")
            return True
        else:
            print(f"✗ Failed to install service: {stderr}")
            return False
    
    def enable_service(self, name):
        """Enable service to start on boot"""
        self._check_root()
        stdout, stderr, code = self._run_command(f"systemctl enable {name}")
        
        if code == 0:
            print(f"✓ Service '{name}' enabled")
            return True
        else:
            print(f"✗ Failed to enable service: {stderr}")
            return False
    
    def start_service(self, name):
        """Start the service"""
        self._check_root()
        stdout, stderr, code = self._run_command(f"systemctl start {name}")
        
        if code == 0:
            print(f"✓ Service '{name}' started")
            return True
        else:
            print(f"✗ Failed to start service: {stderr}")
            return False
    
    def stop_service(self, name):
        """Stop the service"""
        self._check_root()
        stdout, stderr, code = self._run_command(f"systemctl stop {name}")
        
        if code == 0:
            print(f"✓ Service '{name}' stopped")
            return True
        else:
            print(f"✗ Failed to stop service: {stderr}")
            return False
    
    def status_service(self, name):
        """Check service status"""
        # Get status output
        stdout, stderr, code = self._run_command(f"systemctl status {name}", check=False)
        
        # Get active state
        active_out, _, _ = self._run_command(f"systemctl is-active {name}", check=False)
        active_state = active_out.strip()
        
        # Get enabled state
        enabled_out, _, _ = self._run_command(f"systemctl is-enabled {name}", check=False)
        enabled_state = enabled_out.strip()
        
        # Determine status emoji and text
        status_map = {
            'active': '🟢 ACTIVE',
            'inactive': '🔴 INACTIVE',
            'failed': '❌ FAILED',
            'activating': '🟡 ACTIVATING',
            'deactivating': '🟡 DEACTIVATING'
        }
        
        status_display = status_map.get(active_state, f'⚪ {active_state.upper()}')
        enabled_display = '✓ ENABLED' if enabled_state == 'enabled' else '✗ DISABLED'
        
        print(f"\n{'='*60}")
        print(f"Status for service: {name}")
        print(f"{'='*60}")
        print(f"Active State:  {status_display}")
        print(f"Enabled State: {enabled_display}")
        print(f"{'='*60}")
        print(stdout if stdout else stderr)
        print(f"{'='*60}\n")
        
        return code == 0
    
    def disable_service(self, name):
        """Disable service from starting on boot"""
        self._check_root()
        stdout, stderr, code = self._run_command(f"systemctl disable {name}")
        
        if code == 0:
            print(f"✓ Service '{name}' disabled")
            return True
        else:
            print(f"✗ Failed to disable service: {stderr}")
            return False
    
    def delete_service(self, name):
        """Delete service file"""
        self._check_root()
        
        # Stop and disable first
        self.stop_service(name)
        self.disable_service(name)
        
        service_file = self.service_path / f"{name}.service"
        
        try:
            if service_file.exists():
                service_file.unlink()
                self._run_command("systemctl daemon-reload")
                print(f"✓ Service '{name}' deleted")
                return True
            else:
                print(f"✗ Service file not found: {service_file}")
                return False
        except PermissionError:
            print(f"✗ Permission denied. Run with sudo to delete service files.")
            return False
        except Exception as e:
            print(f"✗ Error deleting service: {e}")
            return False


def print_menu():
    """Display menu options"""
    print("\n" + "="*60)
    print("Linux Service Manager")
    print("="*60)
    print("1. Create a new service")
    print("2. Install service (reload daemon)")
    print("3. Enable service (start on boot)")
    print("4. Start service")
    print("5. Check service status")
    print("6. Stop service")
    print("7. Disable service")
    print("8. Delete service")
    print("9. Exit")
    print("="*60)


def main():
    """Main program loop"""
    manager = ServiceManager()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            name = input("Service name: ").strip()
            description = input("Description: ").strip()
            exec_start = input("Command to execute: ").strip()
            user = input("User (press Enter to skip): ").strip() or None
            working_dir = input("Working directory (press Enter to skip): ").strip() or None
            
            manager.create_service(name, description, exec_start, user, working_dir)
        
        elif choice == "2":
            name = input("Service name: ").strip()
            manager.install_service(name)
        
        elif choice == "3":
            name = input("Service name: ").strip()
            manager.enable_service(name)
        
        elif choice == "4":
            name = input("Service name: ").strip()
            manager.start_service(name)
        
        elif choice == "5":
            name = input("Service name: ").strip()
            manager.status_service(name)
        
        elif choice == "6":
            name = input("Service name: ").strip()
            manager.stop_service(name)
        
        elif choice == "7":
            name = input("Service name: ").strip()
            manager.disable_service(name)
        
        elif choice == "8":
            name = input("Service name: ").strip()
            confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                manager.delete_service(name)
            else:
                print("Deletion cancelled")
        
        elif choice == "9":
            print("Exiting...")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)