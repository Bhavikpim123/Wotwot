<template>
  <div class="content-section m-8 md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-6 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold text-green-800">AI Message Generator</h2>
        <p class="text-sm md:text-base text-gray-600">Generate personalized messages using AI prompts</p>
      </div>
      <div>
        <button 
          @click="$router.push('/broadcast/broadcast1')"
          class="bg-gray-600 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-gray-700 transition-all duration-300">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          Back to Templates
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Input Section -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Message Prompt</h3>
        
        <!-- Quick Examples -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Quick Examples:</label>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="example in quickExamples" 
              :key="example.id"
              @click="setPrompt(example.prompt)"
              class="text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full hover:bg-blue-200 transition-colors">
              {{ example.label }}
            </button>
          </div>
        </div>

        <!-- Prompt Input -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Describe the message you want to generate:
          </label>
          <textarea 
            v-model="prompt"
            placeholder="e.g., I want to send a Diwali greeting to my customers with warm wishes and a special discount offer"
            class="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
            :disabled="isGenerating"
          ></textarea>
        </div>

        <!-- Message Type -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Message Type:</label>
          <select v-model="messageType" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500">
            <option value="promotional">Promotional</option>
            <option value="greeting">Greeting/Festive</option>
            <option value="informational">Informational</option>
            <option value="reminder">Reminder</option>
            <option value="support">Customer Support</option>
          </select>
        </div>

        <!-- Tone Selection -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Tone:</label>
          <select v-model="tone" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500">
            <option value="friendly">Friendly</option>
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="formal">Formal</option>
            <option value="enthusiastic">Enthusiastic</option>
          </select>
        </div>

        <!-- Generate Button -->
        <button 
          @click="generateMessage"
          :disabled="!prompt.trim() || isGenerating"
          class="w-full bg-green-700 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center">
          <svg v-if="isGenerating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isGenerating ? 'Generating...' : 'Generate Message' }}
        </button>
      </div>

      <!-- Output Section -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Generated Message</h3>
        
        <div v-if="!generatedMessage && !error" class="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
          <div class="text-center text-gray-500">
            <svg class="w-12 h-12 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            <p>Your AI-generated message will appear here</p>
          </div>
        </div>

        <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex">
            <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <div class="ml-3">
              <p class="text-sm text-red-600">{{ error }}</p>
            </div>
          </div>
        </div>

        <div v-if="generatedMessage" class="space-y-4">
          <!-- Preview Box -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-start mb-2">
              <span class="text-sm font-medium text-gray-700">Generated Message:</span>
              <div class="flex space-x-2">
                <button 
                  @click="copyMessage"
                  class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors">
                  {{ copied ? 'Copied!' : 'Copy' }}
                </button>
                <button 
                  @click="regenerateMessage"
                  class="text-xs bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition-colors">
                  Regenerate
                </button>
              </div>
            </div>
            <div class="bg-white p-3 rounded border" style="white-space: pre-line;">{{ generatedMessage }}</div>
          </div>

          <!-- Editable Message -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Edit Message (Optional):</label>
            <textarea 
              v-model="editableMessage"
              class="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
              placeholder="Make any adjustments to the generated message..."
            ></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="flex space-x-3">
            <button 
              @click="saveAsTemplate"
              class="flex-1 bg-green-700 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-800 transition-colors">
              Save as Template
            </button>
            <button 
              @click="useinBroadcast"
              class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors">
              Use in Broadcast
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MessageGenerator',
  data() {
    return {
      prompt: '',
      messageType: 'promotional',
      tone: 'friendly',
      generatedMessage: '',
      editableMessage: '',
      isGenerating: false,
      error: null,
      copied: false,
      quickExamples: [
        {
          id: 1,
          label: 'Diwali Wishes',
          prompt: 'I want to send warm Diwali greetings to my customers with festive wishes and blessings'
        },
        {
          id: 2,
          label: 'New Year Sale',
          prompt: 'Create a New Year sale announcement with exciting discounts and offers'
        },
        {
          id: 3,
          label: 'Order Confirmation',
          prompt: 'Generate a friendly order confirmation message with delivery details'
        },
        {
          id: 4,
          label: 'Birthday Wishes',
          prompt: 'Send personalized birthday wishes to customers with a special discount'
        },
        {
          id: 5,
          label: 'Service Reminder',
          prompt: 'Remind customers about upcoming service appointments or renewals'
        }
      ]
    };
  },
  methods: {
    setPrompt(examplePrompt) {
      this.prompt = examplePrompt;
    },

    async generateMessage() {
      if (!this.prompt.trim()) return;

      this.isGenerating = true;
      this.error = null;
      this.generatedMessage = '';
      this.editableMessage = '';

      try {
        const response = await axios.post('/api/generate-message', {
          prompt: this.prompt,
          messageType: this.messageType,
          tone: this.tone
        });

        if (response.data && response.data.message) {
          this.generatedMessage = response.data.message;
          this.editableMessage = response.data.message;
        } else {
          throw new Error('Invalid response format');
        }
      } catch (error) {
        console.error('Error generating message:', error);
        if (error.response) {
          // Server responded with error status
          this.error = `Server error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`;
        } else if (error.request) {
          // Request was made but no response received
          this.error = 'Network error: Unable to connect to the server. Please check if the backend is running.';
        } else {
          // Something else happened
          this.error = `Error: ${error.message}`;
        }
      } finally {
        this.isGenerating = false;
      }
    },

    async regenerateMessage() {
      await this.generateMessage();
    },

    copyMessage() {
      try {
        const textToCopy = this.editableMessage || this.generatedMessage;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(textToCopy).then(() => {
            this.copied = true;
            setTimeout(() => {
              this.copied = false;
            }, 2000);
          }).catch(err => {
            console.error('Failed to copy text: ', err);
            // Fallback for older browsers
            this.fallbackCopyTextToClipboard(textToCopy);
          });
        } else {
          // Fallback for older browsers
          this.fallbackCopyTextToClipboard(textToCopy);
        }
      } catch (error) {
        console.error('Copy error:', error);
      }
    },

    fallbackCopyTextToClipboard(text) {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.position = 'fixed';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand('copy');
        this.copied = true;
        setTimeout(() => {
          this.copied = false;
        }, 2000);
      } catch (err) {
        console.error('Fallback: Unable to copy', err);
      }
      document.body.removeChild(textArea);
    },

    saveAsTemplate() {
      try {
        // Navigate to template creation with pre-filled message
        const messageContent = this.editableMessage || this.generatedMessage;
        if (this.$router) {
          this.$router.push({
            path: '/broadcast/broadcast1',
            query: {
              prefillMessage: messageContent,
              messageType: this.messageType
            }
          });
        }
      } catch (error) {
        console.error('Navigation error:', error);
      }
    },

    useinBroadcast() {
      try {
        // Navigate to broadcast creation with the generated message
        const messageContent = this.editableMessage || this.generatedMessage;
        if (this.$router) {
          this.$router.push({
            path: '/broadcast/broadcast2',
            query: {
              generatedMessage: messageContent,
              messageType: this.messageType
            }
          });
        }
      } catch (error) {
        console.error('Navigation error:', error);
      }
    }
  },
  // Add error handling for component lifecycle
  errorCaptured(err, instance, info) {
    console.error('Component error captured:', err, info);
    this.error = 'An unexpected error occurred. Please refresh the page.';
    return false;
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>