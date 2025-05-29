document.querySelector('#avatar-form').addEventListener('submit', async e => {
  e.preventDefault()

  console.log('Загрузка аватара')
  const form = e.target
  const formData = new FormData(form)

  try {
    const response = await fetch('/users/upload_avatar/', {
      method: 'POST',
      body: formData,
    })

    const result = await response.json()

    if (response.ok) {
      window.location.href = result.redirect_url
    } else {
      const errorsContainer = document.querySelector('#avatar-errors')
      errorsContainer.innerHTML = ''

      for (const [field, errors] of Object.entries(result.errors)) {
        errorsContainer.innerHTML += `<p style="font-size: 24px; color: red;">${field}: ${errors.join(
          ', '
        )}</p>`
      }
    }
  } catch (error) {
    console.error('Ошибка при загрузке аватара:', error)
    const errorsContainer = document.querySelector('#avatar-errors')
    errorsContainer.innerHTML =
      '<p style="color: red;">Произошла ошибка при загрузке аватара. Пожалуйста, попробуйте снова.</p>'
  }
})
