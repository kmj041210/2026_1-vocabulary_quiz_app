from __future__ import annotations

from vocabulary_quiz_app.quiz_logic import Word

# example 이용해서 예문 추가
WORDS: list[Word] = [
    Word(term="apple", meaning="사과", example="Apple is good for breakfast."),
    Word(term="book", meaning="책", example="Reading book is one of good hobby."),
    Word(term="chair", meaning="의자", example="Leave that chair for James."),
    Word(term="door", meaning="문", example="Can you open the door please?"),
    Word(term="flower", meaning="꽃", example="Flower is good present for mom."),
    Word(term="friend", meaning="친구", example="Hang out with friends is fun but tired."),
    Word(term="music", meaning="음악", example="Music is my life."),
    Word(term="school", meaning="학교", example="I always wondering to go back to school."),
    Word(term="summer", meaning="여름", example="Anna's birthday is on August, she is summer girl."),
    Word(term="water", meaning="물", example="You need to drink more water not an soda."),
]
