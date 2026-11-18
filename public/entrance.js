(() => {
  const gate = document.querySelector('#suit-entrance');
  if (!gate || typeof gate.showModal !== 'function') return;
  const enter = gate.querySelector('.entrance-enter');
  const skip = gate.querySelector('.entrance-skip');
  const status = gate.querySelector('.entrance-status');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let openingTimer;
  let readyTimer;
  let closeTimer;
  let leaving = false;
  const finish = () => {
    gate.close();
    document.querySelector('.hero-actions .launch')?.focus({ preventScroll: true });
  };
  const leave = () => {
    if (leaving) return;
    leaving = true;
    clearTimeout(openingTimer);
    clearTimeout(readyTimer);
    if (reduced) finish();
    else { gate.classList.add('entrance-leaving'); closeTimer = setTimeout(finish, 550); }
  };
  enter.addEventListener('click', leave);
  skip.addEventListener('click', leave);
  gate.addEventListener('cancel', event => { event.preventDefault(); leave(); });
  gate.addEventListener('close', () => {
    clearTimeout(openingTimer); clearTimeout(readyTimer); clearTimeout(closeTimer);
  });
  gate.showModal();
  skip.focus({ preventScroll: true });
  openingTimer = setTimeout(() => {
    if (!gate.open || leaving) return;
    gate.classList.add('faceplate-open');
    readyTimer = setTimeout(() => {
      if (!gate.open || leaving) return;
      gate.classList.add('entrance-ready');
      status.textContent = 'J.A.R.V.I.S. / WELCOME BACK, ANSH.';
      enter.disabled = false;
    }, reduced ? 0 : 1550);
  }, reduced ? 0 : 650);
})();
