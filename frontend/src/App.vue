<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar 
      app 
      color="primary" 
      dark 
      elevation="4"
      height="64"
    >
      <v-app-bar-title class="app-title">
        <v-icon left size="large">mdi-brain</v-icon>
        <span class="title-text">NLP Word Analyzer</span>
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <!-- Theme Toggle -->
      <v-btn
        icon
        @click="toggleTheme"
        size="large"
      >
        <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
      
      <!-- API Status Indicator -->
      <v-chip
        :color="apiStatus.color"
        variant="flat"
        size="small"
        class="ml-2"
      >
        <v-icon left size="small">{{ apiStatus.icon }}</v-icon>
        {{ apiStatus.text }}
      </v-chip>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="main-container">
        <v-row justify="center">
          <v-col cols="12" md="8" lg="6">
            <!-- Hero Section -->
            <div class="hero-section text-center mb-8">
              <h1 class="text-h2 font-weight-bold mb-4 gradient-text">
                Explore Words Like Never Before
              </h1>
              <p class="text-h6 text-medium-emphasis mb-6">
                Discover the linguistic richness of any word with advanced natural language processing
              </p>
            </div>

            <!-- Word Input Component -->
            <WordInput
              ref="wordInput"
              @word-analyzed="handleWordAnalysis"
              @analysis-error="handleAnalysisError"
            />

            <!-- Analysis Result Component -->
            <AnalysisResult
              v-if="analysisResult"
              :analysis="analysisResult"
              @new-analysis="resetAnalysis"
            />

            <!-- Error Display -->
            <v-alert
              v-if="errorMessage"
              type="error"
              variant="tonal"
              closable
              @click:close="errorMessage = ''"
              class="mt-4"
            >
              <v-alert-title>Analysis Error</v-alert-title>
              {{ errorMessage }}
            </v-alert>

            <!-- Features Section -->
            <v-card
              v-if="!analysisResult && !errorMessage"
              class="features-card mt-8"
              variant="outlined"
            >
              <v-card-title class="text-center">
                <v-icon left color="primary">mdi-feature-search</v-icon>
                What You'll Discover
              </v-card-title>
              
              <v-card-text>
                <v-row>
                  <v-col cols="12" sm="6" md="3" v-for="feature in features" :key="feature.title">
                    <div class="feature-item text-center">
                      <v-avatar size="48" :color="feature.color" class="mb-3">
                        <v-icon :color="feature.textColor">{{ feature.icon }}</v-icon>
                      </v-avatar>
                      <h4 class="text-subtitle-1 font-weight-bold">{{ feature.title }}</h4>
                      <p class="text-body-2 text-medium-emphasis">{{ feature.description }}</p>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="surface" class="text-center">
      <v-row justify="center" no-gutters>
        <v-col cols="12" class="py-4">
          <p class="text-body-2 text-medium-emphasis">
            Built with ❤️ using Vue.js, Vuetify, and NLTK | 
            <v-icon size="small" class="mx-1">mdi-api</v-icon>
            Powered by Natural Language Processing
          </p>
        </v-col>
      </v-row>
    </v-footer>

    <!-- Loading Overlay -->
    <v-overlay
      v-model="globalLoading"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
      ></v-progress-circular>
      <p class="mt-4 text-h6">Processing your word...</p>
    </v-overlay>

    <!-- Snackbar for Notifications -->
    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      timeout="4000"
      location="top"
    >
      {{ snackbarMessage }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="showSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { useTheme } from 'vuetify'
import { ref, onMounted, computed } from 'vue'
import WordInput from './components/WordInput.vue'
import AnalysisResult from './components/AnalysisResult.vue'
import { nlpService } from './services/nlpService'

export default {
  name: 'App',
  components: {
    WordInput,
    AnalysisResult
  },
  setup() {
    const theme = useTheme()
    const isDark = computed(() => theme.global.current.value.dark)
    
    const toggleTheme = () => {
      theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
    }
    
    return { isDark, toggleTheme }
  },
  data() {
    return {
      analysisResult: null,
      errorMessage: '',
      globalLoading: false,
      showSnackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      apiStatus: {
        color: 'warning',
        icon: 'mdi-connection',
        text: 'Checking...'
      },
      features: [
        {
          title: 'Part of Speech',
          description: 'Identify grammatical categories',
          icon: 'mdi-tag-outline',
          color: 'primary',
          textColor: 'white'
        },
        {
          title: 'Synonyms',
          description: 'Find similar words',
          icon: 'mdi-equal',
          color: 'success',
          textColor: 'white'
        },
        {
          title: 'Antonyms',
          description: 'Discover opposite meanings',
          icon: 'mdi-not-equal',
          color: 'error',
          textColor: 'white'
        },
        {
          title: 'Examples',
          description: 'See words in context',
          icon: 'mdi-format-quote-open',
          color: 'info',
          textColor: 'white'
        }
      ]
    }
  },
  async mounted() {
    await this.checkApiStatus()
  },
  methods: {
    async handleWordAnalysis(word) {
      this.errorMessage = ''
      this.globalLoading = true
      this.$refs.wordInput.setLoading(true)
      
      try {
        const result = await nlpService.analyzeWord(word)
        
        if (result.success) {
          this.analysisResult = result
          this.showNotification('Analysis completed successfully!', 'success')
        } else {
          this.errorMessage = result.error || 'Analysis failed'
          this.$refs.wordInput.setError(this.errorMessage)
        }
      } catch (error) {
        this.errorMessage = error.message
        this.$refs.wordInput.setError(error.message)
        this.showNotification(error.message, 'error')
      } finally {
        this.globalLoading = false
        this.$refs.wordInput.setLoading(false)
      }
    },
    
    handleAnalysisError(error) {
      this.errorMessage = error
      this.showNotification(error, 'error')
    },
    
    resetAnalysis() {
      this.analysisResult = null
      this.errorMessage = ''
    },
    
    async checkApiStatus() {
      try {
        await nlpService.checkHealth()
        this.apiStatus = {
          color: 'success',
          icon: 'mdi-check-circle',
          text: 'Online'
        }
      } catch (error) {
        this.apiStatus = {
          color: 'error',
          icon: 'mdi-alert-circle',
          text: 'Offline'
        }
      }
    },
    
    showNotification(message, color = 'info') {
      this.snackbarMessage = message
      this.snackbarColor = color
      this.showSnackbar = true
    }
  }
}
</script>

<style scoped>
.app-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.title-text {
  margin-left: 8px;
}

.main-container {
  min-height: calc(100vh - 128px);
  padding-top: 32px;
  padding-bottom: 32px;
}

.hero-section {
  padding: 48px 0;
}

.gradient-text {
  background: linear-gradient(45deg, #1976D2, #42A5F5);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
}

.features-card {
  border-radius: 16px;
}

.feature-item {
  padding: 16px;
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-4px);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-section {
  animation: fadeInUp 0.8s ease-out;
}

/* Responsive Design */
@media (max-width: 960px) {
  .hero-section {
    padding: 32px 0;
  }
  
  .gradient-text {
    font-size: 2.5rem;
  }
}

@media (max-width: 600px) {
  .app-title {
    font-size: 1.1rem;
  }
  
  .title-text {
    display: none;
  }
  
  .hero-section {
    padding: 24px 0;
  }
  
  .gradient-text {
    font-size: 2rem;
  }
}

/* Dark theme enhancements */
.v-theme--dark .hero-section {
  color: rgba(255, 255, 255, 0.87);
}

.v-theme--dark .gradient-text {
  background: linear-gradient(45deg, #42A5F5, #90CAF9);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>