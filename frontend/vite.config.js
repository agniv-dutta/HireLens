import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'node:fs'
import path from 'node:path'

const localResultsPlugin = {
  name: 'hirelens-local-results',
  configureServer(server) {
    server.middlewares.use('/local-results', (_req, res) => {
      const resultsPath = path.resolve(__dirname, '..', 'backend', 'output', 'results.json')

      try {
        const fileContent = fs.readFileSync(resultsPath, 'utf-8')
        res.setHeader('Content-Type', 'application/json; charset=utf-8')
        res.end(fileContent)
      } catch {
        res.statusCode = 200
        res.setHeader('Content-Type', 'application/json; charset=utf-8')
        res.end('[]')
      }
    })
  },
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), localResultsPlugin],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
