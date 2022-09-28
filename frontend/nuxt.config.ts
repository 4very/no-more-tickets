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
    config: {
      content: [
        'components/**/*.{vue,js}',
        'layouts/**/*.vue',
        'pages/**/*.vue',
        'composables/**/*.{js,ts}',
        'plugins/**/*.{js,ts}',
        'App.{js,ts,vue}',
        'app.{js,ts,vue}'
      ],
      theme: {
        extend: {}
      },
      plugins: []
    }
  }
});
