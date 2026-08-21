import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

# Optional text-to-speech
try:
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False


DATA_FILE = "language_data.json"
PROGRESS_FILE = "progress.json"


default_data = {
    "Spanish": {
        "Vocabulary": [
            {"word": "Hola", "meaning": "Hello", "pronunciation": "OH-la"},
            {"word": "Gracias", "meaning": "Thank you", "pronunciation": "GRAH-see-as"},
            {"word": "Casa", "meaning": "House", "pronunciation": "KA-sa"},
            {"word": "Agua", "meaning": "Water", "pronunciation": "AH-gwa"},
            {"word": "Amigo", "meaning": "Friend", "pronunciation": "a-MEE-go"}
        ],
        "Phrases": [
            {
                "word": "¿Cómo estás?",
                "meaning": "How are you?",
                "pronunciation": "KOH-mo es-TAS"
            },
            {
                "word": "Buenos días",
                "meaning": "Good morning",
                "pronunciation": "BWE-nos DEE-as"
            },
            {
                "word": "Buenas noches",
                "meaning": "Good night",
                "pronunciation": "BWE-nas NO-ches"
            }
        ],
        "Grammar": [
            {"word": "Yo soy", "meaning": "I am", "pronunciation": "YO soy"},
            {"word": "Tú eres", "meaning": "You are", "pronunciation": "TOO EH-res"},
            {"word": "Él es", "meaning": "He is", "pronunciation": "EL es"}
        ]
    },

    "French": {
        "Vocabulary": [
            {"word": "Bonjour", "meaning": "Hello", "pronunciation": "bon-ZHOOR"},
            {"word": "Merci", "meaning": "Thank you", "pronunciation": "mehr-SEE"},
            {"word": "Maison", "meaning": "House", "pronunciation": "may-ZON"},
            {"word": "Eau", "meaning": "Water", "pronunciation": "OH"},
            {"word": "Ami", "meaning": "Friend", "pronunciation": "ah-MEE"}
        ],
        "Phrases": [
            {
                "word": "Comment allez-vous?",
                "meaning": "How are you?",
                "pronunciation": "koh-MAHN tah-lay VOO"
            },
            {
                "word": "Bonne journée",
                "meaning": "Have a good day",
                "pronunciation": "bun zhoor-NAY"
            },
            {
                "word": "Bonne nuit",
                "meaning": "Good night",
                "pronunciation": "bun NWEE"
            }
        ],
        "Grammar": [
            {"word": "Je suis", "meaning": "I am", "pronunciation": "zhuh swee"},
            {"word": "Tu es", "meaning": "You are", "pronunciation": "too ay"},
            {"word": "Il est", "meaning": "He is", "pronunciation": "eel ay"}
        ]
    },

    "German": {
        "Vocabulary": [
            {"word": "Hallo", "meaning": "Hello", "pronunciation": "HA-lo"},
            {"word": "Danke", "meaning": "Thank you", "pronunciation": "DAN-kuh"},
            {"word": "Haus", "meaning": "House", "pronunciation": "HOWS"},
            {"word": "Wasser", "meaning": "Water", "pronunciation": "VA-ser"},
            {"word": "Freund", "meaning": "Friend", "pronunciation": "FROYNT"}
        ],
        "Phrases": [
            {
                "word": "Wie geht es dir?",
                "meaning": "How are you?",
                "pronunciation": "vee gate es deer"
            },
            {
                "word": "Guten Morgen",
                "meaning": "Good morning",
                "pronunciation": "GOO-ten MOR-gen"
            },
            {
                "word": "Gute Nacht",
                "meaning": "Good night",
                "pronunciation": "GOO-teh nakht"
            }
        ],
        "Grammar": [
            {"word": "Ich bin", "meaning": "I am", "pronunciation": "ikh bin"},
            {"word": "Du bist", "meaning": "You are", "pronunciation": "doo bist"},
            {"word": "Er ist", "meaning": "He is", "pronunciation": "air ist"}
        ]
    }
}



def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return default_data

    save_data(default_data)
    return default_data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {
                "quiz_attempts": 0,
                "correct": 0,
                "questions_answered": 0
            }

    return {
        "quiz_attempts": 0,
        "correct": 0,
        "questions_answered": 0
    }


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress, file, indent=4)



