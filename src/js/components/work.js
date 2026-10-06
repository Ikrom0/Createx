let currentCategory = 'all';
let currentPage = 1;

function initFilters() {
  document.addEventListener('click', e => {
    const filter = e.target.closest('.projects__filter');
    if (!filter) return;

    document
      .querySelectorAll('.projects__filter')
      .forEach(f => f.classList.remove('projects__filter--active'));

    filter.classList.add('projects__filter--active');

    currentCategory = filter.dataset.filter
    currentPage = 1;
    loadProjects(currentCategory, 1, false);

  });
}

function initLoadMore() {
  document.addEventListener('click', e => {
    const btn = e.target.closest('.projects__load-btn');
    if (!btn) return;

    currentPage += 1;
    loadProjects(currentCategory, currentPage, true);
  });
}

function loadProjects(category, page, append) {
  const list = document.querySelector('.projects__list');
  const loadMoreWrap = document.querySelector('.projects__load');

  list.style.transition = 'opacity 0.2s ease';
  if (!append) list.style.opacity = '0';

  const doFetch = () => {
    fetch(`/work?category=${category}&page=${page}`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(res => res.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const cards = doc.querySelectorAll('.projects__card');
        const hasMore = doc.querySelector('[data-has-more]')?.dataset.hasMore === 'true';

        if (append) {
          cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transition = 'opacity 0.3s ease';
            list.appendChild(card);

            requestAnimationFrame(() => {
              requestAnimationFrame(() => {
                card.style.opacity = '1';
              });
            });
          });
        } else {
          list.innerHTML = '';
          cards.forEach(card => list.appendChild(card));
        }

        if (loadMoreWrap) loadMoreWrap.style.display = hasMore ? '' : 'none';
        list.style.opacity = '1';

        if (!append) {
          let url = '/work';

          if (category !== 'all') {
            url = `/work?category=${category}`;

            if (page !== 1) {
              url += `&page=${page}`;
            }
          } else if (page !== 1) {
            url = `/work?page=${page}`;
          }

          history.replaceState({ page, category }, '', url);
        }
      })
      .catch(() => {
        if (!append) {
          list.innerHTML = '<p>Не удалось загрузить проекты. Попробуйте ещё раз.</p>';
        }

        list.style.opacity = '1';
      });
  };

  if (append) {
    doFetch();
  } else {
    list.addEventListener('transitionend', doFetch, { once: true });
  }
}

function initFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  const category = urlParams.get('category') || 'all';

  document.querySelectorAll('.projects__filter').forEach(btn => {
    btn.classList.toggle(
      'projects__filter--active', 
      btn.dataset.filter === category
    );
  });

  currentCategory = category
}

export default function initPortfolio() {
  initFilters();
  initLoadMore();
  initFromURL();
}