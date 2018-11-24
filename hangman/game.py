from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self,guess,hit=None,miss=None):
        if hit==True and miss==True:
            raise InvalidGuessAttempt()
        self.hit=hit
        self.miss=miss
        
    def is_hit(self):
        if self.hit==True:
            return True
        return False
        
    def is_miss(self):
        if self.miss==True:
            return True
        return False
        

class GuessWord(object):
    def __init__(self,word):
        if len(word)==0:
            raise InvalidWordException()
        self.answer=word
        self.masked="*"*len(word)
    
    def unveil_letters(self,letter):
        result=""
        for i in range(len(self.masked)):
            if letter == self.answer[i].lower():
                result+=letter
            else:
                result+=self.masked[i]
        return result
    
    def perform_attempt(self,guess):
        if len(guess)>1:
            raise InvalidGuessedLetterException()
        guess=guess.lower()
        if guess in self.answer.lower():
            attemp=GuessAttempt(guess,hit=True)
            self.masked=self.unveil_letters(guess)
            return attemp
        else:
            attemp=GuessAttempt(guess,miss=True)
            return attemp
    



class HangmanGame(object):
    WORD_LIST=['rmotr', 'python', 'awesome']
    def __init__(self,word_list=None,number_of_guesses=5):
        if not word_list:
            word_list=self.WORD_LIST
        self.WORD_LIST=word_list
        self.remaining_misses=number_of_guesses
        self.word=GuessWord(self.select_random_word(word_list))
        self.previous_guesses=[]
        
    def is_won(self):
        if self.word.answer==self.word.masked:
            return True
        return False
        
    def is_lost(self):
        if self.remaining_misses==0:
            return True
        return False
        
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def guess(self,guess_char):
        guess_char=guess_char.lower()
        if self.is_finished()==True:
            raise GameFinishedException()        
        if guess_char in self.previous_guesses:
            raise InvalidGuessedLetterException
        
        attempt=self.word.perform_attempt(guess_char)
        self.previous_guesses.append(guess_char)
        
        if attempt.is_miss()==True:
            self.remaining_misses-=1
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()

        
        return attempt
        
    @classmethod
    def select_random_word(self, list_of_words):
        if len(list_of_words)==0:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
    
