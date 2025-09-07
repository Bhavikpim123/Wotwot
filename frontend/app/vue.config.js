const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true),
        // define other feature flags here if needed
      }),
    ],
    devtool: 'source-map'  // better debugging
  },
  devServer: {
    allowedHosts: 'all',  // Disable host checking
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:8004', // Load from .env
        changeOrigin: true,
        secure: false,
        logLevel: 'debug'
      },
    },
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
      overlay: false,   // disable overlay completely
      logging: 'info'
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    }
  },
};
