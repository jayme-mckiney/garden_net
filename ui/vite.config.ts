import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    plugins: [react()],
    define: {
      'process.env.SERVER_HOST': env.SERVER_HOST, 
      'process.env.SERVER_PORT': env.SERVER_PORT 
    }
  }
})
