import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-hi")

def hindiToHinglish(sentence):
    consonant = {'क':['ka','k'],'ख':['kha','kh'],'ग':['ga','g'],'घ':['gha','gh'],'च':['cha','ch'],'छ':['chha','chh'],'ज':['ja','j'],'झ':['jha','jh'],'ट':['ta','t'],'ठ':['tha','th'],'ड':['da','d'],'ढ':['dha','dh'],'त':['ta','t'],'थ':['tha','th'],'द':['da','d'],'ध':['dha','dh'],'न':['na','n'],'प':['pa','p'],'फ':['pha','ph'],'ब':['ba','b'],'भ':['bha','bh'],'म':['ma','m'],'य':['ya','y'],'र':['ra','r'],'ल':['la','l'],'व':['va','v'],'श':['sha','sh'],'स':['sa','s'],'ह':['ha','h'],'ञ':['gya','gy'],'ण':['da','d']}
    vowel = {'अ':['a'],'आ':['aa'],'इ':['e'],'ई':['e'],'उ':['u'],'ऊ':['u'],'ए':['e'],'ऐ':['ae'],'ओ':['o'],'औ':['ao'],'ा':['a'],'ि':['i'],'ी':['ee'],'ु':['u'],'ू':['u'],'े':['e'],'ै':['ae'],'ो':['o'],'ौ':['ao'],'ं':['n'],'ँ':['n'],'्':['a'], '़':[''],'ः':['ah']}
    words = sentence.split(' ')
    eng = ''
    for j in range(len(words)):
        w = words[j]
        for i in range(len(w)):
            char = w[i]
            if char in vowel:
                eng += vowel[char][0]
            elif char in consonant:
                if i+1 == len(w) or i+1 < len(w) and w[i+1] in vowel:
                    eng += consonant[char][1]
                else:
                    eng += consonant[char][0]
            else:
                eng += char
        eng += ' '
    return eng.strip()

def englishToHindi(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt")
    outputs = model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)
    hindi = tokenizer.decode(outputs[0])
    return hindi.strip()

def englishToHinglish(sentence):
    return hindiToHinglish(englishToHindi(sentence))


st.title("App to translate English sentence to Hindi & Hinglish")

st.subheader("Enter text in English")
text = st.text_input('Enter text') #text is stored in this variable

st.header("Translated text")

hindi_text = englishToHindi(text)
st.subheader("Hindi")
st.write(hindi_text.strip())

hinglish_text = hindiToHinglish(hindi_text)
st.subheader("Hinglish")
st.write(hinglish_text)