from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.APIFuzzer import INT_GRAMMAR, FLOAT_GRAMMAR, ASCII_STRING_GRAMMAR, LIST_GRAMMAR
from fuzzingbook.Grammars import EXPR_GRAMMAR, URL_GRAMMAR
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
import json, random, fuzzingbook, string, sys, os
import fuzzingbook.MutationFuzzer as MutationFuzzer
import azure_blob.driver as BlobDriver
import azure_queue.driver as QueueDriver
import azure_table.driver as TableDriver
import s3.driver as S3Driver
import dynamodb.driver as DynamoDBDriver



JSON_GRAMMAR = json.loads(open('grammar/json_grammar.json').read())['0']

if __name__ == '__main__':

    # take service type as argument and exit if no argument
    if len(sys.argv) < 2:
        print('Please specify service type from the following:')
        print('1: Azure Blob')
        print('2: Azure Queue')
        print('3: Azure Table')
        print('4: S3')
        print('5: DynamoDB')
        sys.exit()

    services = {'1': 'azure_blob', '2': 'azure_queue', '3': 'azure_table', '4': 's3', '5': 'dynamodb'}

    service_type = services[sys.argv[1]]

    if service_type == 'azure_blob':
        driver = BlobDriver
    elif service_type == 'azure_queue':
        driver = QueueDriver
    elif service_type == 'azure_table':
        driver = TableDriver
    elif service_type == 's3':
        driver = S3Driver
    elif service_type == 'dynamodb':
        driver = DynamoDBDriver


    int_fuzzer = ProbabilisticGeneratorGrammarFuzzer(INT_GRAMMAR)
    float_fuzzer = ProbabilisticGeneratorGrammarFuzzer(FLOAT_GRAMMAR)
    # string_fuzzer = ProbabilisticGeneratorGrammarFuzzer(ASCII_STRING_GRAMMAR)
    # url_fuzzer = ProbabilisticGeneratorGrammarFuzzer(URL_GRAMMAR)

    list_fuzzer_int = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(INT_GRAMMAR))
    list_fuzzer_float = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(FLOAT_GRAMMAR))
    list_fuzzer_string = ProbabilisticGrammarFuzzer(fuzzingbook.APIFuzzer.list_grammar(ASCII_STRING_GRAMMAR))


    # load input from file
    with open(f'in/{service_type}.json', 'r') as f:
        input_data = f.read()

    if not os.path.exists(f'logs/{service_type}'):
        os.mkdir(f'logs/{service_type}')

    # create log files
    with open(f'logs/{service_type}/discrepancy.txt', 'w') as f:
            f.write('')

    with open(f'logs/{service_type}/discrepant_methods.txt', 'w') as f:
        f.write('')

    with open(f'logs/{service_type}/discrepant_sequences.txt', 'w') as f:
        f.write('')

    with open(f'logs/{service_type}/log_all.txt', 'w') as f:
        f.write('')

    # simple run with default input
    driver.main(())
    
    input_data = json.loads(input_data)

    driver.main(input_data)
    
    config = json.loads(open('config.json').read())

    # iterate through json object and mutate
    fuzzing_rounds = config['fuzzing_rounds']
    for i in range(fuzzing_rounds):
        for key, _ in input_data.items():
            list_fuzzer = random.choice([list_fuzzer_int, list_fuzzer_float, list_fuzzer_string])

            for i in range(len(input_data[key])):

                # if input_data[key][i] == []:
                #     input_data[key][i] = None
                #     continue

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


        # print(input_data)
        driver.main(input_data)
