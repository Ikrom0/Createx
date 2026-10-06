import IMask from "imask";

export default function initInputMask() {
  const phoneInputs = document.querySelectorAll("input[name='phone']")

  if (!phoneInputs.length) return;

  phoneInputs.forEach(input => {
    IMask(input, {
      mask: '+{998} (00) 000-00-00'
    })
  })
}