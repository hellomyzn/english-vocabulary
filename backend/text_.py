

def get_list_of_example():
    '''Get list including dict from data/examples.txt'''
    
    with open('./data/examples.txt', 'r') as f:
        # SBV = Suplited by Vocabulary
        # SBVAE = Suplited by Vocabulary and Example
        examples_SBV = f.read().split("\n\n")
        examples_SBVAE = {}
        examples = []

        for example in examples_SBV:
            examples_SBVAE['title'] = example.split("\n")[0]
            examples_SBVAE['example_sentence'] = example.split("\n")[1]
            examples.append(examples_SBVAE)
        
    return examples
        