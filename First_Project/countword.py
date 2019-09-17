import pathlib
from typing import List #imports List data structure


def count_words(text:List[str]):
   word_dict = {} #creates a blank dictionary
   for line in text: #loop that goes through each line of the List os lines
      wordsOfLine = line.split(" ") # breaks apart each line of text from spaces
      for word in wordsOfLine: # another loop is created to go through each word in a given line
         rstripWord = word.rstrip("!@#$%^&*()_,./:;'\"?\n")  #a given word from the current loop iteration has special stripped off from the Right side
         cleanWord = rstripWord.lstrip("!@#$%^&*()_,./:;'\"?\n""") # final word product after rstripWord has special characters stripped off from the Left side
            if cleanWord in word_dict:
                word_dict[cleanWord] = word_dict[cleanWord]+1
            else:
                word_dict[cleanWord] = 1
        return

    return word_dict



def main():
    story = open("book-war-and-peace.txt", "r")
    all_lines = story.readlines()
    product = count_words(all_lines)
    print(product)
main()