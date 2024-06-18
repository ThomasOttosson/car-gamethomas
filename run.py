def get_shot():

    shot = input("please enter your guess")

def show_board(hit,miss,comp):


    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in miss:
                ch = " x "
            elif place in hit:
                ch = " o "
            elif place in comp:
                ch = " O "

            row = row + ch
            place = place + 1

hit = [21,22]
miss = [20,24,12,13]
comp = [23]

get_shot()
show_board(hit,miss,comp)