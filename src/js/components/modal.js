export default function initModals() {

  const openBtns = document.querySelectorAll('[data-modal-open]')

  openBtns.forEach(btn => {

    btn.addEventListener('click', () => {

      const name = btn.dataset.modalOpen
      const modal = document.querySelector(`[data-modal="${name}"]`)

      if (!modal) return;

      modal.classList.add('modal--active')
      document.documentElement.style.overflow = "hidden";

    })

  })


  const modals = document.querySelectorAll('[data-modal]')

  modals.forEach(modal => {

    const closeBtn = modal.querySelector('[data-modal-close]')

    if (closeBtn) {
      closeBtn.addEventListener('click', () => closeModal(modal))
    }

    modal.addEventListener('click', e => {
      if (e.target === modal) closeModal(modal)
    })

  })

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document
        .querySelectorAll('.modal--active')
        .forEach(closeModal)
    }
  })

}

const closeModal = modal => {
  modal.classList.remove('modal--active')
  document.documentElement.style.overflow = "";
}