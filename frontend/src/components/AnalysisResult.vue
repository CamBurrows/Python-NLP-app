<template>
  <v-fade-transition>
    <v-card 
      v-if="analysis" 
      class="analysis-result-card" 
      elevation="6"
      rounded="lg"
    >
      <!-- Word Header -->
      <v-card-title class="analysis-header">
        <div class="word-display">
          <h2 class="text-h3 font-weight-bold primary--text">
            {{ analysis.word }}
          </h2>
          <v-chip 
            :color="getPosColor(analysis.partOfSpeech)"
            variant="flat"
            size="large"
            class="pos-chip"
          >
            <v-icon left size="small">{{ getPosIcon(analysis.partOfSpeech) }}</v-icon>
            {{ analysis.partOfSpeech }}
          </v-chip>
        </div>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <!-- Definition Section -->
        <v-row>
          <v-col cols="12">
            <div class="definition-section mb-6">
              <h3 class="text-h6 mb-3 section-title">
                <v-icon left color="info">mdi-book-open-variant</v-icon>
                Definition
              </h3>
              <p class="definition-text text-body-1">
                {{ analysis.definition }}
              </p>
            </div>
          </v-col>
        </v-row>

        <!-- Example Sentence Section -->
        <v-row>
          <v-col cols="12">
            <div class="example-section mb-6">
              <h3 class="text-h6 mb-3 section-title">
                <v-icon left color="success">mdi-format-quote-open</v-icon>
                Example Usage
              </h3>
              <v-card 
                variant="tonal" 
                color="success"
                class="example-card"
              >
                <v-card-text>
                  <p class="example-text text-body-1 font-italic">
                    "{{ analysis.exampleSentence }}"
                  </p>
                </v-card-text>
              </v-card>
            </div>
          </v-col>
        </v-row>

        <!-- Synonyms and Antonyms Section -->
        <v-row>
          <!-- Synonyms -->
          <v-col cols="12" md="6">
            <div class="synonyms-section">
              <h3 class="text-h6 mb-3 section-title">
                <v-icon left color="primary">mdi-equal</v-icon>
                Synonyms
                <v-badge 
                  :content="analysis.synonyms.length" 
                  color="primary" 
                  inline
                ></v-badge>
              </h3>
              
              <div v-if="analysis.synonyms.length > 0" class="word-chips">
                <v-chip
                  v-for="synonym in analysis.synonyms"
                  :key="`syn-${synonym}`"
                  color="primary"
                  variant="outlined"
                  class="ma-1"
                  size="default"
                >
                  {{ synonym }}
                </v-chip>
              </div>
              
              <v-alert 
                v-else 
                type="info" 
                variant="tonal"
                density="compact"
                class="no-data-alert"
              >
                No synonyms found
              </v-alert>
            </div>
          </v-col>

          <!-- Antonyms -->
          <v-col cols="12" md="6">
            <div class="antonyms-section">
              <h3 class="text-h6 mb-3 section-title">
                <v-icon left color="error">mdi-not-equal</v-icon>
                Antonyms
                <v-badge 
                  :content="analysis.antonyms.length" 
                  color="error" 
                  inline
                ></v-badge>
              </h3>
              
              <div v-if="analysis.antonyms.length > 0" class="word-chips">
                <v-chip
                  v-for="antonym in analysis.antonyms"
                  :key="`ant-${antonym}`"
                  color="error"
                  variant="outlined"
                  class="ma-1"
                  size="default"
                >
                  {{ antonym }}
                </v-chip>
              </div>
              
              <v-alert 
                v-else 
                type="warning" 
                variant="tonal"
                density="compact"
                class="no-data-alert"
              >
                No antonyms found
              </v-alert>
            </div>
          </v-col>
        </v-row>
      </v-card-text>

      <!-- Action Buttons -->
      <v-divider></v-divider>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          variant="outlined"
          color="primary"
          @click="shareAnalysis"
          prepend-icon="mdi-share"
        >
          Share
        </v-btn>
        <v-btn
          variant="flat"
          color="primary"
          @click="$emit('new-analysis')"
          prepend-icon="mdi-refresh"
        >
          Analyze Another Word
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-fade-transition>
</template>

<script>
export default {
  name: 'AnalysisResult',
  props: {
    analysis: {
      type: Object,
      required: true
    }
  },
  emits: ['new-analysis'],
  methods: {
    getPosColor(pos) {
      const colors = {
        'Noun': 'blue',
        'Verb': 'green',
        'Adjective': 'purple',
        'Adverb': 'orange',
        'Pronoun': 'teal',
        'Preposition': 'indigo',
        'Conjunction': 'pink',
        'Interjection': 'cyan'
      }
      
      // Check for partial matches
      for (const [key, color] of Object.entries(colors)) {
        if (pos.includes(key)) {
          return color
        }
      }
      
      return 'grey'
    },
    
    getPosIcon(pos) {
      const icons = {
        'Noun': 'mdi-cube-outline',
        'Verb': 'mdi-run',
        'Adjective': 'mdi-palette',
        'Adverb': 'mdi-speedometer',
        'Pronoun': 'mdi-account',
        'Preposition': 'mdi-arrow-right',
        'Conjunction': 'mdi-link',
        'Interjection': 'mdi-exclamation'
      }
      
      // Check for partial matches
      for (const [key, icon] of Object.entries(icons)) {
        if (pos.includes(key)) {
          return icon
        }
      }
      
      return 'mdi-help-circle'
    },
    
    shareAnalysis() {
      const text = `Word Analysis: ${this.analysis.word}\n` +
                  `Part of Speech: ${this.analysis.partOfSpeech}\n` +
                  `Definition: ${this.analysis.definition}\n` +
                  `Example: ${this.analysis.exampleSentence}`
      
      if (navigator.share) {
        navigator.share({
          title: `Analysis of "${this.analysis.word}"`,
          text: text,
        })
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
          // You could show a snackbar here
          console.log('Copied to clipboard!')
        })
      }
    }
  }
}
</script>

<style scoped>
.analysis-result-card {
  margin-top: 24px;
  background: linear-gradient(145deg, #ffffff, #f5f5f5);
}

.analysis-header {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  padding: 24px;
}

.word-display {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.pos-chip {
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-title {
  display: flex;
  align-items: center;
  color: rgba(0, 0, 0, 0.87);
  font-weight: 600;
}

.definition-text {
  background: rgba(0, 0, 0, 0.04);
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid #2196F3;
  font-size: 1.1em;
  line-height: 1.6;
}

.example-card {
  border-left: 4px solid #4CAF50;
}

.example-text {
  font-size: 1.1em;
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.8);
}

.word-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.no-data-alert {
  margin-top: 8px;
}

.definition-section,
.example-section,
.synonyms-section,
.antonyms-section {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile Responsiveness */
@media (max-width: 600px) {
  .word-display {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .word-display h2 {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
}

/* Dark theme adjustments */
.v-theme--dark .analysis-result-card {
  background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
}

.v-theme--dark .analysis-header {
  background: linear-gradient(135deg, #1a237e, #283593);
}

.v-theme--dark .definition-text {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.87);
}
</style>