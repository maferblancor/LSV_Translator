
# coding: utf-8

# In[191]:


import pyfreeling as freeling
import sys
import re
import pandas as pd


# In[3]:


def txt_to_dict(file_path):
    final_list = ''
    with open(file_path) as lines:
        for lineItem in lines:
            attribute = lineItem.split(':')[0]
            try:
                value = lineItem.split(':')[1]
            except:
                value = lineItem
                #print ('--->Falta por clasificar')
            final_list = final_list + (attribute+':'+value+',')
    final_list = final_list.rstrip(',').replace('\n','').replace(' ','') 
    lines_dict = dict((k,v) for k, v in (e.split(':') for e in final_list.split(',')))
    return lines_dict


# In[4]:


def my_maco_options(lang,lpath) :

    # create options holder 
    opt = freeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not 
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = "";
    opt.LocutionsFile = lpath + "locucions.dat"; 
    opt.AffixFile = lpath + "afixos.dat";
    opt.ProbabilityFile = lpath + "probabilitats.dat"; 
    opt.DictionaryFile = lpath + "dicc.src";
    opt.NPdataFile = lpath + "np.dat"; 
    opt.PunctuationFile = lpath + "../common/punct.dat"; 
    return opt;


# In[5]:


def get_re_value(line, re_value, group_number = 0): 
    value = re.search(re_value,line)
    if not value:
        return None 
    value = value.group(group_number)
    return value


# In[6]:


def clean_input(token, list_):
    for iterator in list_:    
        val = get_re_value(token, iterator)
        if val:
            return True
    return False


# In[244]:


def is_something(syns,categories):
    is_top = False
    is_label = False
    for syn in syns:
        while not is_label:
            si = sdb.get_sense_info(syn)
            for label in categories:
                is_label = (si.sumo == label)
                if is_label:
                    is_top = True
                    break
                else:
                    if len(si.parents) > 0 :
                        syn = si.parents[0]
                        continue
                    else:
                        is_top = True
                        is_label = 'NoValid'
                        break
        if is_label != 'NoValid':
            return (categories[label])
    return False


# In[8]:


def is_sumo_tag(syns,label):
    is_top = False
    is_label = False
    while not is_label:
        si = sdb.get_sense_info(syns)
        is_label = (si.sumo == label)
        if is_label:
            is_top = True
            break
        else:
            if len(si.parents) > 0 :
                syns = si.parents[0]
                continue
            else:
                is_top = True
                is_label = 'NoValid'
                break
    if is_label != 'NoValid':
        return (label)
    return False


# In[163]:


def analize_gender_number(tag):
    #DAOFS0
    #gender = [3]
    #number = [4]
    gender = '' ; number = ''
    if tag[3] == 'F' or tag[2] == 'F': gender = '(F)'
    if tag[3] == 'M' or tag[2] == 'M': gender = ''
    if tag[3] == 'N' or tag[2] == 'N': gender = ''
    if tag[4] == 'S' or tag[3] == 'S': number = ''
    if tag[4] == 'P' or tag[3] == 'P': number = '(x2)'
    if tag[4] == 'N' or tag[3] == 'N': number = ''
    return (gender, number)    
        
    


# In[221]:


def is_syns_tag(syns,label):
    is_top = False ; is_label = False
    for syn in syns:
        while not is_label and not is_top:
            si = sdb.get_sense_info(syn)
            is_label = (si.sumo == label)
            if is_label:
                is_top = True
                return True
            else:
                if len(si.parents) > 0 :
                    syn = si.parents[0]
                else:
                    is_top = True
        is_top = False ; is_label = False
    return False
    


# In[91]:


def get_time(tag):    
    if tag[3] == 'P' or tag[2] == 'G' : return 'Presente'
    if tag[3] == 'F' : return 'Futuro'
    if tag[3] == 'S' or tag[3] == 'I'  : return 'Pasado'
    return ''
    


# In[140]:


def get_word_info(word):
    if len(word.get_senses())>0:
        try:
            syns = (word.get_senses()[0][0],word.get_senses()[1][0])
        except:
            syns = (word.get_senses()[0][0])
    else:
        syns = '' 
    return word.get_tag(),word.get_lemma(),word.get_form(),syns


# In[150]:


def get_expresions(tag,expresions, expresions_final):
    expre = ''
    if tag[0:3] in expresions_final:
        expre = (expresions_final[tag[0:3]])
        expre = ''
    else:
        if tag[0:3] in expresions:
            expre =(expresions[tag[0:3]])
    return expre


# In[159]:


def spell(name): 
    spell_name = ''
    for letter in name:
        spell_name = spell_name +str.upper(letter)+ '-'
    return spell_name.rstrip('-')


