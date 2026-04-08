import string

with open('example.txt', 'r', encoding='utf-8') as file:
    text = file.read()

words = text.split()


cleaned_words = []
max_length = 0


for word in words:
    # Удаляем знаки препинания с начала и конца слова
    clean_word = word.strip(string.punctuation)
    if clean_word:  # если слово не пустое
        length = len(clean_word)
        if length > max_length:
            max_length = length
        cleaned_words.append((clean_word, word))


for clean_word, original_word in cleaned_words:
    if len(clean_word) == max_length:
        print(original_word)