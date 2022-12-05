
land_types = ["Forest", "Plains", "Mountain", "Island", "Swamp"]

def handle_search(effect):
    if(type(effect)==list):
        print(effect)
        for s in effect:
            #do some other stuff
            if("search your library for" in s):
                spl = s.split(' ')
                f = spl.index("library")
                if(spl[f+1]=="for"):
                    search_str = []
                    for l in land_types:
                        if(l in s):
                            search_str.append(l)
                    return "this searches for: "+str(search_str)+" which are lands"
    if(type(effect)==str):
        return "do the string stuff"