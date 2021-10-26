module.exports = {
  lintOnSave: false,

  transpileDependencies: ["vuetify"],

  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
    }
  }
};
