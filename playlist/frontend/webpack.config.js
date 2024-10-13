const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,  // Match both .js and .jsx files
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],  // Use the presets for React and modern JS
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Resolve these extensions
  },
  // module: {
  //       rules: [
  //           {
  //               test: /\.css$/,
  //               use: ['style-loader', 'css-loader'],
  //           },
  //       ],
  //   },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("production"),
      },
    }),
  ],
};