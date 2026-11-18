const $ = (s) => document.querySelector(s);
const theater = $('#theater');
const video = $('#tribute');
const sound = $('.sound-toggle');
let soundOn = false;
let soundChosen = false;
let trigger = null;
function setSound(enabled) {
  soundOn = enabled;
  video.muted = !enabled;
  sound.setAttribute('aria-pressed', String(enabled));
  sound.setAttribute('aria-label', enabled ? 'Mute sound' : 'Enable sound');
  $('.sound-label').textContent = enabled ? 'SOUND ON' : 'SOUND OFF';
}
setSound(false);
sound.addEventListener('click', () => { soundChosen = true; setSound(!soundOn); });
async function launch(time = 0, source) {
  trigger = source || document.activeElement;
  $('.playback-note').textContent = '';
  if (!theater.open) theater.showModal();
  // A deliberate play gesture enables the soundtrack; native video controls can mute it.
  if (!soundChosen) setSound(true);
  video.currentTime = time;
  try { await video.play(); } catch { $('.playback-note').textContent = 'Press play to start the birthday protocol.'; }
}
document.querySelectorAll('.launch').forEach(button => button.addEventListener('click', () => launch(0, button)));
document.querySelectorAll('[data-time]').forEach(button => button.addEventListener('click', () => launch(Number(button.dataset.time), button)));
$('#close-theater').addEventListener('click', () => theater.close());
theater.addEventListener('close', () => { video.pause(); trigger?.focus(); });
theater.addEventListener('click', event => { if (event.target === theater && event.clientX < theater.getBoundingClientRect().left) theater.close(); });
video.addEventListener('volumechange', () => {
  const enabled = !video.muted && video.volume > 0;
  soundOn = enabled;
  sound.setAttribute('aria-pressed', String(enabled));
  sound.setAttribute('aria-label', enabled ? 'Mute sound' : 'Enable sound');
  $('.sound-label').textContent = enabled ? 'SOUND ON' : 'SOUND OFF';
});
video.addEventListener('error', () => { $('.playback-note').textContent = 'The film could not load. Please try the download link below.'; });
const memories = [
  'Ansh giving two thumbs up at a restaurant',
  'Celebrating together with a sparkler',
  'A playful portrait with a smile',
  'A sunny beach selfie together',
  'Three friends by the water',
  'A golden-hour boat ride together',
  'Friends striking a funny pose in the living room',
  'Three friends dressed up for a celebration',
  'Three friends together at night',
  'A mirror selfie together in a shoe store',
  'A candid selfie together at a café',
  'Dressed up together for an event',
  'Three friends in the golden evening light',
  'A full-length photo together at an event',
  'A snowy outdoor memory'
];
let current = 0;
const carousel = $('.carousel');
const cards = memories.map((alt, i) => {
  const button = document.createElement('button');
  button.className = 'memory-card';
  button.setAttribute('aria-label', `Open memory ${i + 1}: ${alt}`);
  const img = document.createElement('img');
  img.src = `/photos/${String(i).padStart(2, '0')}.jpg`;
  img.alt = alt; img.loading = i < 3 || i > 12 ? 'eager' : 'lazy';
  button.append(img);
  const caption = document.createElement('span');
  caption.textContent = `MEMORY_${String(i + 1).padStart(3, '0')} / THE GOOD STUFF`;
  button.append(caption);
  button.addEventListener('click', () => {
    if (i !== current) { current = i; updateCarousel(); } else openLightbox(i);
  });
  carousel.append(button);
  return button;
});
function updateCarousel() {
  const mobile = matchMedia('(max-width:760px)').matches;
  cards.forEach((card, i) => {
    let offset = (i - current + memories.length) % memories.length;
    if (offset > memories.length / 2) offset -= memories.length;
    const abs = Math.abs(offset);
    card.style.transform = `translateX(${offset * (mobile ? 235 : 310)}px) translateZ(${-abs * 130}px) rotateY(${-Math.sign(offset) * Math.min(abs, 2) * 18}deg)`;
    card.style.opacity = abs > 2 ? '0' : String(1 - abs * .20);
    card.style.zIndex = String(10 - abs);
    card.style.pointerEvents = abs > 2 ? 'none' : 'auto';
    card.tabIndex = abs > 2 ? -1 : 0;
    card.setAttribute('aria-hidden', String(abs > 2));
    card.dataset.active = String(offset === 0);
  });
  $('#archive-count').textContent = `${String(current + 1).padStart(2, '0')} / 15`;
}
function step(delta) { current = (current + delta + memories.length) % memories.length; updateCarousel(); }
$('#prev').addEventListener('click', () => step(-1));
$('#next').addEventListener('click', () => step(1));
window.addEventListener('resize', updateCarousel);
let touchX = null;
carousel.addEventListener('touchstart', event => { touchX = event.changedTouches[0].clientX; }, { passive:true });
carousel.addEventListener('touchend', event => {
  if (touchX !== null) { const dx = event.changedTouches[0].clientX - touchX; if (Math.abs(dx) > 45) step(dx > 0 ? -1 : 1); }
  touchX = null;
}, { passive:true });
const lightbox = $('#lightbox');
let lightIndex = 0;
function showPhoto(index) {
  lightIndex = (index + memories.length) % memories.length;
  const image = lightbox.querySelector('img');
  image.src = `/photos/${String(lightIndex).padStart(2, '0')}.jpg`;
  image.alt = memories[lightIndex];
  $('#light-count').textContent = `MEMORY ${String(lightIndex + 1).padStart(2, '0')} / 15`;
}
function openLightbox(index) { showPhoto(index); lightbox.showModal(); }
$('#close-lightbox').addEventListener('click', () => lightbox.close());
$('#light-prev').addEventListener('click', () => showPhoto(lightIndex - 1));
$('#light-next').addEventListener('click', () => showPhoto(lightIndex + 1));
document.addEventListener('keydown', event => {
  if (theater.open) return;
  if (lightbox.open && ['ArrowLeft','ArrowRight'].includes(event.key)) { event.preventDefault(); showPhoto(lightIndex + (event.key === 'ArrowLeft' ? -1 : 1)); }
  else if ($('#archive').contains(document.activeElement) && ['ArrowLeft','ArrowRight'].includes(event.key)) { event.preventDefault(); step(event.key === 'ArrowLeft' ? -1 : 1); }
});
updateCarousel();
