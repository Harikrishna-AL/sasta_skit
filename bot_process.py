import os
import pty
import subprocess
import threading
import time
import select


def read_output(master, output):
    while True:
        try:
            data = os.read(master, 1024).decode("utf-8")
            if not data:
                break
            output.append(data)

            # Do whatever you want with the data (e.g., print it).
            print(data, end="", flush=True)
        except OSError:
            # OSError will be raised when there's no more data to read.
            break


def send_input(slave):
    while True:
        try:
            user_input = input()
            os.write(slave, user_input.encode("utf-8") + b"\n")
        except EOFError:
            break


def run_interactive_command(command):
    master, slave = pty.openpty()
    process = subprocess.Popen(
        command,
        stdout=slave,
        stdin=slave,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
        close_fds=True,
    )

    # Close the slave end of the pseudo-terminal to avoid deadlocks.
    os.close(slave)

    output = []
    output_thread = threading.Thread(target=read_output, args=(master, output))
    output_thread.start()

    # Send user input via another thread.
    input_thread = threading.Thread(target=send_input, args=(master,))
    input_thread.start()

    # Wait for the process to complete.
    process.communicate()

    # Wait for the output_thread to finish reading.
    output_thread.join()
    input_thread.join()

    return "".join(output).strip(), output


if __name__ == "__main__":
    command = './main -m ~/Downloads/sasta_skit/pyllama_data/7B/ggml-model-q4_0.bin -n 128 --repeat_penalty 1.0 --color -i -r "User:" -f prompts/chat-with-skit.txt'
    result, output_list = run_interactive_command(command)
    print("Final output:")
    print(result)

    with open("live_outputs.txt", "w", encoding="utf-8") as file:
        file.writelines(output_list)
