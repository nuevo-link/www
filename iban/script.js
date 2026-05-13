/* ===========================
   BANCO SANTANDER - SCRIPT
   =========================== */

// ── SLIDER ──
let currentSlide = 0;
let totalSlides = 2;
let autoplayInterval = null;
let isPaused = false;

function goToSlide(index) {
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.slider-dot');
  slides[currentSlide].classList.remove('slide--active');
  dots[currentSlide].classList.remove('slider-dot--active');
  currentSlide = (index + totalSlides) % totalSlides;
  slides[currentSlide].classList.add('slide--active');
  dots[currentSlide].classList.add('slider-dot--active');
}

function changeSlide(dir) {
  goToSlide(currentSlide + dir);
  if (!isPaused) resetAutoplay();
}

function startAutoplay() {
  autoplayInterval = setInterval(() => { goToSlide(currentSlide + 1); }, 5000);
}

function resetAutoplay() {
  clearInterval(autoplayInterval);
  startAutoplay();
}

function togglePause() {
  isPaused = !isPaused;
  const btn = document.getElementById('pauseBtn');
  if (isPaused) {
    clearInterval(autoplayInterval);
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>';
  } else {
    startAutoplay();
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
  }
}

// Touch swipe
let touchStartX = 0;
const slider = document.querySelector('.hero-slider');
if (slider) {
  slider.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
  slider.addEventListener('touchend', e => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) changeSlide(diff > 0 ? 1 : -1);
  }, { passive: true });
}

// ── MOBILE MENU ──
function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  menu.classList.toggle('open');
}

// ── HEADER SCROLL ──
window.addEventListener('scroll', () => {
  const header = document.getElementById('header');
  if (header) {
    header.style.boxShadow = window.scrollY > 10 ? '0 4px 16px rgba(0,0,0,0.12)' : '0 2px 8px rgba(0,0,0,0.08)';
  }
});

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
  startAutoplay();
});
