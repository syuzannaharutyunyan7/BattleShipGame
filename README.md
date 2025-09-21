# Battleship Game

A simple networked Battleship game implemented in Python with a client-server architecture.
The client provides a Tkinter GUI to place ships and play against the server over a TCP socket connection.

---

## Overview

This project demonstrates a turn-based Battleship game played between a server and a client over a network connection.
The server manages the game logic and board state, while the client provides a graphical interface for user interaction.

### The project consists of:

* **Server (`server.py`)** – manages game logic, handles client connections, and enforces rules.
* **Client (`client.py`)** – a Tkinter GUI that allows ship placement and gameplay against the server.

---

## Tech Stack

* **Language:** Python 3.x
* **Networking:** TCP sockets (`socket` module)
* **Serialization:** `pickle` for data exchange
* **GUI:** Tkinter

---

## Project Structure

```
BattleShipGame/
├── server.py          # Game server handling connections and logic
├── client.py          # Tkinter-based game client GUI
├── README.md          # This file
└── (other project files)
```

---

## Prerequisites

Before running the project, ensure you have:

* Python 3.x installed
* Tkinter installed (usually included with Python)
* No external dependencies required

---

## Running the Project

### 1. Run the Server

```bash
python3 server.py
```

The server will start and wait for a client to connect.

### 2. Run the Client

Open another terminal (or machine on the same network) and run:

```bash
python3 client.py
```

Make sure the client’s `HOST` and `PORT` variables match the server’s IP and port.

---

## How to Play

1. Place your 3 ships by clicking cells on your board.
2. Once all ships are placed, the game begins.
3. Take turns attacking cells on the opponent’s board.
4. Hits and misses are visually indicated.
5. The game ends when all ships of one player are sunk.

---

## Example Gameplay Flow

* Client places ships and sends the board to the server.
* Server randomly places its ships and sends its board to the client.
* Players alternate turns sending attack coordinates.
* Boards update with hits ("X") and misses ("O").
* The first to sink all opponent ships wins.

---

## Features

* Real-time two-player Battleship game over network.
* Simple, intuitive Tkinter GUI for gameplay.
* Uses Python’s socket and pickle modules for communication.
* Ship placement and turn-based gameplay enforced.

---

## License

This project is licensed under the MIT License.

---

**Author:** Syuzanna Harutyunyan

---
