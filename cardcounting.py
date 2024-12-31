import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Define card values for various counting systems
counting_systems = {
    "Hi-Lo": {
        "values": {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0, "10": -1, "jack": -1, "queen": -1, "king": -1, "ace": -1},
        "difficulty": "Beginner"
    },
    "KO": {
        "values": {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 0, "9": 0, "10": -1, "jack": -1, "queen": -1, "king": -1, "ace": -1},
        "difficulty": "Beginner"
    },
    "Omega II": {
        "values": {"2": 1, "3": 1, "4": 2, "5": 2, "6": 2, "7": 1, "8": 0, "9": -1, "10": -2, "jack": -2, "queen": -2, "king": -2, "ace": 0},
        "difficulty": "Advanced"
    },
    "Halves": {
        "values": {"2": 0.5, "3": 1, "4": 1, "5": 1.5, "6": 1, "7": 0.5, "8": 0, "9": -0.5, "10": -1, "jack": -1, "queen": -1, "king": -1, "ace": -1},
        "difficulty": "Advanced"
    },
    "Zen Count": {
        "values": {"2": 1, "3": 1, "4": 2, "5": 2, "6": 2, "7": 1, "8": 0, "9": 0, "10": -2, "jack": -2, "queen": -2, "king": -2, "ace": -1},
        "difficulty": "Intermediate"
    }
}

# Define suits
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Create a deck of cards with suits
def create_deck(num_decks=1):
    single_deck = [f"{rank} of {suit}" for suit in suits for rank in 
                   ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]]
    return single_deck * num_decks

# Extract the rank from a card (e.g., "2 of Hearts" -> "2")
def extract_rank(card):
    return card.split(" of ")[0]

# Shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)

# Calculate the True Count
def calculate_true_count(running_count, cards_remaining, deck_size):
    decks_remaining = cards_remaining / deck_size
    if decks_remaining > 0:
        return running_count / decks_remaining
    return 0

# Main application class
class CardCountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Counting Practice")
        self.root.geometry("700x600")
        self.root.resizable(True, True)  # Allow resizing of the window
        
        # Initialize variables
        self.deck = []
        self.running_count = 0
        self.deck_size = 52
        self.cards_dealt = 0
        self.num_decks = 1
        self.card_images = {}
        self.default_image = None  # Placeholder for missing images
        self.selected_system = "Hi-Lo"
        self.showing_results = False
        
        # Load card images
        self.load_card_images()
        
        # UI Setup
        self.setup_ui()
        
    def load_card_images(self):
        """Load card images into a dictionary."""
        self.default_image = ImageTk.PhotoImage(Image.new("RGB", (100, 150), color="gray"))  # Default placeholder
        for suit in suits:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]:
                card_name = f"{rank} of {suit}"
                try:
                    image = Image.open(f"/Users/aaronstern/Desktop/python_files/cardcounting/card_images/{rank}_of_{suit}.png").resize((100, 150))
                    self.card_images[card_name] = ImageTk.PhotoImage(image)
                except FileNotFoundError:
                    print(f"Image for {card_name} not found. Using default image.")
                    self.card_images[card_name] = self.default_image
        
    def setup_ui(self):
        tk.Label(self.root, text="Card Counting Practice", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.root, text="Number of Decks:").pack()
        self.deck_entry = tk.Entry(self.root, justify="center")
        self.deck_entry.pack()
        self.deck_entry.insert(0, "1")
        
        tk.Label(self.root, text="Counting System:").pack()
        self.system_selector = ttk.Combobox(self.root, values=[f"{name} ({data['difficulty']})" for name, data in counting_systems.items()], state="readonly")
        self.system_selector.pack()
        self.system_selector.set("Hi-Lo (Beginner)")
        
        self.start_button = tk.Button(self.root, text="Start Practice", command=self.start_practice)
        self.start_button.pack(pady=10)
        
        self.card_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.card_label.pack(pady=10)
        
        self.card_image_label = tk.Label(self.root)
        self.card_image_label.pack(pady=10)
        
        self.info_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left")
        self.info_label.pack(pady=10)
        self.info_label.pack_forget()  # Hide the score initially
        
        self.next_button = tk.Button(self.root, text="Next Card", command=self.next_card, state="disabled")
        self.next_button.pack(pady=10)
        
        self.show_results_button = tk.Button(self.root, text="Show Results", command=self.show_results, state="disabled")
        self.show_results_button.pack(pady=10)
        
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)
    
    def start_practice(self):
        try:
            self.num_decks = int(self.deck_entry.get())
            if self.num_decks <= 0:
                raise ValueError("Number of decks must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            return
        
        self.selected_system = self.system_selector.get().split(" (")[0]
        self.deck = create_deck(self.num_decks)
        shuffle_deck(self.deck)
        
        self.running_count = 0
        self.cards_dealt = 0
        self.deck_size = 52 * self.num_decks  # Total number of cards in all decks
        
        self.card_label.config(text="")
        self.info_label.config(text="")
        
        self.next_button.config(state="normal")
        self.show_results_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.deck_entry.config(state="disabled")
        self.system_selector.config(state="disabled")
        self.next_card()
    
    def next_card(self):
        if self.cards_dealt >= len(self.deck):
            # Show results after the last card
            cards_remaining = len(self.deck) - self.cards_dealt
            true_count = calculate_true_count(self.running_count, cards_remaining, self.deck_size)
            self.info_label.config(
                text=f"Practice Complete!\n"
                     f"Cards Dealt: {self.cards_dealt}\n"
                     f"Cards Remaining: {cards_remaining}\n"
                     f"Running Count: {self.running_count}\n"
                     f"True Count: {true_count:.2f}"
            )
            self.info_label.pack()  # Show the final scores
            messagebox.showinfo("Practice Complete", "You have gone through the entire deck.")
            self.reset_practice()
            return

        # Deal the next card
        card = self.deck[self.cards_dealt]
        self.cards_dealt += 1

        # Update Running Count and True Count
        rank = extract_rank(card)
        values = counting_systems[self.selected_system]["values"]
        self.running_count += values[rank]

        # Update UI
        self.card_label.config(text=f"Revealed Card: {card}")
        if card in self.card_images:
            self.card_image_label.config(image=self.card_images[card])
        else:
            self.card_image_label.config(image=self.default_image)

        # Ensure the info label is hidden if it was previously displayed
        self.info_label.pack_forget()
        self.showing_results = False
    
    def show_results(self):
        if not self.showing_results:
            cards_remaining = len(self.deck) - self.cards_dealt
            true_count = calculate_true_count(self.running_count, cards_remaining, self.deck_size)
            self.info_label.config(
                text=f"Running Count: {self.running_count}\n"
                     f"True Count: {true_count:.2f}\n"
                     f"Cards Dealt: {self.cards_dealt}\n"
                     f"Cards Remaining: {cards_remaining}"
            )
            self.info_label.pack()
            self.showing_results = True
        else:
            self.info_label.pack_forget()
            self.showing_results = False
    
    def reset_practice(self):
        self.next_button.config(state="disabled")
        self.show_results_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.deck_entry.config(state="normal")
        self.system_selector.config(state="normal")
        self.card_label.config(text="")
        self.card_image_label.config(image=self.default_image)
        self.info_label.pack_forget()

# Create the main window and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CardCountingApp(root)
    root.mainloop()

