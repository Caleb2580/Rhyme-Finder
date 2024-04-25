import nltk
from nltk.corpus import wordnet as wn

arpabet = nltk.corpus.cmudict.dict()


# def words_ending_with_phoneme(phonemes):
#     words = [word for word, pronunciations in arpabet.items() if (pronunciations[-1][-2] == phonemes[-2] and pronunciations[-1][-1] == phonemes[-1])]
#     return words

# def words_ending_with_phoneme(phonemes):
#     new_arpabet = [(w, p) for w, p in arpabet.items() if len(p[-1]) >= len(phonemes)]
#     words = [word for word, pronunciations in new_arpabet if ''.join(pronunciations[-1][-1 * len(phonemes):]) == ''.join(phonemes)]

#     # words = [word for word, pronunciations in new_arpabet if (pronunciations[-1][-2] == phonemes[-2] and pronunciations[-1][-1] == phonemes[-1])]
#     return words

def words_ending_with_phoneme(phonemes):
    new_arpabet = [(w, p) for w, p in arpabet.items() if len(p[-1]) >= len(phonemes)]
    words = [word for word, pronunciations in new_arpabet if ''.join(pronunciations[-1][-1 * len(phonemes)]) == ''.join(phonemes)]

    # words = [word for word, pronunciations in new_arpabet if (pronunciations[-1][-2] == phonemes[-2] and pronunciations[-1][-1] == phonemes[-1])]
    return words


def words_starting_with_phoneme(phonemes):
    new_arpabet = [(w, p) for w, p in arpabet.items() if len(p[-1]) >= len(phonemes)]
    words = [word for word, pronunciations in new_arpabet if ''.join(pronunciations[-1][:len(phonemes)]) == ''.join(phonemes)]

    # words = [word for word, pronunciations in new_arpabet if (pronunciations[-1][-2] == phonemes[-2] and pronunciations[-1][-1] == phonemes[-1])]
    return words

def remove_digits(w):
    new_w = []
    for _ in w:
        new_w.append(''.join([i for i in _ if not i.isdigit()]))
    return new_w

def get_stress_level(p):
    try:
        sl = int(p[-1])
        return sl
    except:
        return -1


def compare_words(w1, w2, p=False):
    if len(w2) < 3:
        return False
    w1 = remove_digits(w1)
    w2 = remove_digits(w2)
    start = []
    current_w1 = w1.copy()
    rhymes = []
    for w1_letter in range(0, len(w1)):
        current_w1 =  w1[w1_letter:]
        current_rhymes = start + []
        for w2_letter in w2:
            if len(current_w1) == 0:
                rhymes.append( current_rhymes )
                break

            try:
                index = current_w1.index(w2_letter)
                if index > -1:
                    current_rhymes.append( w2_letter )
                    current_w1 = current_w1[index+1:]
                else:
                    current_rhymes.append( '_' )
            except:
                current_rhymes.append( '_' )
        rhymes.append(current_rhymes)

    types = {
        'bme': 0,
        'beg_end': 0,
        'middle_end': 0,
        'end': 0,
        'beg': 0,
        'beg_middle': 0
    }
    for r in rhymes:
        if len(r) == 1:
            types['beg'] += 1
            break
        if r[0] != '_':  # Beginning rhymes
            if r[-1] != '_':
                if r[-2] != '_':
                    types['beg_end'] += 2
                else:
                    types['beg_end'] += 1
                for r_2 in r[1:-1]:
                    if r_2 != '_':
                        types['bme'] += 1
            elif r[-2] != '_':
                if len(w2) > 3:
                    types['beg_end'] += .5
                    for r_2 in r[1:-2]:
                        if r_2 != '_':
                            types['bme'] += .5
                else:
                    types['beg_middle'] += 1
            else:
                if len(w2) > 3:
                    for r_2 in r[1:-2]:
                        if r_2 != '_':
                            types['beg_middle'] += 1
                else:
                    types['beg'] += 1
        elif r[-1] != '_':
            if r[-2] != '_':
                types['end'] += 2
            else:
                types['end'] += 1
            for r_2 in r[1:-1]:
                if r_2 != '_':
                    types['middle_end'] += 1
        elif r[-2] != '_':
            if len(w2) > 3:
                types['end'] += .5
                for r_2 in r[1:-2]:
                    if r_2 != '_':
                        types['middle_end'] += .5
    
    if w1[0] != w2[0]:
        types['beg'] = 0
        types['beg_middle'] = 0
        types['beg_end'] = 0

    if p:
        print( f'Types: {types}' )

        print(f'Rhymes: {rhymes}')
    if types['beg_end'] > 0:
        return True
    else:
        return False

def compare_words_stressed(w1, w2, p=False):
    w1_stressed = [w for w in w1 if get_stress_level(w) > -1]
    w2_stressed = [w for w in w2 if get_stress_level(w) > -1]
    if ''.join(w1_stressed) == ''.join(w2_stressed):

        return True
    return False


def get_rhymes(word):
    error = False
    try:
        w1_p = arpabet[word][-1]
    except:
        error = True

    rhymes = []
    extra_rhymes = []

    if error:
        print(f"Couldn't find {word}")
        return
    else:
        w1_stressed = [w for w in w1_p if get_stress_level(w) > -1]
        end_phs = w1_p[w1_p.index(w1_stressed[-1])+1:]
        for w in words_ending_with_phoneme(end_phs):
            w2_p = arpabet[w][-1]
            if compare_words_stressed(w1_p, w2_p):
                rhymes.append(w)
        if len(rhymes) == 0:
            print('No rhymes')
            for w in arpabet:
                w2_p = arpabet[w][-1]
                if compare_words_stressed(w1_p, w2_p):
                    rhymes.append(w)
        else:
            extra = []
            for w in arpabet:
                w2_p = arpabet[w][-1]
                if compare_words_stressed(w1_p, w2_p) and w not in rhymes:
                    extra_rhymes.append(w)
    print(rhymes)
    print("\n\n\n")
    print('Extra: ', extra_rhymes)



# def get_rhymes(word):
#     # print(matching_words)

#     w1 = 'rapper'
#     w2 = 'rafter'

#     w1 = 'rapper'
#     w2 = 'spur'


#     error = False

#     try:
#         w1_p = arpabet[w1][-1]
#         w2_p = arpabet[w2][-1]
#         print(w1_p, w2_p)
#     except Exception as e:
#         print(f"Couldn't find {e}")
#         error = True


#     if not error:
#         compare_words(w1_p, w2_p)
#     else:
#         print('Error')

#     # try:
#     #     w = arpabet['rubber'][-1]
#     #     print(w)
#     #     wds = words_ending_with_phoneme(w[-2:])
#     #     print(wds)
#     #     print('----')
#     #     wds = words_starting_with_phoneme(w[:3])
#     #     print(wds)
#     # except Exception as e:
#     #     print(f"Couldn't find {e}")


def main():
    word = 'verge'
    get_rhymes(word)



main()









