node .output/server/index.mjs &
npx tailwind-config-viewer serve -p 3001 &
wait -n
exit $?