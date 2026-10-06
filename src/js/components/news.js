const container = document.querySelector('.news__wrapper');
const newsSection = document.querySelector('.news');
let currentCategory = 'all';

function initFilters() {
  document.addEventListener('click', e => {
    const filter = e.target.closest('.news__filter');
    if (!filter) return;

    document
      .querySelectorAll('.news__filter')
      .forEach(f => f.classList.remove('news__filter--active'));

    filter.classList.add('news__filter--active');

    currentCategory = filter.dataset.filter;
    loadPage(currentCategory, 1);
  });
}

function initFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  const category = urlParams.get('category') || 'all';

  document.querySelectorAll('.news__filter').forEach(btn => {
    btn.classList.toggle(
      'news__filter--active',
      btn.dataset.filter === category
    );
  });

  currentCategory = category
}

function initPagination() {
  document.addEventListener('click', e => {
    const link = e.target.closest('.news__pagination-link');
    if (!link) return;

    e.preventDefault();
    loadPage(currentCategory, parseInt(link.dataset.page));
  });
}

function loadPage(category, page) {
  container.style.transition = 'opacity 0.2s ease';
  container.style.opacity = '0';

  container.addEventListener('transitionend', () => {
    fetch(`/news?category=${category}&page=${page}`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(res => res.text())
      .then(html => {
        newsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        container.innerHTML = html;
        container.style.opacity = '1';
        let url = '/news';

        if (category !== 'all') {
          url = `/news?category=${category}`;

          if (page !== 1) {
            url += `&page=${page}`;
          }
        } else if (page !== 1) {
          url = `/news?page=${page}`;
        }

        history.replaceState({ page, category }, '', url);
      })
      .catch(() => {
        container.innerHTML = '<p>Failed to load articles. Try again.</p>';
        container.style.opacity = '1';
      });
  }, { once: true });
}

export default function initNews() {
  initFilters();
  initPagination();
  initFromURL();
}