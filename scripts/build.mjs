import { mkdir, copyFile, cp, rm, stat } from 'node:fs/promises';
await stat(new URL('../public/media/Ansh_Birthday_Protocol.mp4', import.meta.url));
const root = new URL('../', import.meta.url);
await rm(new URL('dist/', root), { recursive: true, force: true });
await mkdir(new URL('dist/', root), { recursive: true });
for (const name of ['index.html', 'styles.css', 'app.js']) await copyFile(new URL(name, root), new URL(`dist/${name}`, root));
await cp(new URL('public/', root), new URL('dist/', root), { recursive: true });
console.log('Built dist/ — ready for Vercel.');
