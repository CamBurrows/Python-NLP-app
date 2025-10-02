const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, // Disable ESLint during development to avoid parser errors
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  configureWebpack: {
    resolve: {
      fallback: {
        "path": false,
        "os": false,
        "crypto": false
      }
    }
  }
})