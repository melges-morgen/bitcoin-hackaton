module.exports = {
  entry: ["babel-polyfill", "./src/index.js"],
  output: {
    filename: "./app.js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
            plugins: ["@babel/plugin-transform-async-to-generator"]
          }
        }
      }
    ]
  }
};
