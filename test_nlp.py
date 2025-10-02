# Test the improved NLP processor
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import NLPProcessor

def test_improved_function():
    nlp = NLPProcessor()
    
    test_words = ['beautiful', 'good', 'happy', 'fast', 'big', 'new']
    
    print("Testing improved synonyms and antonyms function:")
    print("=" * 60)
    
    for word in test_words:
        synonyms, antonyms = nlp.get_synonyms_antonyms(word)
        print(f"\n{word.upper()}:")
        print(f"  Synonyms ({len(synonyms)}): {synonyms}")
        print(f"  Antonyms ({len(antonyms)}): {antonyms}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")

if __name__ == "__main__":
    test_improved_function()