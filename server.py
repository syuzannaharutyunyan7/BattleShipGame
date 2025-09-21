import socket
import pickle
import random

SIZE = 5
SHIPS = 3

def create_board():
    return [["~"] * SIZE for _ in range(SIZE)]

def check_hit(board, move):
    x, y = move
    if board[x][y] == "S":
        board[x][y] = "X"
        return True
    elif board[x][y] == "~":
        board[x][y] = "O"
        return False
    return False

def has_ships(board):
    for row in board:
        if "S" in row:
            return True
    return False

HOST = '0.0.0.0'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("Waiting for a player to join...")

conn, addr = server.accept()
print(f"Player connected: {addr}")

# 1. Receive player's board from client
data = conn.recv(4096)
player_board = pickle.loads(data)
print("Received player board.")

# 2. Create server board and place ships randomly
server_board = create_board()
count = 0
while count < SHIPS:
    x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
    if server_board[x][y] == "~":
        server_board[x][y] = "S"
        count += 1

# 3. Send server board to client
conn.send(pickle.dumps(server_board))

turn = 0  # 0 = server's turn, 1 = client's turn

while True:
    if turn == 0:
        # Server's turn to attack - wait for input here
        print("\nYour turn. Enter attack coordinates:")
        while True:
            try:
                x = int(input(f"Row (0-{SIZE-1}): "))
                y = int(input(f"Col (0-{SIZE-1}): "))
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    if player_board[x][y] in ["X", "O"]:
                        print("Already attacked there. Try again.")
                    else:
                        break
                else:
                    print("Coordinates out of range. Try again.")
            except ValueError:
                print("Invalid input. Use numbers.")

        hit = check_hit(player_board, (x, y))
        print("🎯 HIT!" if hit else "💨 MISS!")

        # Send move result to client
        conn.send(pickle.dumps(((x, y), hit)))

        if not has_ships(player_board):
            print("🏆 You win!")
            conn.send(pickle.dumps("LOSE"))  # Tell client they lost
            break

        turn = 1

    else:
        # Client's turn to attack - receive move from client
        print("\nWaiting for client's move...")
        data = conn.recv(4096)
        if not data:
            print("Connection lost.")
            break

        payload = pickle.loads(data)

        if payload == "LOSE":
            print("🏆 You lose!")
            conn.send(pickle.dumps("WIN"))  # Tell client they won
            break

        move = payload
        x, y = move
        hit_result = check_hit(server_board, move)
        print(f"Client attacked ({x},{y}) -> {'HIT' if hit_result else 'MISS'}")

        # Send result back to client
        conn.send(pickle.dumps(((x, y), hit_result)))

        if not has_ships(server_board):
            print("🏆 You lose!")
            conn.send(pickle.dumps("WIN"))  # Tell client they won
            break

        turn = 0

conn.close()