# In[212]:


def get_number(tag):
    if tag[3] == 'P' : return 'X2'
    return False


# In[240]:


def ProcessSentences(ls, sdb,exceptions,categories,expresions, expresion_final):    
    expre = '' ; gender = ''; number = '' ; time = '' ; verb_aux = False ; verb_number = False
    out = {'tag':[],'lemma':[],'word':[],'expresion':[],'number':[],'gender':[],'time':[]}
    for s in ls :
        for w, itera in zip(s , range(len(s))):    
            tag,lemma,word,syns = get_word_info(w)
            prev_word_tag,prev_word_lemma,prev_word_form, prev_word_syns = get_word_info(s[itera-1])
            expre = get_expresions(tag, expresions, expresions_final)
            if tag[0] == 'N':
                if (tag[0:2] == 'NC'):
                    if not is_syns_tag(syns,'Human='):
                        verb_number = get_number(tag)
                        gender = '' ; number =''
                    else:
                        (gender, number)= analize_gender_number(tag)
                else:
                    #Se deletran los nombres propios.
                    lemma = spell(word)         
            if tag[0:2] == 'DA' or tag[0:2] == 'DI':
                (gender,number) = analize_gender_number(tag) 
                #continue
            if tag[0] == 'V':
                if verb_number:
                    number = verb_number
                if (tag[0:2] == 'VA' or tag[0:2] == 'VS'):
                    time = get_time(tag)
                    verb_aux = True
                elif tag[0:2] == 'VM':
                    if verb_aux == False:
                        time = get_time(tag)
                    #Es verbo principal
            #Reviso la pertenencia al contexto 
            tok = is_something(syns,categories)
            if tok:
                lemma = tok
            if (clean_input(list_=exceptions,token=tag) or lemma == 'estar' or lemma == 'ser'):
                continue
            out['tag'].append(tag);out['lemma'].append(str.upper(lemma));out['word'].append(word)
            out['expresion'].append(expre);out['gender'].append(gender);out['number'].append(number);out['time'].append(time)
            gender = '';number =''; time =''     
    return out


# In[219]:


freeling.util_init_locale("default");
lang = "es" ; ipath = "/usr"
lpath = ipath + "/share/freeling/" + lang + "/"
tk=freeling.tokenizer(lpath+"tokenizer.dat");
sp=freeling.splitter(lpath+"splitter.dat");
morfo=freeling.maco(my_maco_options(lang,lpath));
morfo.set_active_options (False,  # UserMap 
                          True,  # NumbersDetection,  
                          True,  # PunctuationDetection,   
                          True,  # DatesDetection,    
                          True,  # DictionarySearch,  
                          True,  # AffixAnalysis,  
                          False, # CompoundAnalysis, 
                          True,  # RetokContractions,
                          True,  # MultiwordsDetection,  
                          True,  # NERecognition,     
                          False, # QuantitiesDetection,  
                          True); # ProbabilityAssignment                 
tagger = freeling.hmm_tagger(lpath+"tagger.dat",True,2)
# create sense annotator
sen = freeling.senses(lpath+"senses.dat");
# create sense disambiguator
wsd = freeling.ukb(lpath+"ukb.dat");
sdb = freeling.semanticDB(lpath+"semdb.dat");


# In[223]:


exceptions=['^PR0','^P0','^DI','^DA','Fd','Flt','Fla','Fe','Frc','Fra','Fx', 'Faa','Fat','Fia','Fit','Fp']
categories = txt_to_dict('categories.txt') ; expresions = txt_to_dict('expresions.txt') ; expresions_final = txt_to_dict('expresions_final.txt')


# In[245]:


text = ''; prev_expre = ''; order = ['tag','lemma','word','expresion','gender','number','time']
f = open ('out.txt','w')
with open('input.txt') as lineas:    
    for text in lineas:
        if text == '':
            break
        lw = tk.tokenize(text.replace('\n',''))
        # split list of words in sentences, return list of sentences
        ls = sp.split(lw)

        # perform morphosyntactic analysis and disambiguation
        ls = morfo.analyze(ls)
        ls = tagger.analyze(ls)
        ls = sen.analyze(ls);
        ls = wsd.analyze(ls);
        # create semantic DB module
        
        # do whatever is needed with processed sentences 
        print ('Input:'+text+'\n')
        print ('Output:'+'\n')
        out = ProcessSentences(ls,sdb, exceptions, categories, expresions, expresions_final)
        out = pd.DataFrame(out)
        print (out[order])
        print ('\n')
        f.write('\nInput:'+text+'\n')
        f.write('Output:'+'\n')
        f.write(out[order].to_string())
        f.write('\n')
f.close()

