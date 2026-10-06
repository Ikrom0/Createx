export default function initSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const openButton = document.querySelector('[data-sidebar-open]');
  const closeButton = document.querySelector('[data-sidebar-close]');
  const overlay = document.querySelector('[data-sidebar-overlay]');

  if (!sidebar) return;
  function openSidebar() {
      sidebar.classList.add('sidebar--open');
      overlay.classList.add('sidebar-overlay--visible');
      document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
      sidebar.classList.remove('sidebar--open');
      overlay.classList.remove('sidebar-overlay--visible');
      document.body.style.overflow = '';
  }

  openButton.addEventListener('click', openSidebar);
  closeButton.addEventListener('click', closeSidebar);
  overlay.addEventListener('click', closeSidebar);
}






