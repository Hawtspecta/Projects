import random

DIRECTIONS = ["north", "south", "east", "west"]

class Room:
    def __init__(self, name):
        self.name = name
        self.exits = {}  # direction: Room
        self.item = None
        self.monster = None

    def connect(self, other_room, direction):
        opposite = {"north": "south", "south": "north", "east": "west", "west": "east"}
        if direction in DIRECTIONS:
            self.exits[direction] = other_room
            other_room.exits[opposite[direction]] = self

    def describe(self):
        print(f"\nYou are in the {self.name}.")
        if self.item:
            print(f"You see a {self.item} here.")
        if self.monster:
            print(f"A wild {self.monster} appears!")
        if self.exits:
            print("Exits: " + ", ".join(self.exits.keys()))

    def preview(self):
        return f"{self.name} (Item: {self.item or 'None'}, Monster: {self.monster or 'None'})"

class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.inventory = []
        self.alive = True
        self.must_fight = False
        self.visited = set()

    def move(self, direction):
        if direction in self.current_room.exits:
            next_room = self.current_room.exits[direction]
            # Block access to treasure if Goblin is alive and coming from Library
            if next_room.name == "Treasure Room" and "Torch" not in self.inventory:
                print("It's too dark to enter the Treasure Room without a Torch!")
                return
            if self.current_room.name == "Library" and next_room.name == "Treasure Room" and self.current_room.monster:
                print("The Goblin blocks your path to the Treasure Room! You must defeat it to proceed.")
                self.must_fight = True
                return
            self.current_room = next_room
            self.visited.add(self.current_room.name)
        else:
            print("You can't go that way!")

    def get_item(self):
        if self.current_room.item:
            self.inventory.append(self.current_room.item)
            print(f"You picked up the {self.current_room.item}.")
            self.current_room.item = None
        else:
            print("No item here.")

    def fight(self):
        if self.current_room.monster:
            if "Sword" in self.inventory:
                print(f"You slayed the {self.current_room.monster}!")
                self.current_room.monster = None
                self.must_fight = False
            else:
                print(f"The {self.current_room.monster} killed you...")
                self.alive = False
        else:
            print("No monster here.")

class Game:
    def __init__(self):
        self.rooms = {}
        self.entrance_room = None
        self.setup_rooms()
        self.player = Player(self.entrance_room)
        self.player.visited.add(self.entrance_room.name)

    def setup_rooms(self):
        # Create rooms with fixed layout
        entrance = Room("Entrance")
        hallway = Room("Hallway")
        armory = Room("Armory")
        library = Room("Library")
        treasure = Room("Treasure Room")

        # Connect rooms in a fixed structure
        entrance.connect(hallway, "north")
        hallway.connect(armory, "east")
        hallway.connect(library, "west")
        library.connect(treasure, "north")

        # Assign rooms
        self.rooms = {
            "Entrance": entrance,
            "Hallway": hallway,
            "Armory": armory,
            "Library": library,
            "Treasure Room": treasure
        }
        self.entrance_room = entrance

        # Place items and monster
        hallway.item = "Torch"
        armory.item = "Sword"
        treasure.item = "Gold"
        library.monster = "Goblin"

        print("Room Map (Name, Item, Monster):")
        for room in self.rooms.values():
            print(" - " + room.preview())
        print("📢 Rumor: The Treasure Room lies beyond the Goblin guarding the Library...")

    def game_loop(self):
        print("\nWelcome to Dungeon Escape!")
        print("Find the Gold and return to the Entrance to win!")
        print("Type 'help' to view available commands.")
        print("Commands:")
        print("  north/south/east/west - move in a direction")
        print("  get     - pick up the item in the room")
        print("  fight   - fight the monster if present")
        print("  inventory - check your inventory")
        print("  help    - show this help message")
        print("  quit    - exit the game")

        while self.player.alive:
            self.player.current_room.describe()
            print(f"Visited Rooms: {', '.join(sorted(self.player.visited))}")
            self.player.must_fight = False  # reset
            command = input("\n> ").strip().lower()

            if command in DIRECTIONS:
                self.player.move(command)
            elif command == "get":
                self.player.get_item()
            elif command == "fight":
                self.player.fight()
            elif command == "inventory":
                print(f"Inventory: {self.player.inventory}")
            elif command == "help":
                print("Commands:")
                print("  north/south/east/west - move in a direction")
                print("  get     - pick up the item in the room")
                print("  fight   - fight the monster if present")
                print("  inventory - check your inventory")
                print("  help    - show this help message")
                print("  quit    - exit the game")
            elif command == "quit":
                print("Goodbye!")
                break
            else:
                print("❓ Unknown command.")

            if not self.player.alive:
                print("You died. Game Over.")
                break

            if "Gold" in self.player.inventory and self.player.current_room.name == "Entrance":
                print("You escaped the dungeon with the treasure! YOU WIN!")
                break

if __name__ == "__main__":
    Game().game_loop()
