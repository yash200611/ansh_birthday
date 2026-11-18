# Ansh — Birthday Protocol

A cinematic birthday website and 45-second vertical film for Ansh. Built with HTML, CSS and JavaScript, with no runtime dependencies or backend.

## Local development

Run `npm run dev` and open http://127.0.0.1:3000. Requires Node.js 22+.

## Vercel

Import this repository into Vercel. `vercel.json` configures `npm run build` and output directory `public`. No environment variables are needed.

## Included

- Animated armor entrance: an opening faceplate reveals Ansh, then “TIME FOR WAR” and “GET IN” lead into the app. Includes skip, Escape, keyboard focus handling, and reduced-motion support.
- Responsive landing page, arc-reactor portrait, full-screen film player and MP4 download.
- Seven chapter controls, a 15-photo perspective carousel, swipe and keyboard navigation, photo lightbox and reduced-motion support.
- Original photos in `source/photos`, web photos in `public/photos`, supplied audio and editable rendering scripts.

## Film

`public/media/Ansh_Birthday_Protocol.mp4`: exactly 45 seconds, 1080 × 1920, 30 fps, H.264 and stereo AAC.

Uses the supplied **The Avengers – Alan Silvestri.mp3**, **1:18 through 2:03**, with startup effects underneath the opening. The birthday message remains through the musical tail before fading to black.

| Video | Audio source | Chapter |
|---|---|---|
| 0:00–0:05 | 1:18–1:23 | JARVIS activation |
| 0:05–0:12 | 1:23–1:30 | Bollywood buff |
| 0:12–0:19 | 1:30–1:37 | Marvel geek |
| 0:19–0:26 | 1:37–1:44 | Best dancer |
| 0:26–0:33 | 1:44–1:51 | My GOAT |
| 0:33–0:40 | 1:51–1:58 | Brother and bestest friend |
| 0:40–0:45 | 1:58–2:03 | Birthday and Love You 3000 |

Photographs retain their original faces. The themed chapters use the supplied personal photos; no separate Marvel or dance photos were supplied. The opening has text and sound effects, without spoken dialogue.

## Regenerate the video

From the repository root:

```sh
python3 -m pip install -r scripts/requirements.txt
mkdir -p build
python3 scripts/render_tribute.py
python3 scripts/mix_audio.py
npm run build
```

The renderer uses macOS Arial fonts at `/System/Library/Fonts/Supplemental/`; adjust `fontdir` on other systems. Vercel builds do not require Python or these fonts.

The deploy directory is checked into Git as `public/`. The build validates those static files; it does not rely on generating a separate output folder.
