from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import wordnet, brown
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import random
import re

app = Flask(__name__)
CORS(app)

class NLPProcessor:
    def __init__(self):
        self.download_required_data()
    
    def download_required_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        try:
            nltk.data.find('corpora/brown')
        except LookupError:
            nltk.download('brown')
    
    def get_part_of_speech(self, word):
        """Get part of speech for a word"""
        tokens = word_tokenize(word.lower())
        if not tokens:
            return "Unknown"
        
        pos_tags = pos_tag(tokens)
        pos_code = pos_tags[0][1]
        
        # Convert POS tags to readable format
        pos_mapping = {
            'NN': 'Noun', 'NNS': 'Noun (plural)', 'NNP': 'Proper Noun', 'NNPS': 'Proper Noun (plural)',
            'VB': 'Verb', 'VBD': 'Verb (past tense)', 'VBG': 'Verb (gerund)', 'VBN': 'Verb (past participle)',
            'VBP': 'Verb (present)', 'VBZ': 'Verb (3rd person singular)',
            'JJ': 'Adjective', 'JJR': 'Adjective (comparative)', 'JJS': 'Adjective (superlative)',
            'RB': 'Adverb', 'RBR': 'Adverb (comparative)', 'RBS': 'Adverb (superlative)',
            'IN': 'Preposition', 'DT': 'Determiner', 'PRP': 'Pronoun', 'CC': 'Conjunction',
            'MD': 'Modal', 'WP': 'Wh-pronoun', 'WDT': 'Wh-determiner', 'WRB': 'Wh-adverb'
        }
        
        return pos_mapping.get(pos_code, f"Other ({pos_code})")
    
    def get_synonyms_antonyms(self, word):
        """Get synonyms and antonyms using WordNet"""
        synonyms = set()
        antonyms = set()
        
        # Get all synsets for the word
        synsets = wordnet.synsets(word.lower())
        
        for syn in synsets:
            # Add synonyms from all lemmas in the synset
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower() and len(synonym) > 1:
                    synonyms.add(synonym)
            
            # Also add synonyms from related synsets (similar_tos)
            for similar_syn in syn.similar_tos():
                for lemma in similar_syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower() and len(synonym) > 1:
                        synonyms.add(synonym)
        
        # Get antonyms by checking all lemmas across all synsets
        for syn in synsets:
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    for antonym in lemma.antonyms():
                        antonym_name = antonym.name().replace('_', ' ')
                        if len(antonym_name) > 1:
                            antonyms.add(antonym_name)
        
        # If we don't find antonyms in the main word, try related words
        if not antonyms:
            for synonym in synonyms:  # Check all synonyms
                synonym_synsets = wordnet.synsets(synonym.replace(' ', '_'))
                for syn in synonym_synsets:
                    for lemma in syn.lemmas():
                        if lemma.antonyms():
                            for antonym in lemma.antonyms():
                                antonym_name = antonym.name().replace('_', ' ')
                                if len(antonym_name) > 1:
                                    antonyms.add(antonym_name)
        
        # Convert to lists and limit results
        synonyms_list = list(synonyms)[:8]
        antonyms_list = list(antonyms)[:8]
        
        # If still no antonyms found, use common antonym patterns
        if not antonyms_list:
            antonyms_list = self.get_common_antonyms(word.lower())
        
        return synonyms_list, antonyms_list
    
    def get_common_antonyms(self, word):
        """Get antonyms using common patterns when WordNet doesn't have them"""
        common_antonyms = {
            'good': ['bad', 'evil', 'poor', 'terrible'],
            'beautiful': ['ugly', 'hideous', 'repulsive'],
            'happy': ['sad', 'unhappy', 'miserable', 'depressed'],
            'big': ['small', 'tiny', 'little', 'miniature'],
            'fast': ['slow', 'sluggish'],
            'hot': ['cold', 'freezing', 'cool'],
            'light': ['dark', 'heavy'],
            'easy': ['hard', 'difficult', 'challenging'],
            'new': ['old', 'ancient', 'vintage'],
            'clean': ['dirty', 'filthy', 'messy'],
            'rich': ['poor', 'broke'],
            'strong': ['weak', 'feeble'],
            'tall': ['short', 'small'],
            'wide': ['narrow', 'thin'],
            'thick': ['thin', 'slim'],
            'loud': ['quiet', 'silent'],
            'bright': ['dim', 'dark'],
            'smooth': ['rough', 'bumpy'],
            'soft': ['hard', 'rough'],
            'young': ['old', 'elderly'],
            'early': ['late'],
            'empty': ['full'],
            'open': ['closed', 'shut'],
            'high': ['low'],
            'long': ['short'],
            'near': ['far', 'distant'],
            'first': ['last'],
            'begin': ['end', 'finish'],
            'start': ['stop', 'end'],
            'love': ['hate', 'despise'],
            'like': ['dislike', 'hate'],
            'win': ['lose', 'fail'],
            'give': ['take', 'receive'],
            'buy': ['sell'],
            'push': ['pull'],
            'up': ['down'],
            'in': ['out'],
            'on': ['off'],
            'yes': ['no'],
            'true': ['false'],
            'right': ['wrong', 'left'],
            'always': ['never'],
            'everything': ['nothing'],
            'everyone': ['nobody'],
            'everywhere': ['nowhere']
        }
        
        return common_antonyms.get(word, [])
    
    def get_definition(self, word):
        """Get definition using WordNet"""
        synsets = wordnet.synsets(word.lower())
        if synsets:
            return synsets[0].definition()
        return "No definition available"
    
    def generate_example_sentence(self, word):
        """Generate an example sentence using the word"""
        # First try to find examples from WordNet
        for syn in wordnet.synsets(word.lower()):
            if syn.examples():
                return syn.examples()[0]
        
        # If no examples found, create a simple template-based sentence
        pos = self.get_part_of_speech(word)
        templates = {
            'Noun': [
                f"The {word} was beautiful.",
                f"I saw a {word} in the garden.",
                f"Everyone admired the {word}."
            ],
            'Verb': [
                f"They {word} every morning.",
                f"She likes to {word} during weekends.",
                f"We should {word} more often."
            ],
            'Adjective': [
                f"The weather is very {word} today.",
                f"She looks {word} in that dress.",
                f"This book is quite {word}."
            ],
            'Adverb': [
                f"He spoke {word} to the audience.",
                f"She worked {word} on the project.",
                f"They handled the situation {word}."
            ]
        }
        
        # Get base POS (remove details in parentheses)
        base_pos = pos.split('(')[0].strip()
        
        if base_pos in templates:
            return random.choice(templates[base_pos])
        else:
            return f"The word '{word}' is used in many contexts."

