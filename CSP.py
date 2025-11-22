board = [
    ['', '', '', '2','6', '', '7', '', '1'],
    ['6', '8', '', '','7', '', '', '9', ''],
    ['1', '9', '', '','', '4', '5', '', ''],
    ['8', '2', '', '1','', '', '', '4', ''],
    ['', '', '4', '6','', '2', '9', '', ''],
    ['', '5', '', '','', '3', '', '2', '8'],
    ['', '', '9', '3','', '', '', '7', '4'],
    ['', '4', '', '','5', '', '', '3', '6'],
    ['7', '', '3', '','1', '8', '', '', '']
    ]

def CSP_menu():

    print ("Pick a Heuristic")
    Heuristic = int(input ("1.MRV\n2.MCV\n3.LCV"))
    print(Heuristic)
    match Heuristic:
        case 1:
            MRV(board)
        case 2:
            MCV(board)
        case 3:
            MLV(board) 
        case _:
            print("Invalid Option!")


def MRV(board):
    print("MRV Approach\n")


def MCV(board):
    print("MCV Approach\n")


def LCV(board):
    print("MCV Approach\n")


CSP_menu()