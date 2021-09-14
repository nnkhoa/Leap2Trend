'''
TRAIN MODEL
Takes a text file, trains it into a word2vec model.
REQUIRES
+ gensim
'''
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import models, matutils


input_filename =  'data_full/paper_content_2010.txt'		# file of text to train on
model_filename =  'models/fresh_model_2010.model'		# name for saving trained model

# train using skip-gram?
# (ignore unless you wanna do detailed tweaking)
skip_gram = True


# create vocabulary
print ('building vocabulary...')
model = models.Word2Vec()
sentences = models.word2vec.LineSentence(input_filename)
model.build_vocab(sentences)
bigram_transformer = models.Phrases(sentences)
model = models.Word2Vec(bigram_transformer[sentences], vector_size=200, min_count=10, window=6)



# train model
print ('training model...')
if skip_gram:
    #model.train(bigram_transformer[sentences], sg=1)
    model.train(bigram_transformer[sentences], total_examples=model.corpus_count, epochs=model.epochs)
    #(sentences, total_examples= model.corpus_count, epochs= model.iter)
else:
    #model.train(sentences)
    model.train(bigram_transformer[sentences], total_examples=self.corpus_count, epochs=self.epochs, vector_size=200, min_count=5, window=6)


# and save
print ('- saving model...')
model.save(model_filename)

# bye
print ('all done, thank you!')
