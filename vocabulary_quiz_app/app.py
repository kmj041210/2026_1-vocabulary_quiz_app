from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font, messagebox

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        
        self.root = root # root for class
        
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("480x360") #Change size for add word button / Change size again for more UI
        root.resizable(False, False)

        self.word_var = tk.StringVar(value="단어를 불러오는 중...")
        
        self.example_var = tk.StringVar(value="") # example용 변수 추가
        
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")

        ttk.Label(root, text="영단어").pack(pady=(16, 4))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack(pady=(2, 8))

        # show example under the word
        ttk.Label(root, textvariable=self.example_var, font=("NanumGothic", 12, "italic")).pack(pady=(2, 8))
        
        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)

        buttons = ttk.Frame(root)
        buttons.pack(pady=6)
        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(
            side=tk.LEFT, padx=6
        )

        #pop up for add words
        ttk.Button(root, text="Add Word", command=self.open_add_word_window).pack(pady=(2, 6))

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()
        

    def next_word(self) -> None:
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()
        
        #예문 있을때 화면에 나오고 없으면 빈칸으로
        if self.current.example:
            self.example_var.set(f'"{self.current.example}"')
        else:
            self.example_var.set("")
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()
        

    def check_current(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1
        user_input = self.answer_entry.get()
        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])

    # Add word to list
    def open_add_word_window(self) -> None:
        add_win = tk.Toplevel(self.root)
        add_win.title("새 단어 추가")
        add_win.geometry("320x240") #make more space for example
        add_win.resizable(False, False)
        
        #use pop-up page only for prevent user click main page
        add_win.transient(self.root)
        add_win.grab_set()
        
        ttk.Label(add_win, text="영어 단어:").pack(pady=(15, 2))
        term_entry = ttk.Entry(add_win, font=("NanumGothic", 11))
        term_entry.pack(fill=tk.X, padx=20)
        term_entry.focus()

        ttk.Label(add_win, text="한국어 뜻:").pack(pady=(10, 2))
        meaning_entry = ttk.Entry(add_win, font=("NanumGothic", 11))
        meaning_entry.pack(fill=tk.X, padx=20)
        
        #Make space for insert example
        tk.Label(add_win, text="Example : ").pack(pady=(10, 2))
        example_entry = ttk.Entry(add_win, font=("NanumGothic", 12))
        example_entry.pack(fill=tk.X, padx=20) #for design tight
        

        def save_word() -> None:
            term = term_entry.get().strip()
            meaning = meaning_entry.get().strip()
            example = example_entry.get().strip() # calling example

            if not term or not meaning: #for forget to add term or meaning
                messagebox.showwarning("경고", "단어와 뜻을 모두 입력해주세요.", parent=add_win)
                return
            
            # Add word while list is processing
            #The word will disappear quit and open again
            #Save example data too
            new_word = Word(term=term, meaning=meaning, example=example)
            self.words.append(new_word)
            
            messagebox.showinfo("성공", f"'{term}' 단어가 추가되었습니다!", parent=add_win)
            add_win.destroy()

        ttk.Button(add_win, text="저장", command=save_word).pack(pady=15)