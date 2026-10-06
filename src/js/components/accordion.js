export default function initAccordion() {

  const accordions = document.querySelectorAll('.accordion-item')
  const accordionOpen = 'accordion-item--open'
  const accordionBtn = '.accordion-btn'
  const accordionContent = '.accordion-content'

  if (!accordions.length) return

  accordions.forEach((item, i) => {

    const btn = item.querySelector(accordionBtn)
    const panel = item.querySelector(accordionContent)

    if (!btn || !panel) return

    if (i === 0) {
      item.classList.add(accordionOpen)
      panel.style.maxHeight = panel.scrollHeight + 'px'
      btn.setAttribute('aria-expanded', true)
    }

    btn.addEventListener('click', () => {

      const isOpen = item.classList.contains(accordionOpen)

      accordions.forEach(other => {

        const otherBtn = other.querySelector(accordionBtn)
        const otherPanel = other.querySelector(accordionContent)

        other.classList.remove(accordionOpen)
        otherBtn?.setAttribute('aria-expanded', false)
        if (otherPanel) otherPanel.style.maxHeight = null

      })

      if (!isOpen) {

        item.classList.add(accordionOpen)
        btn.setAttribute('aria-expanded', true)
        panel.style.maxHeight = panel.scrollHeight + 'px'

      }

    })

  })

}