# Initialize NLP processor
nlp_processor = NLPProcessor()

@app.route('/api/analyze', methods=['POST'])
def analyze_word():
    """Analyze a word and return comprehensive information"""
    try:
        data = request.get_json()
        word = data.get('word', '').strip()
        
        if not word:
            return jsonify({'error': 'Word is required'}), 400
        
        # Validate word (basic check for single word)
        if len(word.split()) > 1:
            return jsonify({'error': 'Please enter a single word'}), 400
        
        # Remove special characters
        clean_word = re.sub(r'[^a-zA-Z]', '', word)
        if not clean_word:
            return jsonify({'error': 'Please enter a valid word'}), 400
        
        # Get analysis
        part_of_speech = nlp_processor.get_part_of_speech(clean_word)
        synonyms, antonyms = nlp_processor.get_synonyms_antonyms(clean_word)
        definition = nlp_processor.get_definition(clean_word)
        example_sentence = nlp_processor.generate_example_sentence(clean_word)
        
        result = {
            'word': clean_word.lower(),
            'partOfSpeech': part_of_speech,
            'definition': definition,
            'synonyms': synonyms,
            'antonyms': antonyms,
            'exampleSentence': example_sentence,
            'success': True
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}', 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'NLP API is running'})

@app.route('/api/test', methods=['GET'])
def test_synonyms_antonyms():
    """Test endpoint to verify synonyms and antonyms functionality"""
    test_words = ['beautiful', 'good', 'happy']
    results = {}
    
    for word in test_words:
        synonyms, antonyms = nlp_processor.get_synonyms_antonyms(word)
        results[word] = {
            'synonyms': synonyms,
            'antonyms': antonyms,
            'synonyms_count': len(synonyms),
            'antonyms_count': len(antonyms)
        }
    
    return jsonify({
        'message': 'Synonyms and antonyms test results',
        'results': results,
        'success': True
    })

if __name__ == '__main__':
    print("Starting NLP API server...")
    print("Available endpoints:")
    print("- POST /api/analyze - Analyze a word")
    print("- GET /api/health - Health check")
    print("- GET /api/test - Test synonyms and antonyms functionality")
    app.run(debug=True, host='0.0.0.0', port=5000)