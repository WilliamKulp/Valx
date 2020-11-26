try:
    from .Valx.W_utility.file import *
    from .Valx.W_utility.log import ext_print
    from .Valx import Valx_core
except ImportError:
    from Valx.W_utility.file import *
    from Valx.W_utility.log import ext_print
    from Valx import Valx_core
    
import os,sys,re
from tqdm import tqdm_notebook
import pandas as pd

class valex_ie_parser:
    def __init__(self,debug=False,ffea='Valx/data/variable_features_dk.csv',
                        ffea2='Valx/data/variable_features_umls.csv',var='All'):
        self.debug=debug
        self.ffea = ffea
        self.ffea2 = ffea2
        self.var = var


    def extract_variables (self,trials,fdin):
        # read input data
    #     if fdin is None or fdin =="": return False
    #     trials = pd.read_csv(fdin,header=None)
        if trials is None or len(trials) <= 0:
            print(ext_print ('input data error, please check either no such file or no data --- interrupting'))
            return False
        print(ext_print ('found a total of %d data items' % len(trials)))
        
        # read feature list - domain knowledge
        if self.ffea is None or self.ffea =="": return False
        fea_dict_dk = read_csv_as_dict_with_multiple_items (self.ffea)
        if fea_dict_dk is None or len(fea_dict_dk) <= 0:
            print(ext_print ('no feature data available --- interrupting'))
            return False

        # get feature info
        features, feature_dict_dk = {}, {}
        if self.var == "All":
            features = fea_dict_dk
            del features["Variable name"]
        elif self.var in fea_dict_dk:
            features = {self.var:fea_dict_dk[self.var]}
        for key, value in fea_dict_dk.items():
            names = value[0].lower().split('|')
            for name in names:
                if name.strip() != '': feature_dict_dk[name.strip()] =key

        # read feature list - UMLS (can be replaced by full UMLS)
        if self.ffea2 is None or self.ffea2 =="": return False
        fea_dict_umls = read_csv_as_dict (self.ffea2)
        if fea_dict_umls is None or len(fea_dict_umls) <= 0:
            print(ext_print ('no feature data available --- interrupting'))
            return False

        #load numeric feature list
        Valx_core.init_features()

        output = []
        for i in tqdm_notebook(range(0,len(trials))):
            if i%1000 == 0:
                print ('processing %d' % i)
            # pre-processing eligibility criteria text
            text = Valx_core.preprocessing(trials.iloc[i,1]) # trials[i][1] is the eligibility criteria text
            if self.debug: print(text)
            (sections_num, candidates_num) = Valx_core.extract_candidates_numeric(text) # extract candidates containing numeric features
            for j in range(0,len(candidates_num)): # for each candidate
                if self.debug: print(f"Criteria {j} : {text}")
                exp_text = Valx_core.formalize_expressions(candidates_num[j]) # identify and formalize values
                if self.debug: print(f"formalize_expressions 1 {j} : {exp_text}")
                (exp_text, key_ngrams) = Valx_core.identify_variable(exp_text, feature_dict_dk, fea_dict_umls) # identify variable mentions and map them to names
                if self.debug: print(f"formalize_expressions 2 {j} : {exp_text}")
                if self.debug: print(f"key_ngrams {j} : {key_ngrams}")
                (variables, vars_values) = Valx_core.associate_variable_values(exp_text)
                if self.debug: print(f"variables {j} : {variables}")
                if self.debug: print(f"vars_values {j} : {vars_values}")
    #             print(variables,vars_values)
                all_exps = []
                for k in range(0,len(variables)):
                    curr_var = variables[k]
                    curr_exps = vars_values[k]
                    if curr_var in features:
                        fea_list = features[curr_var]
                        curr_exps = Valx_core.context_validation(curr_exps, fea_list[1], fea_list[2])                           
                        curr_exps = Valx_core.normalization(fea_list[3], curr_exps) # unit conversion and value normalization
                        curr_exps = Valx_core.hr_validation (curr_exps, float(fea_list[4]), float(fea_list[5])) # heuristic rule-based validation
                    if len(curr_exps) > 0:
                        if self.var == "All" or self.var.lower() == curr_var.lower() or self.var.lower() in curr_var.lower(): 
                            all_exps += curr_exps                     
    #                 print(curr_var)
    #                 print(curr_exps)
                if len(all_exps) > 0: 
                    output.append((trials.iloc[i,0], sections_num[j], candidates_num[j], exp_text, str(all_exps).replace("u'", "'"))) # output result
    #         break
        # output result
        fout = os.path.splitext(fdin)[0] + "_exp_%s_out.csv" % self.var
        pd.DataFrame(output).to_csv(fout,index=None)
        print(ext_print ('saved processed results into: %s' % fout))
        return output,trials.values


    def process_valx_results(original_text, valx_outputs) : 

        word_blocks = get_words_space_blocks(original_text)

        all_words = [word_block['word'] for word_block in word_blocks]

        count_word_blocks = len(word_blocks)

        word_block_index = 0

        result = [] 
        
        for output in valx_outputs : 

            value_exps = output[4]
            value_exps = eval(value_exps)

            for value_exp in value_exps :

                value = value_exp[2]
                unit = value_exp[3]
                value_type = value_exp[0]

                float_count = all_words.count(str(value))
                int_count = all_words.count(str(int(value)))
                value_count =  float_count + int_count

                print(value_exp)
                print('value_count', value_count)
                print(word_block_index)
                if len(result)>0 : 
                    if result[-1]['EntityType'] == value_type and (str(int(value) in get_alphanumeric_groups(result[-1]['Entity'])) or str(value) in get_alphanumeric_groups(result[-1]['Entity'])) : 
                        continue

                if word_block_index == count_word_blocks : 
                    break 

                elif value_count == 1 :
                    if float_count == 1 : 
                        word_block_index = all_words.index(str(value))
                    else : 
                        word_block_index = all_words.index(str(int(value)))

                    if word_block_index <= count_word_blocks - len(unit.split(" ")) - 2 : 
                        word = word_blocks[word_block_index]["word"]
                        word_start_index = word_blocks[word_block_index]['start_index']

                        next_word_blocks = word_blocks[word_block_index+1:word_block_index+len(unit.split(" "))+1]
                        unit_word = " ".join([word_block['word'] for word_block in next_word_blocks])
                        if unit_word == unit : 
                            if len(next_word_blocks) == 0 : 
                                end_index = word_end_index
                            else : 
                                end_index = next_word_blocks[-1]['end_index']
                            result.append({'Entity':" ".join([word, unit]), 
                                           "EntityType":value_type, 
                                           "StartIndex":word_start_index,
                                           "EndIndex":end_index, 
                                           "Confidence":1})
                            word_block_index = word_block_index + len(unit.split(" ")) + 1 

                        else : 
                            result.append({'Entity':word_blocks[word_block_index]['word'], 
                                   'EntityType':value_type, 
                                   'StartIndex':word_blocks[word_block_index]['start_index'],
                                   'EndIndex':word_blocks[word_block_index]['end_index'], 
                                   'Confidence':1
                                  })
                            word_block_index = word_block_index + 1 
                    else : 
                        result.append({'Entity':word_blocks[word_block_index]['word'], 
                                   'EntityType':value_type, 
                                   'StartIndex':word_blocks[word_block_index]['start_index'],
                                   'EndIndex':word_blocks[word_block_index]['end_index'], 
                                   'Confidence':1
                                  })
                        word_block_index = word_block_index + 1 

                else : 
                    while word_block_index < count_word_blocks : 
                        word_block = word_blocks[word_block_index]
                        word = word_block['word']
                        word_start_index = word_block["start_index"]
                        word_end_index = word_block["end_index"]
                        all_alphanumerics = get_alphanumeric_groups(word)

                        if str(value) in all_alphanumerics or str(int(value)) in all_alphanumerics : 
                            if word_block_index <= count_word_blocks - len(unit.split(" ")) - 1 : 
                                next_word_blocks = word_blocks[word_block_index+1:word_block_index+len(unit.split(" "))+1]
                                unit_word = " ".join([word_block['word'] for word_block in next_word_blocks])
                                if unit_word == unit : 
                                    if len(next_word_blocks) == 0 : 
                                        end_index = word_end_index
                                    else : 
                                        end_index = next_word_blocks[-1]['end_index']
                                    result.append({'Entity':" ".join([word, unit]), 
                                                   "EntityType":value_type, 
                                                   "StartIndex":word_start_index,
                                                   "EndIndex":end_index, 
                                                   "Confidence":1
                                                   })
                                    word_block_index = word_block_index + len(unit.split(" ")) + 1 
                                    break 
                        else :
                            if str(value)+unit in all_alphanumerics  or str(int(value))+unit in all_alphanumerics: 
                                result.append({'Entity': word, 
                                               'EntityType':value_type,
                                               'StartIndex':word_start_index,
                                               'EndIndex':word_end_index, 
                                               'Confidence':1
                                              })
                                word_block_index = word_block_index + 1 
                                break 
                        word_block_index = word_block_index + 1

        return result
