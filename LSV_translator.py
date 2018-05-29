
# coding: utf-8

# In[1]:


from LSV import *
import pyfreeling as freeling
import sys
import re
import pandas as pd


# In[2]:


freeling.util_init_locale("default");
lang = "es" ; ipath = "/usr"
lpath = ipath + "/share/freeling/" + lang + "/"
tk=freeling.tokenizer(lpath+"tokenizer.dat");
sp=freeling.splitter(lpath+"splitter.dat");


# In[3]:



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


# In[4]:


exceptions=['^PR0','^P0','^DI','^DA','Fd','Flt','Fla','Fe','Frc','Fra','Fx', 'Faa','Fat','Fia','Fit','Fp']


# In[5]:


categories = txt_to_dict('categories.txt') ; expresions = txt_to_dict('expresions.txt') ; expresions_final = txt_to_dict('expresions_final.txt')
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

