def main():
    commands = []
    while input() != "exit" and input() != "quit" :
        if input() not in commands:
            print("Unknown command")