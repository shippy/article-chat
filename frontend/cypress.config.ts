import { defineConfig } from "cypress";
import 'dotenv/config';

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:5173",
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },

  env: {
    'cognito_domain': 'https://auth.journalarticle.chat',
    'cognito_username': process.env.CYPRESS_cognito_username,
    'cognito_password': process.env.CYPRESS_cognito_password,
  },
  
  component: {
    devServer: {
      framework: "vue",
      bundler: "vite",
    },
  },
});