class LanguageLearningApp:

    # FIXED: __init__
    def __init__(self, root):

        self.root = root
        self.root.title("Language Learning App")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        self.data = load_data()
        self.progress = load_progress()

        self.current_card = 0
        self.current_category = "Vocabulary"
        self.showing_answer = False

        self.quiz_questions = []
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_options = []
        self.correct_answer = ""

        self.setup_style()
        self.create_header()
        self.create_language_selection()
        self.create_tabs()

        self.update_flashcard()


    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Heading.TLabel",
            font=("Arial", 16, "bold")
        )

        style.configure(
            "Normal.TLabel",
            font=("Arial", 12)
        )

        style.configure(
            "Action.TButton",
            font=("Arial", 11, "bold"),
            padding=8
        )


    def create_header(self):

        header = ttk.Frame(self.root)
        header.pack(fill="x", pady=15)

        title = ttk.Label(
            header,
            text="🌍 Language Learning App",
            style="Title.TLabel"
        )
        title.pack()

        subtitle = ttk.Label(
            header,
            text="Learn words, phrases and grammar interactively"
        )
        subtitle.pack(pady=5)


    def create_language_selection(self):

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(
            frame,
            text="Select Language:",
            style="Heading.TLabel"
        ).pack(side="left", padx=10)

        self.language_var = tk.StringVar(
            value=list(self.data.keys())[0]
        )

        language_menu = ttk.Combobox(
            frame,
            textvariable=self.language_var,
            values=list(self.data.keys()),
            state="readonly",
            width=20
        )

        language_menu.pack(side="left")

        language_menu.bind(
            "<<ComboboxSelected>>",
            self.language_changed
        )

    def language_changed(self, event=None):

        self.current_card = 0
        self.showing_answer = False

        self.update_flashcard()


    def create_tabs(self):

        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.flashcard_tab = ttk.Frame(self.notebook)
        self.quiz_tab = ttk.Frame(self.notebook)
        self.add_tab = ttk.Frame(self.notebook)
        self.progress_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.flashcard_tab,
            text="📚 Flashcards"
        )

        self.notebook.add(
            self.quiz_tab,
            text="📝 Quiz"
        )

        self.notebook.add(
            self.add_tab,
            text="➕ Add Word"
        )

        self.notebook.add(
            self.progress_tab,
            text="📊 Progress"
        )

        self.create_flashcard_ui()
        self.create_quiz_ui()
        self.create_add_word_ui()
        self.create_progress_ui()



    def create_flashcard_ui(self):

        category_frame = ttk.Frame(self.flashcard_tab)
        category_frame.pack(pady=15)

        ttk.Label(
            category_frame,
            text="Category:"
        ).pack(side="left", padx=5)

        self.category_var = tk.StringVar(
            value="Vocabulary"
        )

        categories = [
            "Vocabulary",
            "Phrases",
            "Grammar"
        ]

        category_menu = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=18
        )

        category_menu.pack(side="left")

        category_menu.bind(
            "<<ComboboxSelected>>",
            self.category_changed
        )

        # Flashcard
        self.card_frame = tk.Frame(
            self.flashcard_tab,
            bd=2,
            relief="ridge",
            width=600,
            height=280
        )

        self.card_frame.pack(
            pady=10,
            padx=50
        )

        self.card_frame.pack_propagate(False)

        self.word_label = tk.Label(
            self.card_frame,
            text="",
            font=("Arial", 30, "bold")
        )

        self.word_label.pack(
            pady=(50, 15)
        )

        self.meaning_label = tk.Label(
            self.card_frame,
            text="",
            font=("Arial", 18)
        )

        self.meaning_label.pack(pady=5)

        self.pronunciation_label = tk.Label(
            self.card_frame,
            text="",
            font=("Arial", 13)
        )

        self.pronunciation_label.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(self.flashcard_tab)
        button_frame.pack(pady=15)

        ttk.Button(
            button_frame,
            text="⬅️ Previous",
            command=self.previous_card,
            style="Action.TButton"
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="🔍 Show Answer",
            command=self.show_answer,
            style="Action.TButton"
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="🔊 Pronounce",
            command=self.pronounce,
            style="Action.TButton"
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            button_frame,
            text="Next ➡️",
            command=self.next_card,
            style="Action.TButton"
        ).grid(row=0, column=3, padx=5)

        self.card_counter = ttk.Label(
            self.flashcard_tab,
            text=""
        )

        self.card_counter.pack(pady=5)


    def get_cards(self):

        language = self.language_var.get()
        category = self.category_var.get()

        return self.data[language][category]

    def category_changed(self, event=None):

        self.current_card = 0
        self.showing_answer = False

        self.update_flashcard()

    def update_flashcard(self):

        cards = self.get_cards()

        if not cards:

            self.word_label.config(
                text="No cards available"
            )

            self.meaning_label.config(text="")
            self.pronunciation_label.config(text="")
            self.card_counter.config(text="")

            return

        if self.current_card >= len(cards):
            self.current_card = 0

        card = cards[self.current_card]

        self.word_label.config(
            text=card["word"]
        )

        if self.showing_answer:

            self.meaning_label.config(
                text="Meaning: " + card["meaning"]
            )

            self.pronunciation_label.config(
                text="Pronunciation: " +
                card.get("pronunciation", "Not available")
            )

        else:

            self.meaning_label.config(
                text="Click 'Show Answer'"
            )

            self.pronunciation_label.config(
                text=""
            )

        self.card_counter.config(
            text=f"Card {self.current_card + 1} / {len(cards)}"
        )

    def show_answer(self):

        self.showing_answer = True
        self.update_flashcard()

    def next_card(self):

        cards = self.get_cards()

        if cards:

            self.current_card = (
                self.current_card + 1
            ) % len(cards)

            self.showing_answer = False

            self.update_flashcard()

    def previous_card(self):

        cards = self.get_cards()

        if cards:

            self.current_card = (
                self.current_card - 1
            ) % len(cards)

            self.showing_answer = False

            self.update_flashcard()

    def pronounce(self):

        if not SPEECH_AVAILABLE:

            messagebox.showinfo(
                "Text-to-Speech",
                "Install pyttsx3 to enable pronunciation:\n\n"
                "pip install pyttsx3"
            )

            return

        cards = self.get_cards()

        if not cards:
            return

        word = cards[self.current_card]["word"]

        try:

            engine = pyttsx3.init()
            engine.say(word)
            engine.runAndWait()

        except Exception:

            messagebox.showerror(
                "Error",
                "Unable to play pronunciation."
            )


    def create_quiz_ui(self):

        ttk.Label(
            self.quiz_tab,
            text="Language Quiz",
            style="Title.TLabel"
        ).pack(pady=20)

        ttk.Label(
            self.quiz_tab,
            text="Test your vocabulary knowledge!"
        ).pack(pady=5)

        self.quiz_question = ttk.Label(
            self.quiz_tab,
            text="Click Start Quiz",
            font=("Arial", 20, "bold"),
            wraplength=650
        )

        self.quiz_question.pack(pady=35)

        self.answer_var = tk.StringVar()

        self.answer_buttons = []

        for i in range(4):

            button = ttk.Button(
                self.quiz_tab,
                text="",
                command=lambda i=i: self.check_answer(i),
                width=40
            )

            button.pack(pady=5)

            self.answer_buttons.append(button)

        self.start_quiz_button = ttk.Button(
            self.quiz_tab,
            text="▶️ Start Quiz",
            command=self.start_quiz,
            style="Action.TButton"
        )

        self.start_quiz_button.pack(pady=20)

        self.quiz_score_label = ttk.Label(
            self.quiz_tab,
            text="Score: 0"
        )

        self.quiz_score_label.pack()


    def start_quiz(self):

        language = self.language_var.get()

        all_cards = []

        for category in self.data[language]:

            all_cards.extend(
                self.data[language][category]
            )

        if len(all_cards) < 4:

            messagebox.showwarning(
                "Not Enough Data",
                "At least 4 learning items are required."
            )

            return

        self.quiz_questions = random.sample(
            all_cards,
            min(10, len(all_cards))
        )

        self.quiz_index = 0
        self.quiz_score = 0

        self.progress["quiz_attempts"] = (
            self.progress.get("quiz_attempts", 0) + 1
        )

        save_progress(self.progress)

        self.show_quiz_question()

    def show_quiz_question(self):

        if self.quiz_index >= len(self.quiz_questions):

            self.quiz_question.config(
                text=(
                    f"🎉 Quiz Finished!\n\n"
                    f"Score: {self.quiz_score}/"
                    f"{len(self.quiz_questions)}"
                )
            )

            for button in self.answer_buttons:

                button.config(
                    text="",
                    state="disabled"
                )

            save_progress(self.progress)

            self.update_progress()

            return

        current = self.quiz_questions[self.quiz_index]

        self.correct_answer = current["meaning"]

        language = self.language_var.get()

        all_cards = []

        for category in self.data[language]:

            all_cards.extend(
                self.data[language][category]
            )

        wrong_answers = [
            card["meaning"]
            for card in all_cards
            if card["meaning"] != self.correct_answer
        ]

        # Remove duplicates
        wrong_answers = list(set(wrong_answers))

        wrong_answers = random.sample(
            wrong_answers,
            min(3, len(wrong_answers))
        )

        options = wrong_answers + [
            self.correct_answer
        ]

        random.shuffle(options)

        self.quiz_options = options

        self.quiz_question.config(
            text=f"What does '{current['word']}' mean?"
        )

        for i, button in enumerate(self.answer_buttons):

            if i < len(options):

                button.config(
                    text=options[i],
                    state="normal"
                )

            else:

                button.config(
                    text="",
                    state="disabled"
                )

        self.quiz_score_label.config(
            text=f"Score: {self.quiz_score}"
        )

    def check_answer(self, index):

        if self.quiz_index >= len(self.quiz_questions):
            return

        if index >= len(self.quiz_options):
            return

        selected = self.quiz_options[index]

        if selected == self.correct_answer:

            self.quiz_score += 1

            self.progress["correct"] = (
                self.progress.get("correct", 0) + 1
            )

            messagebox.showinfo(
                "Correct!",
                "🎉 Correct answer!"
            )

        else:

            messagebox.showinfo(
                "Incorrect",
                f"Correct answer:\n{self.correct_answer}"
            )

        self.progress["questions_answered"] = (
            self.progress.get("questions_answered", 0) + 1
        )

        self.quiz_index += 1

        save_progress(self.progress)

        self.show_quiz_question()


    def create_add_word_ui(self):

        ttk.Label(
            self.add_tab,
            text="Add New Learning Material",
            style="Title.TLabel"
        ).pack(pady=20)

        form = ttk.Frame(self.add_tab)
        form.pack(pady=20)

        ttk.Label(
            form,
            text="Language:"
        ).grid(
            row=0,
            column=0,
            pady=8
        )

        self.add_language = tk.StringVar(
            value=list(self.data.keys())[0]
        )

        ttk.Combobox(
            form,
            textvariable=self.add_language,
            values=list(self.data.keys()),
            state="readonly",
            width=25
        ).grid(
            row=0,
            column=1
        )

        ttk.Label(
            form,
            text="Category:"
        ).grid(
            row=1,
            column=0,
            pady=8
        )

        self.add_category = tk.StringVar(
            value="Vocabulary"
        )

        ttk.Combobox(
            form,
            textvariable=self.add_category,
            values=[
                "Vocabulary",
                "Phrases",
                "Grammar"
            ],
            state="readonly",
            width=25
        ).grid(
            row=1,
            column=1
        )

        ttk.Label(
            form,
            text="Word / Phrase:"
        ).grid(
            row=2,
            column=0,
            pady=8
        )

        self.word_entry = ttk.Entry(
            form,
            width=28
        )

        self.word_entry.grid(
            row=2,
            column=1
        )

        ttk.Label(
            form,
            text="Translation:"
        ).grid(
            row=3,
            column=0,
            pady=8
        )

        self.meaning_entry = ttk.Entry(
            form,
            width=28
        )

        self.meaning_entry.grid(
            row=3,
            column=1
        )

        ttk.Label(
            form,
            text="Pronunciation:"
        ).grid(
            row=4,
            column=0,
            pady=8
        )

        self.pronunciation_entry = ttk.Entry(
            form,
            width=28
        )

        self.pronunciation_entry.grid(
            row=4,
            column=1
        )

        ttk.Button(
            self.add_tab,
            text="➕ Add Material",
            command=self.add_word,
            style="Action.TButton"
        ).pack(pady=20)


    def add_word(self):

        language = self.add_language.get()
        category = self.add_category.get()

        word = self.word_entry.get().strip()
        meaning = self.meaning_entry.get().strip()
        pronunciation = self.pronunciation_entry.get().strip()

        if not word or not meaning:

            messagebox.showwarning(
                "Missing Information",
                "Please enter both word and translation."
            )

            return

        new_card = {
            "word": word,
            "meaning": meaning,
            "pronunciation": pronunciation
        }

        self.data[language][category].append(
            new_card
        )

        save_data(self.data)

        self.word_entry.delete(
            0,
            tk.END
        )

        self.meaning_entry.delete(
            0,
            tk.END
        )

        self.pronunciation_entry.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Success",
            "New learning material added!"
        )

        self.update_flashcard()


    def create_progress_ui(self):

        ttk.Label(
            self.progress_tab,
            text="Your Learning Progress",
            style="Title.TLabel"
        ).pack(pady=30)

        self.progress_label = ttk.Label(
            self.progress_tab,
            text="",
            font=("Arial", 16)
        )

        self.progress_label.pack(pady=30)

        ttk.Button(
            self.progress_tab,
            text="🔄 Refresh Progress",
            command=self.update_progress
        ).pack(pady=10)

        self.update_progress()

    def update_progress(self):

        attempts = self.progress.get(
            "quiz_attempts",
            0
        )

        correct = self.progress.get(
            "correct",
            0
        )

        questions_answered = self.progress.get(
            "questions_answered",
            0
        )

        if questions_answered > 0:

            accuracy = (
                correct / questions_answered
            ) * 100

        else:

            accuracy = 0

        self.progress_label.config(
            text=(
                f"Quiz Attempts: {attempts}\n\n"
                f"Questions Answered: {questions_answered}\n\n"
                f"Correct Answers: {correct}\n\n"
                f"Accuracy: {accuracy:.1f}%"
            )
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = LanguageLearningApp(root)

    root.mainloop()