document.querySelector('#edit-form').addEventListener('submit', async e => {
  e.preventDefault()
  const form = e.target
  const formData = new FormData(form)

  const response = await fetch('/users/edit-profile/', {
    method: 'POST',
    body: formData,
  })

  const result = await response.json()
  if (response.ok) {
    window.location.href = result.redirect_url
  } else {
    const errorsContainer = document.querySelector('#edit-errors')
    errorsContainer.innerHTML = ''
    for (const [field, errors] of Object.entries(result.errors)) {
      errorsContainer.innerHTML += `<p style="font-size: 24px; color: red;">${field}: ${errors.join(
        ', '
      )}</p>`
    }
  }
})

document.getElementById('edit').addEventListener('click', e => {
  e.preventDefault()
  document.getElementById('EMAIL').disabled = false
  document.getElementById('PHONE').disabled = false
  document.getElementById('edit').style.display = 'none'
  document.getElementById('save').style.display = 'inline-block'
})
document.getElementById('save').addEventListener('click', () => {
  setTimeout(() => {
    document.getElementById('EMAIL').disabled = true
    document.getElementById('PHONE').disabled = true
    document.getElementById('edit').style.display = 'inline-block'
    document.getElementById('save').style.display = 'none'
  }, 0)
})
