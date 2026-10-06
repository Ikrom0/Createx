export default function initHeader() {
  const header = document.querySelector('.header');
  const headerNav = document.querySelector('.header__nav');
  const burger = document.querySelector('.burger');
  const headerNavItems = document.querySelectorAll('.header__nav-item')

  if (!header) return;
  window.addEventListener('scroll', () => {
    const isFixed = window.scrollY >= 600;

    header.classList.toggle('header--fixed', isFixed);
  });

  burger.addEventListener('click', () => {
    burger.classList.toggle('burger--open');
    headerNav.classList.toggle('header__nav--open');

    burger.setAttribute(
      'aria-expanded', 
      burger.classList.contains('burger--open')
    );
  });

  headerNavItems.forEach(item => {
    item.addEventListener('click', () => {
      if (window.innerWidth < 992) {
        item.classList.toggle('header__nav-item--open')
      }
    })
  })
}