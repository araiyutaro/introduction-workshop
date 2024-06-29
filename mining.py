import spacy

nlp = spacy.load("ja_ginza")
text = "隣の客はよく柿食う客だ。"
doc = nlp(text)

# Disable the 'compound_splitter' component
with nlp.disable_pipes('compound_splitter'):
    for token in doc:
        print("{}\t{}\t{}\t{}".format(token, token.lemma_, token.pos_, token.tag_))
