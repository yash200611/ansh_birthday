import http from 'node:http';
import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import path from 'node:path';
const root = path.resolve(process.argv[2] || '.');
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.jpg':'image/jpeg', '.svg':'image/svg+xml', '.mp4':'video/mp4', '.wav':'audio/wav' };
const server = http.createServer(async (req,res) => {
 try {
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const clean=pathname==='/'?'index.html':pathname.replace(/^\/+/, '');
  let file=path.resolve(root,clean);
  if (!file.startsWith(root+path.sep)) {res.writeHead(403).end();return;}
  try {await stat(file);} catch {file=path.resolve(root,'public',clean);}
  if (!file.startsWith(root+path.sep)) {res.writeHead(403).end();return;}
  const info=await stat(file);if(!info.isFile())throw new Error('Missing');
  const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Accept-Ranges':'bytes'};
  if(req.headers.range){
   const match=/^bytes=(\d+)-(\d*)$/.exec(req.headers.range);
   if(!match){res.writeHead(416,{'Content-Range':`bytes */${info.size}`}).end();return;}
   const start=Number(match[1]),end=match[2]?Math.min(Number(match[2]),info.size-1):info.size-1;
   if(start>end||start>=info.size){res.writeHead(416,{'Content-Range':`bytes */${info.size}`}).end();return;}
   res.writeHead(206,{...headers,'Content-Range':`bytes ${start}-${end}/${info.size}`,'Content-Length':end-start+1});if(req.method==='HEAD'){res.end();return;}createReadStream(file,{start,end}).pipe(res);
  } else {res.writeHead(200,{...headers,'Content-Length':info.size});if(req.method==='HEAD'){res.end();return;}createReadStream(file).pipe(res);}
 }catch{res.writeHead(404,{'Content-Type':'text/plain'}).end('Not found');}
});
server.listen(Number(process.env.PORT)||3000,'127.0.0.1',()=>console.log(`Local: http://127.0.0.1:${server.address().port}`));
