import tkinter as tk
from tkinter import messagebox
import random
import time

class GameBlitzApp:
    def __init__(self, root):
        self.root = root
        root.title("🎮 GameBlitz")
        root.geometry("600x450")
        
        # Player stats
        self.player_name = ""
        self.games_played = 0
        self.games_won = 0
        self.total_time = 0
        
        # Game data
        self.riddles = {
            "easy": [("What has keys but no locks?", "keyboard"), ("What gets wet while drying?", "towel")],
            "medium": [("I have cities but no houses. What am I?", "map"), ("The more you take, the more you leave behind.", "footsteps")],
            "hard": [("I speak without a mouth. What am I?", "echo"), ("What disappears when you say its name?", "silence")]
        }
        
        self.words = {
            "easy": ["cat", "dog", "fish", "red", "blue"],
            "medium": ["python", "coding", "physics", "chemistry"],
            "hard": ["mechanical", "blockchain", "quantum", "aerospace"]
        }
        
        # Current game state
        self.game_active = False
        self.start_time = 0
        
        self.show_name_screen()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_name_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🎮 GAMEBLITZ 🎮", font=("Arial", 24, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter your name:", font=("Arial", 12)).pack()
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.name_entry.pack(pady=10)
        tk.Button(self.root, text="Start", font=("Arial", 12), command=self.save_name, width=15).pack(pady=20)
    
    def save_name(self):
        name = self.name_entry.get().strip()
        if name:
            self.player_name = name
            self.show_menu()
        else:
            messagebox.showwarning("Error", "Please enter a name!")
    
    def show_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.player_name}!", font=("Arial", 16, "bold")).pack(pady=20)
        
        stats = f"Games: {self.games_played} | Wins: {self.games_won}"
        if self.games_played > 0:
            win_rate = int((self.games_won / self.games_played) * 100)
            stats += f" | Win Rate: {win_rate}%"
        tk.Label(self.root, text=stats, font=("Arial", 11)).pack(pady=10)
        
        tk.Button(self.root, text="🔢 Number Game", font=("Arial", 13), command=self.number_game, width=20).pack(pady=8)
        tk.Button(self.root, text="🧩 Riddle Game", font=("Arial", 13), command=self.riddle_game, width=20).pack(pady=8)
        tk.Button(self.root, text="🔤 Word Game", font=("Arial", 13), command=self.word_game, width=20).pack(pady=8)
        tk.Button(self.root, text="📊 Stats", font=("Arial", 13), command=self.show_stats, width=20).pack(pady=8)
        tk.Button(self.root, text="Exit", font=("Arial", 13), command=self.root.destroy, width=20).pack(pady=20)
    
    def number_game(self):
        self.clear_screen()
        tk.Label(self.root, text="🔢 NUMBER GAME", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Difficulty:", font=("Arial", 11)).pack()
        self.difficulty = tk.StringVar(value="easy")
        tk.OptionMenu(self.root, self.difficulty, "easy", "medium", "hard").pack()
        
        tk.Button(self.root, text="Start", font=("Arial", 12), command=self.start_number).pack(pady=15)
        
        self.info_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.info_label.pack(pady=10)
        
        self.entry = tk.Entry(self.root, font=("Arial", 12), width=15, state="disabled")
        self.entry.pack()
        
        tk.Button(self.root, text="Submit", font=("Arial", 11), command=self.check_number).pack(pady=10)
        
        self.timer_label = tk.Label(self.root, text="⏱️ 0s", font=("Arial", 11, "bold"))
        self.timer_label.pack(pady=10)
        
        tk.Button(self.root, text="⬅ Back", command=self.show_menu).pack(pady=10)
    
    def start_number(self):
        diff = self.difficulty.get()
        if diff == "easy":
            self.answer = random.randint(1, 10)
            self.max_tries = 3
            self.info_label.config(text="Guess a number between 1 and 10!")
        elif diff == "medium":
            self.answer = random.randint(1, 50)
            self.max_tries = 5
            self.info_label.config(text="Guess a number between 1 and 50!")
        else:
            self.answer = random.randint(1, 100)
            self.max_tries = 7
            self.info_label.config(text="Guess a number between 1 and 100!")
        
        self.tries = 0
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.game_active = True
        self.start_time = time.time()
        self.games_played += 1
        self.update_timer()
    
    def check_number(self):
        if not self.game_active:
            return
        
        try:
            guess = int(self.entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number!")
            return
        
        self.tries += 1
        
        if guess == self.answer:
            self.win_game(f"🎉 Correct! The answer was {self.answer}")
        elif self.tries >= self.max_tries:
            self.lose_game(f"💔 Game Over! The answer was {self.answer}")
        else:
            hint = "📈 Too low!" if guess < self.answer else "📉 Too high!"
            self.info_label.config(text=f"{hint} Tries left: {self.max_tries - self.tries}")
            self.entry.delete(0, tk.END)
    
    def riddle_game(self):
        self.clear_screen()
        tk.Label(self.root, text="🧩 RIDDLE GAME", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Difficulty:", font=("Arial", 11)).pack()
        self.difficulty = tk.StringVar(value="easy")
        tk.OptionMenu(self.root, self.difficulty, "easy", "medium", "hard").pack()
        
        tk.Button(self.root, text="Start", font=("Arial", 12), command=self.start_riddle).pack(pady=15)
        
        self.info_label = tk.Label(self.root, text="", font=("Arial", 11), wraplength=500)
        self.info_label.pack(pady=10)
        
        self.entry = tk.Entry(self.root, font=("Arial", 12), width=25, state="disabled")
        self.entry.pack()
        
        tk.Button(self.root, text="Submit", font=("Arial", 11), command=self.check_riddle).pack(pady=10)
        
        self.timer_label = tk.Label(self.root, text="⏱️ 0s", font=("Arial", 11, "bold"))
        self.timer_label.pack(pady=10)
        
        tk.Button(self.root, text="⬅ Back", command=self.show_menu).pack(pady=10)
    
    def start_riddle(self):
        diff = self.difficulty.get()
        riddle, answer = random.choice(self.riddles[diff])
        self.answer = answer
        self.max_tries = 3 if diff == "easy" else 2 if diff == "medium" else 1
        
        self.info_label.config(text=f"Riddle: {riddle}")
        self.tries = 0
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.game_active = True
        self.start_time = time.time()
        self.games_played += 1
        self.update_timer()
    
    def check_riddle(self):
        if not self.game_active:
            return
        
        guess = self.entry.get().lower().strip()
        self.tries += 1
        
        if guess == self.answer or guess.replace("a ", "").replace("the ", "") == self.answer:
            self.win_game(f"🎉 Correct! The answer was '{self.answer}'")
        elif self.tries >= self.max_tries:
            self.lose_game(f"💔 Game Over! The answer was '{self.answer}'")
        else:
            messagebox.showinfo("Wrong", f"❌ Try again! Attempts left: {self.max_tries - self.tries}")
            self.entry.delete(0, tk.END)
    
    def word_game(self):
        self.clear_screen()
        tk.Label(self.root, text="🔤 WORD GAME", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Difficulty:", font=("Arial", 11)).pack()
        self.difficulty = tk.StringVar(value="easy")
        tk.OptionMenu(self.root, self.difficulty, "easy", "medium", "hard").pack()
        
        tk.Button(self.root, text="Start", font=("Arial", 12), command=self.start_word).pack(pady=15)
        
        self.info_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.info_label.pack(pady=10)
        
        self.entry = tk.Entry(self.root, font=("Arial", 12), width=25, state="disabled")
        self.entry.pack()
        
        tk.Button(self.root, text="Submit", font=("Arial", 11), command=self.check_word).pack(pady=10)
        
        self.timer_label = tk.Label(self.root, text="⏱️ 0s", font=("Arial", 11, "bold"))
        self.timer_label.pack(pady=10)
        
        tk.Button(self.root, text="⬅ Back", command=self.show_menu).pack(pady=10)
    
    def start_word(self):
        diff = self.difficulty.get()
        self.answer = random.choice(self.words[diff])
        self.max_tries = 4 if diff == "easy" else 3 if diff == "medium" else 2
        
        self.info_label.config(text=f"Guess the {len(self.answer)}-letter word!")
        self.tries = 0
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.game_active = True
        self.start_time = time.time()
        self.games_played += 1
        self.update_timer()
    
    def check_word(self):
        if not self.game_active:
            return
        
        guess = self.entry.get().lower().strip()
        self.tries += 1
        
        if guess == self.answer:
            self.win_game(f"🎉 Correct! The word was '{self.answer}'")
        elif self.tries >= self.max_tries:
            self.lose_game(f"💔 Game Over! The word was '{self.answer}'")
        else:
            hint = f"Hint: starts with '{self.answer[0]}'" if self.tries == 1 else f"ends with '{self.answer[-1]}'" if self.tries == 2 else ""
            messagebox.showinfo("Wrong", f"❌ {hint} Attempts left: {self.max_tries - self.tries}")
            self.entry.delete(0, tk.END)
    
    def update_timer(self):
        if self.game_active:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"⏱️ {elapsed}s")
            self.root.after(1000, self.update_timer)
    
    def win_game(self, message):
        self.game_active = False
        self.games_won += 1
        elapsed = int(time.time() - self.start_time)
        self.total_time += elapsed
        messagebox.showinfo("You Win!", f"{message}\nTime: {elapsed}s")
        self.entry.config(state="disabled")
    
    def lose_game(self, message):
        self.game_active = False
        elapsed = int(time.time() - self.start_time)
        self.total_time += elapsed
        messagebox.showinfo("Game Over", f"{message}\nTime: {elapsed}s")
        self.entry.config(state="disabled")
    
    def show_stats(self):
        self.clear_screen()
        tk.Label(self.root, text="📊 YOUR STATS", font=("Arial", 18, "bold")).pack(pady=20)
        
        stats_text = f"""
Player: {self.player_name}

Games Played: {self.games_played}
Games Won: {self.games_won}
Win Rate: {int((self.games_won/self.games_played)*100) if self.games_played > 0 else 0}%

Total Time Played: {int(self.total_time/60)}m {int(self.total_time%60)}s
        """
        
        tk.Label(self.root, text=stats_text, font=("Arial", 12), justify="left").pack(pady=20)
        tk.Button(self.root, text="⬅ Back to Menu", font=("Arial", 12), command=self.show_menu).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameBlitzApp(root)
    root.mainloop()