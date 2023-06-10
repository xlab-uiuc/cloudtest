from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.APIFuzzer import INT_GRAMMAR, FLOAT_GRAMMAR, ASCII_STRING_GRAMMAR, LIST_GRAMMAR
from fuzzingbook.Grammars import EXPR_GRAMMAR, URL_GRAMMAR
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
import json, random, fuzzingbook, string, sys
import fuzzingbook.MutationFuzzer as MutationFuzzer
sys.path.append('../sdk_tests/Azure Storage')
import driver



JSON_GRAMMAR = [{"name":"John Doe","age":30,"address":"123 Main Street, Anytown, USA"},{"name":"Jane Doe","age":25,"address":"456 Elm Street, Anytown, USA"},{"name":"Apple","price":100},{"name":"Orange","price":50},{"message":"Hello, World!"}]



# create main
if __name__ == '__main__':

    int_fuzzer = ProbabilisticGeneratorGrammarFuzzer(INT_GRAMMAR)
    float_fuzzer = ProbabilisticGeneratorGrammarFuzzer(FLOAT_GRAMMAR)
    # string_fuzzer = ProbabilisticGeneratorGrammarFuzzer(ASCII_STRING_GRAMMAR)
    # url_fuzzer = ProbabilisticGeneratorGrammarFuzzer(URL_GRAMMAR)

    list_fuzzer_int = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(INT_GRAMMAR))
    list_fuzzer_float = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(FLOAT_GRAMMAR))
    list_fuzzer_string = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(ASCII_STRING_GRAMMAR))


    # load input from file
    with open('in/input.json', 'r') as f:
        input_data = f.read()

    # todo: change azure storage to a variable
    with open('../sdk_tests/Azure Storage/discrepancy.txt', 'w') as f:
            f.write('')

    # write to file
    with open('../sdk_tests/Azure Storage/unique_discrepancy.txt', 'w') as f:
        f.write('')

    with open('../sdk_tests/Azure Storage/discrepant_methods.txt', 'w') as f:
        f.write('')

    input_data = json.loads(input_data)

    # to-do: do random input fuzzing instead of property based fuzzing 

    # iterate through json object and mutate
    for i in range(15):
        for key, _ in input_data.items():
            list_fuzzer = random.choice([list_fuzzer_int, list_fuzzer_float, list_fuzzer_string])

            for i in range(len(input_data[key])):
                if input_data[key][i] == []:
                    input_data[key][i] = list(list_fuzzer.fuzz())
                    continue

                for j in range(len(input_data[key][i])):
                    
                    if type(input_data[key][i][j]).__name__ == 'int':
                        input_data[key][i][j] = int_fuzzer.fuzz()
                    elif type(input_data[key][i][j]).__name__ == 'float':
                        input_data[key][i][j] = float_fuzzer.fuzz()
                    elif type(input_data[key][i][j]).__name__ == 'list':
                        input_data[key][i][j] = list_fuzzer.fuzz()
                    elif type(input_data[key][i][j]).__name__ == 'dict':
                        json_fuzz = random.choice(JSON_GRAMMAR)
                        input_data[key][i][j] = json_fuzz
                    else:
                        mutation_fuzzer = MutationFuzzer.MutationFuzzer(seed=[j])
                        input_data[key][i][j] = mutation_fuzzer.fuzz()


        print(input_data)

        
        driver.main(input_data)