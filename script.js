const lensData = {
  overall: {
    kicker: 'Overall MAE, lower is better',
    headline: 'XGBoost delta has the lowest point-estimate error.',
    explanation: 'Its advantage is driven by large, volatile country-year rows. The uncertainty interval still includes zero.',
    takeaway: '<strong>Interpretation:</strong> XGBoost delta is the overall point winner, but the evidence does not establish a uniform or statistically settled advantage.',
    rows: [
      ['XGBoost delta', '9.345', 'MtCO<sub>2</sub>', 'winner'],
      ['Linear trend', '9.751', 'MtCO<sub>2</sub>', ''],
      ['HGB delta', '10.369', 'MtCO<sub>2</sub>', ''],
      ['Persistence', '11.004', 'MtCO<sub>2</sub>', 'baseline']
    ]
  },
  typical: {
    kicker: 'Median absolute error, lower is better',
    headline: 'Persistence is best for the typical country.',
    explanation: 'Its MedianAE is 1.367 MtCO2 and its median percentage error is 5.055%, both lower than XGBoost delta.',
    takeaway: '<strong>Interpretation:</strong> the ML gain is not a typical-country gain. It mainly reflects fewer large errors among the biggest emitters.',
    rows: [
      ['Persistence', '1.367', 'MtCO<sub>2</sub>', 'winner baseline'],
      ['HGB delta', '1.419', 'MtCO<sub>2</sub>', ''],
      ['Linear trend', '1.450', 'MtCO<sub>2</sub>', ''],
      ['XGBoost delta', '1.486', 'MtCO<sub>2</sub>', '']
    ]
  }
};

const lensButtons = document.querySelectorAll('[data-lens]');
const ranking = document.querySelector('[data-ranking]');
const lensKicker = document.querySelector('[data-lens-kicker]');
const lensHeadline = document.querySelector('[data-lens-headline]');
const lensExplanation = document.querySelector('[data-lens-explanation]');
const lensTakeaway = document.querySelector('[data-lens-takeaway]');

function renderLens(key) {
  const data = lensData[key];
  if (!data || !ranking) return;

  lensButtons.forEach((button) => {
    const active = button.dataset.lens === key;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  });

  lensKicker.textContent = data.kicker;
  lensHeadline.textContent = data.headline;
  lensExplanation.textContent = data.explanation;
  lensTakeaway.innerHTML = data.takeaway;
  ranking.innerHTML = data.rows.map((row, index) => {
    const [model, value, unit, status] = row;
    const classes = ['rank-row'];
    if (status.includes('winner')) classes.push('is-winner');
    if (status.includes('baseline')) classes.push('is-baseline');
    return `<li class="${classes.join(' ')}">
      <span class="rank-number">${index + 1}</span>
      <span class="rank-model">${model}</span>
      <strong>${value}</strong>
      <span class="rank-unit">${unit}</span>
    </li>`;
  }).join('');
}

lensButtons.forEach((button) => {
  button.addEventListener('click', () => renderLens(button.dataset.lens));
});

const themeToggle = document.querySelector('[data-theme-toggle]');
const themeLabel = document.querySelector('[data-theme-label]');

function updateThemeControl() {
  if (!themeToggle) return;
  const dark = document.documentElement.dataset.theme === 'dark';
  themeToggle.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  themeLabel.textContent = dark ? 'Light' : 'Dark';
}

themeToggle?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('co2-site-theme', next); } catch (_) {}
  updateThemeControl();
});

updateThemeControl();
