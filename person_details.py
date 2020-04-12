import re
import nltk
from nltk.corpus import stopwords
import io

def email(text):
    rmail = re.compile(r'[\w\.-]+@[\w\.-]+')
    email = rmail.search(text)
    if email:
        email=email[0]
    else:
        email = "no email found"
    return email

def linkedin(text):
    rlink = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")
    link = rlink.search(text)
    if link:
        link=link[0]
    else:
        link="no link found"
    return link

def phone(text):
    r = re.compile(r"(([(]?[0-9]{1,3}[)]?)|([(]?[0-9]{4}[)]?))\s*[)]?[-\s\.]?[(]?[0-9]{1,3}[)]?([-\s\.]?[0-9]{3})([-\s\.]?[0-9]{3,4})")
    phone = r.search(text)
    if phone:
        phone=phone[0]
    else:
        phone="Phone number not found"
    return phone

def extract(text):
    pinfo = {}
    if text:
        pinfo['email'] = email(text)
        pinfo['linkedin'] = linkedin(text)
        pinfo['phone'] = phone(text)

        document = text[:int(len(text)/50)]

        stoplist = ["phone","ph","email","linkedin","resume","cv","curriculum vitae","exami"]
        stop = stopwords.words('english')
        stop.extend(stoplist)

        names = []
        document = text[:int(len(text)/50)]
        document = ' '.join([i for i in document.split() if i not in stop])
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        lines = sentences

        names = open("names.txt", "r").read().lower()
        names = set(names.split())

        otherNameHits = []
        nameHits = []
        name = None
        infoDict={}

        grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
        chunkParser = nltk.RegexpParser(grammar)
        all_chunked_tokens = []
        for tagged_tokens in lines:
            if len(tagged_tokens) == 0: continue
            chunked_tokens = chunkParser.parse(tagged_tokens)
            all_chunked_tokens.append(chunked_tokens)
            for subtree in chunked_tokens.subtrees():
                if subtree.label() == 'NAME':
                    for ind, leaf in enumerate(subtree.leaves()):
                        if leaf[0].lower() in names and 'NN' in leaf[1]:
                            hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                            if re.compile(r'[\d,:]').search(hit): continue
                            nameHits.append(hit)
        if len(nameHits) > 0:
            nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits] 
            name = " ".join([el[0].upper()+el[1:].lower() for el in nameHits[0].split() if len(el)>0])
        if name:
            pinfo['name'] = name
        else:
            st = text[:int(len(text)/70)].replace("\t","").replace(pinfo['linkedin'],"").replace(pinfo['email'],"").replace(pinfo['phone'],"").strip().lower()
            st = re.sub(r'[^\w]', ' ', st)
            st = ' '.join([i for i in st.split() if i not in stoplist])
            pinfo['name'] = "Name not found. It may be in string : '"+st+"'"
    else:
        s = "could not extract text from pdf"
        pinfo['email'] = s
        pinfo['linkedin'] = s
        pinfo['phone'] = s
        pinfo['name'] = s
    return pinfo