function showToast(message, type="success") {
  const existingToast = document.querySelector(".toast");

  if (existingToast) {
    existingToast.remove();
  }

  const toast = document.createElement('div');
  toast.textContent = message
  toast.classList.add("toast", `toast--${type}`)
  document.body.append(toast)

  requestAnimationFrame(() => {
    toast.classList.add("toast--show")
  })

  setTimeout(() => {
    toast.classList.remove("toast--show");

    setTimeout(() => {
      toast.remove();
    }, 300)
  }, 3000)
}

function clearFieldError(field) {
  const error = field.nextElementSibling

  if (error?.classList.contains('form-error')) {
    error.remove()
  }

  field.classList.remove("is-invalid")

}

function showErrors(form, errors) {
  form.querySelectorAll(".form-error").forEach(error => error.remove())
  form.querySelectorAll(".is-invalid").forEach(field => {
    field.classList.remove("is-invalid")
  })

  for (const [field, message] of Object.entries(errors)) {
    const input = form.querySelector(`[name="${field}"]`)

    if (!input) continue;

    const error = document.createElement("span")
    error.textContent = message
    error.className = "form-error"
    input.classList.add("is-invalid")

    if (input.tagName === "SELECT") {
      input.parentElement.after(error)
    } else {
      input.after(error)
    }
  }
}

export default function setupForm(selector, formType) {
  const forms = document.querySelectorAll(`${selector}`)

  if (!forms.length) return;

  forms.forEach(form => {
    const fields = form.querySelectorAll("input, select, textarea")

    fields.forEach(field => {
      ["input", "change"].forEach(event => {
        field.addEventListener(event, () => clearFieldError(field))
      })
    })

    form.addEventListener("submit", async (event) => {
      event.preventDefault()

      const formData = new FormData(form)

      const response = await fetch(form.action, {
        method: form.method,
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        if (data.errors) {
          showErrors(form, data.errors)
        } else {
          showToast(data.message, "error")
        }
        return
      }

      if (formType === "comment") {
        const commentList = document.querySelector("[data-comments-list]")
        const li = document.createElement('li')

        li.className = "comments__list-item"

        li.innerHTML = `
        <div>
          <span class="comments__meta-author"></span>
          <time class="comments__meta-date"></time>
        </div>

        <p class="comments__text"></p>
      `

        li.querySelector(".comments__meta-author").textContent = data.comment.name
        li.querySelector(".comments__meta-date").textContent = data.comment.date
        li.querySelector(".comments__meta-date").dateTime = data.comment.datetime
        li.querySelector(".comments__text").textContent = data.comment.message

        commentList.prepend(li)
        const commentsCount = document.querySelector("[data-comments-count]")
        commentsCount.textContent = data.comments_count
      }

      if (data.redirect_url) {
        window.location.href = data.redirect_url
        return
      }

      showToast(data.message)
      form.reset()

      if (formType === "modal") {
        const modal = form.closest(".modal")
        modal?.querySelector("[data-modal-close]").click()

        return
      }
    })
  })

}