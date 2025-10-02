# Frontend Setup Instructions

## Quick Fix for ESLint Parser Error

The error you're seeing is due to missing Babel ESLint parser dependencies. Here's how to fix it:

### Option 1: Delete and Reinstall (Recommended)

```bash
cd frontend
rm -rf node_modules package-lock.json  # On Windows: rmdir /s node_modules & del package-lock.json
npm install --legacy-peer-deps
```

### Option 2: Install Missing Dependencies

```bash
cd frontend
npm install @babel/core @babel/eslint-parser --save-dev
npm install --legacy-peer-deps
```

### Option 3: Skip ESLint During Development

If you want to start quickly without fixing ESLint immediately, you can disable ESLint:

**Create or modify `vue.config.js`:**
```javascript
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,  // This disables ESLint during development
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
```

### What Was Fixed

1. **Added missing Babel dependencies** to `package.json`
2. **Created separate `.eslintrc.js`** file for better configuration
3. **Updated ESLint rules** to be more permissive during development
4. **Fixed Babel configuration** for better compatibility

### Start the Application

After fixing the dependencies:

1. **Backend (Terminal 1):**
   ```bash
   cd backend
   python app.py
   ```

2. **Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run serve
   ```

3. **Open your browser:** http://localhost:8080

The application should now start without ESLint parser errors!