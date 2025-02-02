document.querySelector('#register-form').addEventListener('submit', async e => {
  e.preventDefault()
  const form = e.target
  const formData = new FormData(form)

  const response = await fetch('/users/register/', {
    method: 'POST',
    body: formData,
  })

  const result = await response.json()
  if (response.ok) {
    window.location.href = result.redirect_url
  } else {
    const errorsContainer = document.querySelector('#register-errors')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p>${field}: ${errors.join(', ')}</p>`
    }
  }
})

document.querySelector('#login-form').addEventListener('submit', async e => {
  e.preventDefault()
  const form = e.target
  const formData = new FormData(form)

  const response = await fetch('/users/login/', {
    method: 'POST',
    body: formData,
  })

  const result = await response.json()
  if (response.ok) {
    window.location.href = result.redirect_url
  } else {
    const errorsContainer = document.querySelector('#login-errors')
    errorsContainer.innerHTML = `<p>${result.message}</p>`
  }
})
