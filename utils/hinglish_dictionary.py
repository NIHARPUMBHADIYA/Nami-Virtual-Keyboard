

HINGLISH_WORDS = {

    'namaste': 'nuh-muh-stay',
    'namaskar': 'nuh-muh-skar',
    'namaskaram': 'nuh-muh-ska-rum',
    'pranam': 'pruh-naam',
    'jai': 'jay',
    'ram': 'raam',

    'maa': 'maa',
    'papa': 'paa-paa',
    'bhai': 'bhai',
    'behen': 'beh-hen',
    'didi': 'dee-dee',
    'dada': 'daa-daa',
    'nana': 'naa-naa',
    'nani': 'naa-nee',
    'chacha': 'chaa-chaa',
    'chachi': 'chaa-chee',
    'mama': 'maa-maa',
    'mami': 'maa-mee',
    'beta': 'bay-taa',
    'beti': 'bay-tee',

    'acha': 'uh-chaa',
    'accha': 'uh-chaa',
    'theek': 'teek',
    'thik': 'teek',
    'haan': 'haan',
    'nahi': 'nuh-hee',
    'nahin': 'nuh-heen',
    'kya': 'kyaa',
    'kaise': 'kai-say',
    'kaisa': 'kai-saa',
    'kahan': 'kuh-haan',
    'kab': 'kub',
    'kyun': 'kyoon',
    'kyon': 'kyoon',

    'chai': 'chai',
    'pani': 'paa-nee',
    'roti': 'row-tee',
    'dal': 'daal',
    'sabzi': 'sub-zee',
    'dahi': 'duh-hee',
    'ghee': 'ghee',
    'mithai': 'mit-hai',
    'khana': 'khaa-naa',
    'nashta': 'naash-taa',
    'samosa': 'suh-mow-saa',
    'pakora': 'puh-kow-raa',
    'biryani': 'beer-yaa-nee',
    'masala': 'muh-saa-laa',
    'paneer': 'puh-neer',

    'bahut': 'buh-hut',
    'bohot': 'buh-hut',
    'thoda': 'tow-daa',
    'zyada': 'zyaa-daa',
    'jyada': 'zyaa-daa',
    'kam': 'kum',
    'sahi': 'suh-hee',
    'galat': 'guh-lut',
    'khush': 'khoosh',
    'dukhi': 'dook-hee',
    'pyaar': 'pyaar',
    'pyar': 'pyaar',

    'aao': 'aa-oh',
    'jao': 'jaa-oh',
    'karo': 'kuh-row',
    'dekho': 'day-kow',
    'suno': 'soo-now',
    'bolo': 'bow-low',
    'khao': 'khaa-oh',
    'piyo': 'pee-yow',
    'socho': 'sow-chow',
    'samjho': 'sum-jow',
    'loda':'loo-daa',

    'kal': 'kul',
    'aaj': 'aaj',
    'abhi': 'ub-hee',
    'baad': 'baad',
    'pehle': 'pay-lay',
    'phir': 'feer',
    'kabhi': 'kub-hee',

    'ghar': 'ghar',
    'school': 'school',
    'office': 'office',
    'bazaar': 'buh-zaar',
    'mandir': 'mun-deer',
    'masjid': 'mus-jid',
    'gurudwara': 'goo-roo-dwaa-raa',

    'kuch': 'kooch',
    'bhi': 'bee',
    'baat': 'baat',
    'cheez': 'cheez',
    'log': 'log',
    'sab': 'sub',
    'yeh': 'yay',
    'woh': 'woh',
    'yahan': 'yuh-haan',
    'wahan': 'wuh-haan',
    'idhar': 'id-har',
    'udhar': 'ood-har',

    'ek': 'ake',
    'do': 'doh',
    'teen': 'teen',
    'char': 'chaar',
    'paanch': 'paanch',
    'panch': 'paanch',
    'chhe': 'chay',
    'saat': 'saat',
    'aath': 'aath',
    'nau': 'now',
    'das': 'dus',

    'ji': 'jee',
    'sahab': 'saa-hub',
    'sahib': 'saa-hib',
    'madam': 'maa-dum',
    'sir': 'sir',
    'bhaiya': 'bhai-yaa',
    'dada': 'daa-daa',

    'arrey': 'uh-ray',
    'arre': 'uh-ray',
    'oye': 'oh-yay',
    'yaar': 'yaar',
    'bas': 'bus',
    'chalo': 'chuh-low',
    'achha': 'uh-chaa',
    'shukriya': 'shook-ree-yaa',
    'dhanyavaad': 'dhan-yuh-vaad',
    'meherbani': 'may-her-baa-nee',
}

def convert_to_hinglish_phonetic(text):

    words = text.lower().split()
    converted_words = []

    for word in words:

        clean_word = word.strip('.,!?;:')

        if clean_word in HINGLISH_WORDS:

            phonetic = HINGLISH_WORDS[clean_word]

            if word != clean_word:
                punctuation = word[len(clean_word):]
                converted_words.append(phonetic + punctuation)
            else:
                converted_words.append(phonetic)
        else:

            converted_words.append(word)

    return ' '.join(converted_words)

def is_hinglish_text(text):

    words = text.lower().split()
    for word in words:
        clean_word = word.strip('.,!?;:')
        if clean_word in HINGLISH_WORDS:
            return True
    return False
