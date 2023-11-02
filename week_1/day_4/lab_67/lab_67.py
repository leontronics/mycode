#!/usr/bin/python3

def main():
    vampire_count = 0
    with open('dracula.txt', 'r') as dracula_file:
        with open('vampytimex.txt', 'w') as vampire_file:
            for line in dracula_file:
                if 'vampire' in line.lower():
                    vampire_count += 1
                    vampire_file.write(line)
                    print(line)
    print(vampire_count)

if __name__ == '__main__':
    main()