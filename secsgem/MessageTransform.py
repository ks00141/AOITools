import re

with open('./s7f25.txt', 'r', encoding='utf-8') as file:
    text = file.read()

text1 = re.sub('[\\\\]', '/', text)
text2 = re.sub('//\s\S', "", text1)
text3 = re.sub('\[.*\]', '', text2)
text4 = re.sub('\'', '\"', text3)
text5 = re.sub('<A>', '<A "">', text4)
text6 = re.sub('"0"', '""', text5)
print(text6)
with open('messageform.txt', 'w', encoding='utf-8') as save_file:
    save_file.write(text6)