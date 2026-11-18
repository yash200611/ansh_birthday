import { stat, readFile } from 'node:fs/promises';
const root = new URL('../public/', import.meta.url);
for (const name of ['index.html','styles.css','app.js','entrance.js','reactor.svg','media/Ansh_Birthday_Protocol.mp4']) {
  const info = await stat(new URL(name, root));
  if (!info.isFile() || !info.size) throw new Error(`Missing or empty static asset: ${name}`);
}
for(let i=0;i<15;i++) await stat(new URL(`photos/${String(i).padStart(2,'0')}.jpg`,root));
const html=await readFile(new URL('index.html',root),'utf8');
if(!html.includes('Birthday Protocol')) throw new Error('Birthday page is missing');
console.log('Validated public/: page, scripts, 15 photos and the birthday film.');
