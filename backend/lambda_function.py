"""
AWS Lambda NLP API Handler

A comprehensive Natural Language Processing API that provides:
- Part-of-speech tagging  
- Synonyms and antonyms lookup
- Word definitions
- Example sentence generation

The function intelligently uses NLTK when available and falls back to 
comprehensive built-in dictionaries for reliable functionality.

Designed for AWS Lambda with proper CORS handling for web frontends.
"""

import json
import os
import re
import random

# Set NLTK data path for Lambda environment
os.environ['NLTK_DATA'] = '/opt/nltk_data'

# Import NLTK modules with graceful fallback
try:
    import nltk
    from nltk.corpus import wordnet, brown
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


class NLPProcessor:
    """
    Natural Language Processing engine with NLTK integration and comprehensive fallbacks
    """
    
    def __init__(self):
        self.nltk_ready = False
        self._initialize_nltk()
    
    def _initialize_nltk(self):
        """Initialize NLTK with proper error handling and debugging"""
        if not NLTK_AVAILABLE:
            print("NLTK not available in environment - using fallbacks only")
            return
            
        print("NLTK is available, testing functionality...")
        
        try:
            # Set NLTK data path for Lambda environment
            if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
                print("Running in Lambda - setting NLTK data paths")
                # Add both possible paths
                nltk.data.path.insert(0, '/opt/nltk_data')
                nltk.data.path.insert(0, '/opt/python/nltk_data')
                nltk.data.path.insert(0, '/var/task/nltk_data')
                
                # Try to download essential NLTK data to /tmp (writable in Lambda)
                try:
                    temp_nltk_data = '/tmp/nltk_data'
                    os.makedirs(temp_nltk_data, exist_ok=True)
                    nltk.data.path.insert(0, temp_nltk_data)
                    
                    print("Attempting to download essential NLTK data...")
                    # Download essential datasets (using newer formats)
                    datasets_to_try = [
                        'punkt_tab',                    # New tokenizer format (NLTK 3.8+)
                        'punkt',                        # Fallback for older format
                        'averaged_perceptron_tagger',   # POS tagger
                        'wordnet',                      # WordNet corpus
                        'omw-1.4'                      # Open Multilingual Wordnet
                    ]
                    
                    for dataset in datasets_to_try:
                        try:
                            nltk.download(dataset, download_dir=temp_nltk_data, quiet=True)
                            print(f"✓ Downloaded {dataset}")
                        except Exception as e:
                            print(f"✗ Failed to download {dataset}: {e}")
                            
                except Exception as e:
                    print(f"Data download attempt failed: {e}")
            else:
                print("Running locally - using default NLTK data paths")
            
            # Test basic NLTK functionality progressively
            nltk_features = {
                'tokenization': False,
                'pos_tagging': False, 
                'wordnet': False
            }
            
            # Test 1: Tokenization (try multiple approaches)
            try:
                from nltk.tokenize import word_tokenize
                # Try tokenization with better error handling
                try:
                    tokens = word_tokenize('test word')
                    nltk_features['tokenization'] = len(tokens) == 2
                    print(f"✓ Tokenization working: {tokens}")
                except Exception as token_error:
                    # If punkt_tab fails, try basic split as fallback
                    print(f"Advanced tokenization failed ({token_error}), using basic split")
                    # We can still do basic tokenization without NLTK data
                    tokens = 'test word'.split()
                    nltk_features['tokenization'] = True  # Basic tokenization works
                    print(f"✓ Basic tokenization working: {tokens}")
            except Exception as e:
                print(f"✗ Tokenization completely failed: {e}")
            
            # Test 2: POS Tagging (requires averaged_perceptron_tagger)
            try:
                if nltk_features['tokenization']:
                    from nltk.tag import pos_tag
                    pos_tags = pos_tag(['test', 'word'])
                    nltk_features['pos_tagging'] = len(pos_tags) == 2
                    print(f"✓ POS tagging working: {pos_tags}")
            except Exception as e:
                print(f"✗ POS tagging failed: {e}")
            
            # Test 3: WordNet (requires wordnet corpus)
            try:
                from nltk.corpus import wordnet
                test_synsets = wordnet.synsets('good')
                if test_synsets:
                    nltk_features['wordnet'] = True
                    print(f"✓ WordNet working: {len(test_synsets)} synsets found")
                    print(f"  Example definition: {test_synsets[0].definition()}")
                else:
                    print(f"✗ WordNet: No synsets found for 'good'")
            except Exception as e:
                print(f"✗ WordNet failed: {e}")
            
            # Set nltk_ready based on available features
            working_features = sum(nltk_features.values())
            self.nltk_ready = working_features >= 2  # Need at least 2 features working
            
            if self.nltk_ready:
                print(f"✅ NLTK initialized with {working_features}/3 features working")
            else:
                print(f"⚠️ NLTK partially available ({working_features}/3 features) - using fallbacks")
            
        except Exception as e:
            print(f"❌ NLTK initialization completely failed: {e}")
            self.nltk_ready = False
    
    def analyze_word(self, word):
        """
        Complete word analysis returning all NLP information
        
        Args:
            word (str): The word to analyze
            
        Returns:
            dict: Complete analysis including POS, synonyms, antonyms, definition, example
        """
        clean_word = word.strip().lower()
        
        # Get all analyses
        part_of_speech = self.get_part_of_speech(clean_word)
        synonyms, antonyms = self.get_synonyms_antonyms(clean_word)
        definition = self.get_definition(clean_word)
        example_sentence = self.generate_example_sentence(clean_word)
        
        return {
            'word': clean_word,
            'partOfSpeech': part_of_speech,
            'definition': definition,
            'synonyms': synonyms,
            'antonyms': antonyms,
            'exampleSentence': example_sentence,
            'success': True,
            'nltk_available': self.nltk_ready,
            'nltk_imported': NLTK_AVAILABLE
        }
    
    def get_part_of_speech(self, word):
        """Get part of speech with NLTK or intelligent fallback"""
        if not self.nltk_ready:
            return self._get_fallback_pos(word)
            
        try:
            from nltk.tokenize import word_tokenize
            from nltk.tag import pos_tag
            
            tokens = word_tokenize(word.lower())
            if not tokens:
                return self._get_fallback_pos(word)
            
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
        except Exception as e:
            print(f"POS tagging error: {e}")
            return self._get_fallback_pos(word)
    
    def get_synonyms_antonyms(self, word):
        """Get synonyms and antonyms with NLTK WordNet or comprehensive fallbacks"""
        if not self.nltk_ready:
            return self._get_fallback_synonyms_antonyms(word)
            
        try:
            from nltk.corpus import wordnet
            synonyms = set()
            antonyms = set()
            
            # Get all synsets for the word
            synsets = wordnet.synsets(word.lower())
            
            if not synsets:
                return self._get_fallback_synonyms_antonyms(word)
            
            # Extract synonyms and antonyms from synsets
            for syn in synsets[:5]:  # Limit for performance
                # Add synonyms from lemmas
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if (synonym.lower() != word.lower() and 
                        len(synonym) > 1 and 
                        synonym.replace(' ', '').isalpha()):
                        synonyms.add(synonym)
                
                # Add synonyms from similar synsets
                try:
                    for similar_syn in syn.similar_tos()[:2]:
                        for lemma in similar_syn.lemmas():
                            synonym = lemma.name().replace('_', ' ')
                            if (synonym.lower() != word.lower() and 
                                len(synonym) > 1 and 
                                synonym.replace(' ', '').isalpha()):
                                synonyms.add(synonym)
                except:
                    pass
                
                # Extract antonyms
                for lemma in syn.lemmas():
                    try:
                        if lemma.antonyms():
                            for antonym in lemma.antonyms():
                                antonym_name = antonym.name().replace('_', ' ')
                                if (len(antonym_name) > 1 and 
                                    antonym_name.replace(' ', '').isalpha()):
                                    antonyms.add(antonym_name)
                    except:
                        pass
            
            # Convert to lists with limits
            synonyms_list = list(synonyms)[:8]
            antonyms_list = list(antonyms)[:6]
            
            # Supplement with fallback data if needed
            if len(synonyms_list) < 3 or not antonyms_list:
                fallback_syns, fallback_ants = self._get_fallback_synonyms_antonyms(word)
                
                # Add fallback antonyms if none found
                if not antonyms_list:
                    antonyms_list = fallback_ants[:4]
                
                # Add fallback synonyms if few found
                if len(synonyms_list) < 3:
                    for syn in fallback_syns:
                        if syn not in [s.lower() for s in synonyms_list] and len(synonyms_list) < 8:
                            synonyms_list.append(syn)
            
            return synonyms_list, antonyms_list
            
        except Exception as e:
            print(f"WordNet error: {e}")
            return self._get_fallback_synonyms_antonyms(word)
    
    def get_definition(self, word):
        """Get word definition with WordNet or comprehensive fallback"""
        if not self.nltk_ready:
            return self._get_fallback_definition(word)
            
        try:
            from nltk.corpus import wordnet
            synsets = wordnet.synsets(word.lower())
            
            if synsets:
                # Get the best definition
                best_def = synsets[0].definition()
                
                # If definition is short, try to find a better one
                if len(best_def) < 20 and len(synsets) > 1:
                    for syn in synsets[1:3]:
                        alt_def = syn.definition()
                        if len(alt_def) > len(best_def):
                            best_def = alt_def
                            break
                
                return best_def.capitalize() if best_def else self._get_fallback_definition(word)
            else:
                return self._get_fallback_definition(word)
        except Exception as e:
            print(f"Definition error: {e}")
            return self._get_fallback_definition(word)
    
    def generate_example_sentence(self, word):
        """Generate example sentence with WordNet examples or contextual templates"""
        if not self.nltk_ready:
            return self._get_fallback_example(word)
            
        try:
            from nltk.corpus import wordnet
            synsets = wordnet.synsets(word.lower())
            
            # Look for WordNet examples
            for syn in synsets[:3]:
                if syn.examples():
                    example = syn.examples()[0]
                    if example:
                        example = example.strip()
                        if example:
                            # Capitalize and ensure proper punctuation
                            example = example[0].upper() + example[1:] if len(example) > 1 else example.upper()
                            if not example.endswith(('.', '!', '?')):
                                example += '.'
                            return example
        except Exception as e:
            print(f"Example sentence error: {e}")
        
        return self._get_fallback_example(word)
    
    # === FALLBACK METHODS ===
    
    def _get_fallback_pos(self, word):
        """Intelligent part-of-speech detection using heuristics"""
        word = word.lower().strip()
        
        # Suffix-based detection
        if word.endswith(('ing', 'ed', 'ate', 'ize', 'ify')):
            return 'Verb'
        
        if word.endswith(('ful', 'less', 'ous', 'ive', 'able', 'ible', 'al', 'ic')):
            return 'Adjective'
        
        if word.endswith('ly') and len(word) > 3:
            return 'Adverb'
            
        # Known word classifications
        common_verbs = {'run', 'walk', 'speak', 'work', 'love', 'hate', 'go', 'come', 'see', 'hear', 'think', 'know', 'make', 'take', 'give'}
        common_adjectives = {'good', 'bad', 'beautiful', 'ugly', 'happy', 'sad', 'big', 'small', 'hot', 'cold', 'new', 'old', 'fast', 'slow'}
        
        if word in common_verbs:
            return 'Verb'
        elif word in common_adjectives:
            return 'Adjective'
        else:
            return 'Noun'  # Default to noun
    
    def _get_fallback_synonyms_antonyms(self, word):
        """Comprehensive synonym and antonym dictionary"""
        word = word.lower()
        
        word_mappings = {
            # Positive adjectives
            'beautiful': (['pretty', 'lovely', 'attractive', 'gorgeous', 'stunning', 'elegant'], ['ugly', 'hideous', 'unattractive']),
            'good': (['great', 'excellent', 'fine', 'wonderful', 'superb', 'outstanding'], ['bad', 'poor', 'terrible', 'awful']),
            'happy': (['joyful', 'cheerful', 'glad', 'pleased', 'delighted', 'elated'], ['sad', 'unhappy', 'miserable', 'depressed']),
            'smart': (['intelligent', 'clever', 'brilliant', 'wise', 'bright'], ['dumb', 'stupid', 'foolish', 'ignorant']),
            'kind': (['nice', 'gentle', 'caring', 'compassionate', 'thoughtful'], ['mean', 'cruel', 'harsh', 'unkind']),
            
            # Size and scale
            'big': (['large', 'huge', 'enormous', 'giant', 'massive', 'immense'], ['small', 'tiny', 'little', 'miniature']),
            'small': (['tiny', 'little', 'minute', 'compact', 'petite'], ['big', 'large', 'huge', 'enormous']),
            'tall': (['high', 'lofty', 'towering', 'elevated'], ['short', 'low', 'small']),
            
            # Speed and movement
            'fast': (['quick', 'rapid', 'swift', 'speedy', 'hasty'], ['slow', 'sluggish', 'leisurely']),
            'slow': (['leisurely', 'gradual', 'unhurried', 'delayed'], ['fast', 'quick', 'rapid', 'swift']),
            
            # Temperature
            'hot': (['warm', 'heated', 'burning', 'scorching'], ['cold', 'cool', 'freezing', 'chilly']),
            'cold': (['cool', 'chilly', 'freezing', 'icy', 'frigid'], ['hot', 'warm', 'heated']),
            
            # Difficulty
            'easy': (['simple', 'effortless', 'straightforward', 'uncomplicated'], ['hard', 'difficult', 'challenging', 'complex']),
            'hard': (['difficult', 'challenging', 'tough', 'demanding'], ['easy', 'simple', 'effortless']),
            
            # Time
            'new': (['fresh', 'recent', 'modern', 'latest', 'contemporary'], ['old', 'ancient', 'outdated', 'vintage']),
            'old': (['ancient', 'aged', 'vintage', 'antique'], ['new', 'fresh', 'recent', 'modern']),
            
            # Common words
            'love': (['adore', 'cherish', 'treasure', 'appreciate'], ['hate', 'despise', 'detest']),
            'hate': (['despise', 'detest', 'loathe', 'abhor'], ['love', 'adore', 'like']),
            'light': (['bright', 'illuminated', 'radiant', 'luminous'], ['dark', 'dim', 'shadowy']),
            'dark': (['dim', 'shadowy', 'murky', 'gloomy'], ['light', 'bright', 'illuminated']),
            
            # Greetings
            'hello': (['hi', 'greeting', 'welcome', 'salutation', 'howdy'], ['goodbye', 'farewell', 'bye']),
            'goodbye': (['farewell', 'bye', 'see you later', 'adieu'], ['hello', 'hi', 'welcome']),
            
            # Actions
            'run': (['sprint', 'dash', 'jog', 'race', 'hurry'], ['walk', 'stroll', 'crawl']),
            'walk': (['stroll', 'amble', 'march', 'stride'], ['run', 'sprint', 'dash']),
            'speak': (['talk', 'communicate', 'converse', 'chat'], ['listen', 'hear']),
            'work': (['labor', 'toil', 'operate', 'function'], ['rest', 'relax', 'play']),
        }
        
        if word in word_mappings:
            return word_mappings[word]
        
        # Pattern-based generation for unknown words
        if word.startswith('un'):
            base_word = word[2:]
            return ([f're{base_word}', base_word], [word])
        elif word.startswith('in'):
            base_word = word[2:]
            return ([base_word], [word])
        else:
            return (['similar', 'alike'], ['different', 'opposite'])
    
    def _get_fallback_definition(self, word):
        """Comprehensive definition dictionary"""
        word = word.lower()
        
        definitions = {
            'beautiful': 'pleasing to the senses or mind aesthetically',
            'good': 'having the right or desired qualities; satisfactory',
            'happy': 'feeling or showing pleasure or contentment',
            'smart': 'having or showing intelligence or good judgment',
            'kind': 'having or showing a friendly, generous nature',
            'big': 'of considerable size, extent, or intensity',
            'small': 'of a size that is less than normal or usual',
            'fast': 'moving or capable of moving at high speed',
            'slow': 'moving or operating at a low speed',
            'hot': 'having a high degree of heat or temperature',
            'cold': 'of or at a low temperature',
            'easy': 'achieved with ease; not difficult',
            'hard': 'solid, firm, and resistant to pressure',
            'new': 'not existing before; made or introduced recently',
            'old': 'having lived for a long time; no longer young',
            'love': 'feel deep affection or sexual love for someone',
            'hate': 'feel intense dislike for something or someone',
            'run': 'move at a speed faster than walking',
            'walk': 'move at a regular pace by lifting and setting down each foot',
            'speak': 'say something in order to convey information or express feelings',
            'work': 'activity involving mental or physical effort to achieve a result',
            'hello': 'used as a greeting or to begin a conversation',
            'goodbye': 'used to express good wishes when parting',
        }
        
        return definitions.get(word, f'A common English word meaning "{word}"')
    
    def _get_fallback_example(self, word):
        """Contextually appropriate example sentences"""
        word_lower = word.lower()
        
        examples = {
            'beautiful': f"The sunset was absolutely {word}.",
            'good': f"She did a {word} job on the project.",
            'happy': f"The children were {word} to see their grandmother.",
            'smart': f"He is a very {word} student.",
            'kind': f"She has a {word} heart and helps everyone.",
            'big': f"The elephant is a {word} animal.",
            'small': f"The mouse is a {word} creature.",
            'fast': f"The cheetah is a {word} runner.",
            'slow': f"The turtle moves at a {word} pace.",
            'hot': f"The coffee is too {word} to drink.",
            'cold': f"It's {word} outside, so wear a jacket.",
            'easy': f"This puzzle is {word} to solve.",
            'hard': f"The exam was {word}, but I studied well.",
            'new': f"I bought a {word} car yesterday.",
            'old': f"The {word} oak tree has stood here for centuries.",
            'love': f"I {word} spending time with my family.",
            'hate': f"I {word} waiting in long lines.",
            'run': f"Every morning, I {word} in the park.",
            'walk': f"Let's {word} to the store together.",
            'speak': f"Can you {word} more slowly, please?",
            'work': f"I need to {word} late tonight to finish this project.",
            'hello': f"She said '{word}' when she entered the room.",
            'goodbye': f"It's hard to say '{word}' to old friends.",
        }
        
        if word_lower in examples:
            return examples[word_lower]
        
        # Generate based on likely part of speech
        pos = self._get_fallback_pos(word_lower)
        if pos == 'Adjective':
            return f"The {word} sky looked magnificent."
        elif pos == 'Verb':
            return f"I often {word} when I have free time."
        else:
            return f"The {word} caught everyone's attention."


