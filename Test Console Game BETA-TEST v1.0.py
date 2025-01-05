# TEST CONSOLE GAME BY ZEST4EK
import os,time,threading

cube_pos = 83
spike_pos = 99
score = 0
status = ""

# SYMBOLS
invis_sym = "⠀"
cube_sym = "#"
floor_sym = "@"
spike_sym = "▲"

board = [invis_sym] * 100
floor = [floor_sym] * 20

board[cube_pos] = cube_sym 
board[spike_pos] = spike_sym

jump_value = False


def printt():
    os.system("cls||clear")
    print("".join(board[0:20]),  "| TEST CONSOLE GAME BY ZEST4EK")
    print("".join(board[20:40]), "| JUMP - Press [ENTER]")
    print("".join(board[40:60]), "|")
    print("".join(board[60:80]),f"| Score: {score}")
    print("".join(board[80:100]),"|",status)
    print("".join(floor),        "|")


def main():
    global spike_pos,status,board,floor,score

    while status != "GAME OVER":
        board[spike_pos] = invis_sym
        spike_pos -= 1

        if spike_pos < 80:
            score += 1
            spike_pos = 99

        if board[spike_pos] == board[cube_pos]:
            status = "GAME OVER"
            board = [cube_sym] * 100
            floor = [cube_sym] * 20
            printt()
            return

        board[spike_pos] = spike_sym
        printt()
        time.sleep(0.2)


def jump():
    global cube_pos,jump_value

    if jump_value:
        return

    jump_value = True

    for i in range(3):  # Move up
        board[cube_pos] = invis_sym
        cube_pos -= 20
        board[cube_pos] = cube_sym
        printt()
        time.sleep(0.1)

    for i in range(3):  # Move down
        board[cube_pos] = invis_sym
        cube_pos += 20
        board[cube_pos] = cube_sym
        printt()
        time.sleep(0.1)

    jump_value = False


def check_jump():
    global status
    while status != "GAME OVER":
        input()
        if status != "GAME OVER":
            jump()


if __name__ == "__main__":
    
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

    jump_thread = threading.Thread(target=check_jump, daemon=True)
    jump_thread.start()

    main_thread.join()

    main()
