<template>
  <v-card 
    class="word-input-card" 
    elevation="4"
    rounded="lg"
  >
    <v-card-title class="text-h5 font-weight-bold primary--text">
      <v-icon left color="primary" size="large">mdi-text-search</v-icon>
      Word Analysis
    </v-card-title>
    
    <v-card-text>
      <v-form @submit.prevent="analyzeWord" ref="form">
        <v-text-field
          v-model="word"
          label="Enter a word to analyze"
          placeholder="e.g., beautiful, happy, run..."
          variant="outlined"
          :loading="loading"
          :disabled="loading"
          :error-messages="errorMessage"
          clearable
          autofocus
          @keyup.enter="analyzeWord"
          @input="clearError"
          prepend-inner-icon="mdi-alphabetical-variant"
          class="mb-4"
        >
          <template v-slot:append>
            <v-btn
              :loading="loading"
              :disabled="!word || loading"
              color="primary"
              variant="flat"
              @click="analyzeWord"
              size="large"
              rounded="lg"
            >
              <v-icon left>mdi-magnify</v-icon>
              Analyze
            </v-btn>
          </template>
        </v-text-field>
      </v-form>

      <!-- Quick Examples -->
      <div class="quick-examples mb-4">
        <v-chip-group>
          <v-chip
            v-for="example in exampleWords"
            :key="example"
            @click="selectExample(example)"
            variant="outlined"
            color="primary"
            size="small"
            :disabled="loading"
          >
            {{ example }}
          </v-chip>
        </v-chip-group>
      </div>
    </v-card-text>

    <!-- Loading State -->
    <v-card-text v-if="loading" class="text-center">
      <v-progress-circular 
        color="primary" 
        indeterminate 
        size="48"
      ></v-progress-circular>
      <p class="mt-3 text-body-1">Analyzing word...</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'WordInput',
  emits: ['word-analyzed', 'analysis-error'],
  data() {
    return {
      word: '',
      loading: false,
      errorMessage: '',
      exampleWords: [
        'beautiful', 'happy', 'run', 'incredible', 'analyze', 
        'wonderful', 'create', 'amazing', 'discover', 'brilliant'
      ]
    }
  },
  methods: {
    async analyzeWord() {
      if (!this.word || this.loading) return
      
      // Basic validation
      if (this.word.trim().length === 0) {
        this.errorMessage = 'Please enter a word'
        return
      }
      
      if (this.word.trim().split(' ').length > 1) {
        this.errorMessage = 'Please enter only one word'
        return
      }
      
      this.loading = true
      this.errorMessage = ''
      
      try {
        this.$emit('word-analyzed', this.word.trim())
      } catch (error) {
        this.errorMessage = error.message
        this.$emit('analysis-error', error.message)
      } finally {
        this.loading = false
      }
    },
    
    selectExample(example) {
      if (!this.loading) {
        this.word = example
        this.analyzeWord()
      }
    },
    
    clearError() {
      this.errorMessage = ''
    },
    
    setLoading(isLoading) {
      this.loading = isLoading
    },
    
    setError(message) {
      this.errorMessage = message
      this.loading = false
    }
  }
}
</script>

<style scoped>
.word-input-card {
  margin-bottom: 24px;
}

.quick-examples {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  padding-top: 16px;
}

.v-chip-group {
  justify-content: center;
}

.v-text-field {
  font-size: 1.1em;
}

@media (max-width: 600px) {
  .v-text-field .v-btn {
    margin-top: 8px;
  }
}
</style>