import glob
import matplotlib
import matplotlib.pyplot as plt
import wordcloud
import numpy as np
import PIL
import io
import requests
import random
import re

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('french'))

list_files = glob.glob("./content/**/*.qmd", recursive=True)


book_mask = np.array(PIL.Image.open("./build/python_black.png"))


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.readlines()
        f.close()
    new_text = " ".join([line for line in text])
    s = new_text
    return s

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def make_wordcloud(corpus):
    wc = wordcloud.WordCloud(mask=book_mask, max_words=2000, margin=10, contour_width=3, contour_color='white')
    wc.generate(corpus).recolor(color_func=grey_color_func, random_state=3)
    return wc

def keep_text_within_shortword(shortcode):
    return re.sub(re.compile("(\{\{).*(\}\}\\n)|(\\n\{\{).*(\}\})"),"",shortcode)

def clean_file(text):
    text_s = text.split("\n")
    text_s = [line for line in text_s if not line.strip().startswith('#|')]
    text = " ".join(text_s).lower()
    s = keep_text_within_shortword(text)
    s = re.sub(r'(?s)(---)(.*?)(---)', "", s) #remove header
    s = re.sub(r"```\{python\}","", s) #remove python chunk header
    s = re.sub(r'`', '', s)
    return s

list_content = [read_file(fl) for fl in list_files]

corpus = [clean_file(text = files) for files in list_content]
corpus = " ".join(corpus).split(" ")
corpus = [w for w in corpus if not w in stop_words]
#corpus = [word for word in corpus if word.isalpha()]
corpus = " ".join(corpus)


path = './content/home/word.png'

fig = plt.figure()

plt.imshow(make_wordcloud(corpus), interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig(path, bbox_inches='tight', pad_inches = 0, dpi=199)

print(f"Output written : {path}")