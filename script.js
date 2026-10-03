// Stagger the letter "convergence" animation on load
document.querySelectorAll('.letter').forEach((el, i) => {
  el.style.animationDelay = `${i * 0.04}s`;
});

// One-time "epoch" counter that ticks up then settles — mirrors a model converging
const counterEl = document.getElementById('epochCounter');
if (counterEl && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let epoch = 0;
  let loss = 1.0;
  const totalSteps = 12;
  const finalLoss = 0.043;

  const interval = setInterval(() => {
    epoch++;
    loss = 1.0 - (1.0 - finalLoss) * (epoch / totalSteps);
    counterEl.textContent = `epoch ${String(epoch).padStart(3, '0')} · loss ${loss.toFixed(3)}`;
    if (epoch >= totalSteps) {
      clearInterval(interval);
      counterEl.textContent = `epoch ${String(totalSteps).padStart(3, '0')} · loss ${finalLoss.toFixed(3)}`;
    }
  }, 90);
}
