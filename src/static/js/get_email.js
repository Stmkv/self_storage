document.querySelector('#calc-form').addEventListener('submit', async e => {
  e.preventDefault()
  const form = e.target
  const formData = new FormData(form)

  const response = await fetch('/request-calculation/get_request/', {
    method: 'POST',
    body: formData,
  })

  const result = await response.json()
  if (response.ok) {
    const errorsContainer = document.querySelector('#calc-errors')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p style="font-size: 24px; color: green;">${field}: ${errors.join(
        ', '
      )}</p>`
    }
  } else {
    const errorsContainer = document.querySelector('#calc-errors')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p style="font-size: 24px; color: red;">${field}: ${errors.join(
        ', '
      )}</p>`
    }
  }
})

document.querySelector('#calc-form2').addEventListener('submit', async e => {
  e.preventDefault()
  const form = e.target
  const formData = new FormData(form)

  const response = await fetch('/request-calculation/get_request/', {
    method: 'POST',
    body: formData,
  })

  const result = await response.json()
  if (response.ok) {
    const errorsContainer = document.querySelector('#calc-errors2')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p style="font-size: 24px; color: green;">${field}: ${errors.join(
        ', '
      )}</p>`
    }
  } else {
    const errorsContainer = document.querySelector('#calc-errors2')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p style="font-size: 24px; color: red;">${field}: ${errors.join(
        ', '
      )}</p>`
    }
  }
})
