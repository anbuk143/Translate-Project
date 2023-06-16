import csv
import time
import psutil


def load_dictionary(DictionaryFile):
    dictionary = {}
    with open(DictionaryFile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            english_word, french_word = row
            dictionary[english_word] = french_word
    return dictionary


def get_process_memory_size():  # To find the Memory taken to process
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 * 1024)
    return memory_usage


def replace_words(InputFile, FindwordsFile, DictionaryFile, OutputFile):
    dictionary = load_dictionary(DictionaryFile)
    start_time = time.time()
    with open(InputFile, 'r') as input_doc, open(OutputFile, 'w') as output_doc, open(FindwordsFile,
                                                                                      'r') as find_words_doc, open(
            "frequency.csv", 'w') as frequency_doc:
        words_to_replace = find_words_doc.read().splitlines()
        num_replacements = 0
        replaced_words = set()
        frequency_writer = csv.writer(frequency_doc)
        frequency_writer.writerow(["English word", "French word", "Frequency"])
        frequency_count = {}

        for line in input_doc:
            words = line.split()
            replaced_line = []
            for word in words:
                if word in words_to_replace:
                    if word in dictionary:
                        word = dictionary[word]
                        num_replacements += 1
                        replaced_words.add(word)

                        if word not in frequency_count:
                            frequency_count[word] = 1
                        else:
                            frequency_count[word] += 1
                    else:
                        print(f"Warning: No translation found for word '{word}'")
                replaced_line.append(word)
            replaced_line = ' '.join(replaced_line)
            output_doc.write(replaced_line + '\n')

        for english_word, french_word in dictionary.items():
            frequency_writer.writerow([english_word, french_word, frequency_count.get(french_word, 0)])

    end_time = time.time()
    time_taken = end_time - start_time
    memory_usage = get_process_memory_size()
    print(f"Number of times a word was replaced: {num_replacements}")
    print(f"Time taken for this process: {time_taken:.2f} seconds")
    print("Unique list of words that were replaced with French words from the dictionary:\n", ',\n '.join(replaced_words))
    print(f"Total memory size of the process: {memory_usage:.2f} MB")


InputFile = 't8.shakespeare.txt'
FindwordsFile = 'find_words.txt'
DictionaryFile = 'french_dictionary.csv'
OutputFile = 'Output.txt'

replace_words(InputFile, FindwordsFile, DictionaryFile, OutputFile)
