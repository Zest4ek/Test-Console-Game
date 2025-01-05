import time,threading,random

invis_sym = "⠀"
cube_sym = "#"
floor_sym = "@"
spike_sym = "▲"

cube_pos = 83
spike_pos = []
score = 0
spike_info = 0
status = ""

board = [invis_sym] * 100

floor_var1 = ["%","&"] * 10
floor_var2 = ["&","%"] * 10
floor = [floor_var1]

board[cube_pos] = cube_sym 
for pos in spike_pos:
    board[pos] = spike_sym
    
jump_value = False
jump_event = threading.Event()


def printt():
    print("\033[H\033[J", end="")
    print("".join(board[0:20]),   "| TEST CONSOLE GAME BETA-TEST v0.2")
    print("".join(board[20:40]),  "| JUMP - Press [ENTER]")
    print("".join(board[40:60]),  "|")
    print("".join(board[60:80]), f"| Score: {score}            Spawn a spike - 10% chance")
    print("".join(board[80:100]),f"| Spikes: {spike_info} (max: 5)  Delete all spikes - 1% chance")
    print("".join(floor),        f"| {status}")


def random_gen():
    global spike_pos,spike_info,status
    if random.random() < 0.10 and len(spike_pos) < 5: # 10% chance

        if board[99] == spike_sym:
            random_gen()
        else:
            spike_pos.append(99)
            spike_info += 1
            status = ""

    if random.random() < 0.01: # 5% chance
        for pos in spike_pos:
            board[pos] = invis_sym
        spike_pos = []
        spike_info = 0
        status = "ALL SPIKES HAVE BEEN DELETED"

def main():
    global spike_pos,status,board,floor,score,floor_var1,floor_var2

    while status != "GAME OVER":
        random_gen()

        if floor == floor_var1:
            floor = floor_var2
        else:
            floor = floor_var1

        for i in range(len(spike_pos)):
            board[spike_pos[i]] = invis_sym
            spike_pos[i] -= 1

            if spike_pos[i] < 80:
                spike_pos[i] = 99 

            if board[spike_pos[i]] == board[cube_pos]:
                print("\033[H\033[J", end="")
                status = "GAME OVER"
                board = [cube_sym] * 100
                floor = [cube_sym] * 20
                printt()
                return

            board[spike_pos[i]] = spike_sym

        score += 1
        printt()
        time.sleep(0.2)


def jump():
    global cube_pos,jump_value

    if jump_value:
        return

    jump_value = True

    for i in range(2):
        board[cube_pos] = invis_sym
        cube_pos -= 20
        board[cube_pos] = cube_sym
        printt()
        time.sleep(0.2)

    time.sleep(0.2)

    for i in range(2):
        board[cube_pos] = invis_sym
        cube_pos += 20
        board[cube_pos] = cube_sym
        printt()
        time.sleep(0.2)

    jump_value = False


def check_jump():
    global status
    while status != "GAME OVER":
        input()
        if status != "GAME OVER":
            jump_event.set()


def jump_event_control():
    while status != "GAME OVER":
        jump_event.wait() 
        jump_event.clear()
        jump()
        

if __name__ == "__main__":
    
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

    jump_thread = threading.Thread(target=check_jump, daemon=True)
    jump_thread.start()

    control_thread = threading.Thread(target=jump_event_control, daemon=True)
    control_thread.start()

    main_thread.join()

    main()
