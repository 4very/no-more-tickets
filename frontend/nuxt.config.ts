export default defineNuxtConfig({
  /*
   ** Nuxt modules
   */
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt'
  ],

  components: {
    global: true,
    dirs: ['~/components']
  },

  typescript: {
    tsConfig: {
      compilerOptions: {
        jsx: 'preserve',
        target: 'ES2018',
        module: 'ESNext',
        moduleResolution: 'Node',
        lib: ['ESNext', 'ESNext.AsyncIterable', 'DOM'],
        esModuleInterop: true,
        allowJs: true,
        sourceMap: true,
        strict: true,
        noEmit: true,
        experimentalDecorators: true
      },
      exclude: ['node_modules', '.nuxt', 'dist']
    }
  },

  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js',
    viewer: true
  }
});