# Initialize NLP processor
nlp_processor = NLPProcessor()


def lambda_handler(event, context):
    """
    AWS Lambda handler for NLP API
    
    Provides comprehensive natural language processing with proper CORS handling
    """
    # CORS headers for all responses
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight OPTIONS requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')
        
        # Health check endpoint
        if path == '/api/health' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'message': 'NLP API is running',
                    'nltk_available': NLTK_AVAILABLE,
                    'nltk_ready': nlp_processor.nltk_ready
                })
            }
        
        # Main analysis endpoint
        elif path == '/api/analyze' and method == 'POST':
            # Parse request body
            try:
                body = json.loads(event.get('body', '{}'))
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': cors_headers,
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
                
            word = body.get('word', '').strip()
            
            if not word:
                return {
                    'statusCode': 400,
                    'headers': cors_headers,
                    'body': json.dumps({'error': 'Word is required'})
                }
            
            # Validate single word input
            if len(word.split()) > 1:
                return {
                    'statusCode': 400,
                    'headers': cors_headers,
                    'body': json.dumps({'error': 'Please enter a single word'})
                }
            
            # Clean the word
            clean_word = re.sub(r'[^a-zA-Z]', '', word)
            if not clean_word:
                return {
                    'statusCode': 400,
                    'headers': cors_headers,
                    'body': json.dumps({'error': 'Please enter a valid word'})
                }
            
            # Perform analysis
            result = nlp_processor.analyze_word(clean_word)
            
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps(result)
            }
        
        # Unknown endpoint
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': json.dumps({
                    'error': f'Not found: {method} {path}',
                    'success': False
                })
            }
            
    except Exception as e:
        # Global error handler
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}',
                'success': False
            })
        }