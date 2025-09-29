import requests
import pandas as pd
import random as rand

def get_site(nom):
    url_end = str(nom.encode('windows-1251')).replace("\\x","%").upper()[2:-1]
    url_full = f"https://starlingdb.org/cgi-bin/morph.cgi?flags=endnnnnn&root=config&word={url_end}"
    site = requests.get(url_full).text
    return site

def get_grammar(site):
    grammar_loc = site.find("Dictionary information")
    grammar = site[grammar_loc+24:grammar_loc+30].split(" ")[0]
    return(grammar)

def get_table(nom):
    url_end = str(nom.encode('windows-1251')).replace("\\x","%").upper()[2:-1]
    url_full = f"https://starlingdb.org/cgi-bin/morph.cgi?flags=endnnnnn&root=config&word={url_end}"
    table_list = pd.read_html(url_full, encoding = 'windows-1251')
    table = table_list[0].melt(id_vars = ["Unnamed: 0"])
    return table

def part_of_speech(grammar):
    if grammar in ["мо", "м", "с", "ж", "со", "жо", "мо-жо"]:
        return "noun"
    elif grammar in ["св", "нсв"]:
        return "verb"
    elif grammar in ["п"]:
        return "adjective"
    else:
        raise NameError(f"Could not identify grammar {grammar}")

def add_word(nom, nouns, adjectives, verbs):
    # TODO clean this line up
    if (len(nouns) > 1 and nom in nouns.columns) or (len(adjectives) > 1 and nom in adjectives.columns) or (len(verbs) > 1 and nom in verbs.columns):
        print("Word already in dictionary :)")
    else:
        table = get_table(nom)
        grammar = get_grammar(get_site(nom))
        match part_of_speech(grammar):
            case "noun":
                table.loc[len(table)] = ["Grammar", "Gender", grammar]
                table = table.rename(columns={"Unnamed: 0": "case", "variable": "plurality", "value": nom})
                nouns = nouns.merge(table, on = ["case","plurality"], how="outer")
            case "adjective":
                table = table.rename(columns={"Unnamed: 0": "case", "variable": "gender", "value": nom})
                adjectives = adjectives.merge(table, on = ["case","gender"], how="outer")
            case "verb":
                table = table.rename(columns={"Unnamed: 0": "person", "variable": "singularity", "value": nom})
                verbs = verbs.merge(table, on = ["person","singularity"], how="outer")
    return nouns, adjectives, verbs       

def view_words(nouns, adjectives, verbs):
    print("viewing words")
    print(f" Nouns: {list(nouns.columns)[3:]}\n Adjectives: {list(adjectives.columns)[3:]}\n Verbs: {list(verbs.columns)[3:]}")

def get_gender(noun, nouns):
    ands = lambda x, y: x and y
    gen_ser = nouns[(nouns["case"] == "Grammar").combine(nouns["plurality"] == "Gender",ands)][noun]
    gen_index = int(gen_ser.index[0])
    gen = gen_ser[gen_index]
    if "м" in gen:
        return "Masculine"
    elif "с" in gen:
        return "Neutral"
    elif "ж" in gen:
        return "Feminine"

def practice(declension, nouns, adjectives):
    print(f"practicing {declension}")
    run = True
    ands = lambda x, y: x and y
    while run:
        noun = rand.choice(list(nouns.columns)[3:])
        adjective = rand.choice(list(adjectives.columns)[3:])
        plurality = rand.choice(["Plural", "Singular"])
        if plurality == "Plural":
            gender = "Plural"
        else:
            gender = get_gender(noun, nouns)
        input(f" Noun: {noun}\n Adjective: {adjective}\n Plurality: {plurality}\n Please decline: ")
        n_series = nouns[(nouns["case"] == declension).combine(nouns["plurality"]== plurality, ands)][noun]
        n_index = int(n_series.index[0])
        a_series = adjectives[(adjectives["case"] == declension).combine(adjectives["gender"]== gender, ands)][adjective]
        a_index = int(a_series.index[0])
        print(f"Correct declension: {n_series[n_index]} {a_series[a_index]}")
        run = (input("Enter 'да' to continue: ")=="да")

def upload(nouns, adjectives, verbs):
    file = input("Enter file path: ")
    with open(file, "r", encoding="utf-8") as word_doc:
        for word in word_doc:
            nouns, adjectives, verbs = add_word(word.strip(), nouns, adjectives, verbs)
    return nouns, adjectives, verbs

def save(nouns, adjectives, verbs):
    print("saving...")
    nouns.to_csv("Nouns.csv")
    adjectives.to_csv("Adjectives.csv")
    verbs.to_csv("Verbs.csv")
    print("saved!")

def menu_select(nouns, adjectives, verbs):
    choice = int(input(''' Please select what you would like to do:
                    1. add word
                    2. view word lists
                    3. practice nominative form
                    4. practice locative form
                    5. practice genitive form
                    6. save tables
                    7. add words from text file
                    8. quit
'''))
    match choice:
        case 1:
            word = input("what word would you like to add? ")
            return tuple([True]) + add_word(word.lower(), nouns, adjectives, verbs) 
        case 2: 
            view_words(nouns, adjectives, verbs)
            return (True, nouns, adjectives, verbs)
        case 3:
            practice("Nominative", nouns, adjectives)
            return (True, nouns, adjectives, verbs)
        case 4:
            practice("Locative", nouns, adjectives)
            return (True, nouns, adjectives, verbs)
        case 5:
            practice("Genitive", nouns, adjectives)
            return (True, nouns, adjectives, verbs)
        case 6:
            save(nouns, adjectives, verbs)
            return (True, nouns, adjectives, verbs)
        case 7:
            return tuple([True]) + upload(nouns, adjectives, verbs)
        case 8:
            return (False, nouns, adjectives, verbs)

def main():
    # TODO
    # add in ability to add study list
    # check if correct
    nouns = pd.read_csv("Nouns.csv")
    adjectives = pd.read_csv("Adjectives.csv")
    verbs = pd.read_csv("Verbs.csv")
    run = True
    while run:
        run, nouns, adjectives, verbs = menu_select(nouns, adjectives, verbs)

if __name__=="__main__":
    main()