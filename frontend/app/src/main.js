import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/tailwind.css';
import Toast, { POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css'; 
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

// Global error handler for script loading errors
window.addEventListener('error', (event) => {
  if (event.target && (event.target.tagName === 'SCRIPT' || event.target.tagName === 'LINK')) {
    console.warn(`Failed to load external resource: ${event.target.src || event.target.href}`);
    // Prevent the error from propagating
    event.preventDefault();
    return false;
  }
});

// Enhanced global error logger
window.onerror = function (msg, url, line, col, error) {
  console.error("Global error:", msg, url, line, col, error);
  return false; // Don't suppress default handling
};

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  console.warn('Unhandled promise rejection:', event.reason);
  event.preventDefault();
});

const app = createApp(App);
app.use(ElementPlus);
app.use(Toast, {
    position: POSITION.TOP_LEFT,
    timeout: 5000,
    zIndex: 2147483647
  });

// Enable devtools in production
app.config.devtools = true;

// Global error handler for Vue errors
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue error:', err, info);
};

console.log('API URL:', process.env.VUE_APP_API_URL);

app.use(router).mount('#app');