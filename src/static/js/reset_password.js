document
  .querySelector('#forgot-password-form')
  .addEventListener('submit', async e => {
    e.preventDefault()
    const form = e.target
    const formData = new FormData(form)

    const response = await fetch('/users/password_reset/', {
      method: 'POST',
      body: formData,
    })

    const result = await response.json()

    if (response.ok) {
      const successContainer = document.querySelector(
        '#forgot-password-success'
      )
      successContainer.innerHTML =
        'Инструкции для восстановления пароля отправлены на вашу почту.'
      successContainer.style.display = 'block'

      const errorContainer = document.querySelector('#forgot-password-error')
      errorContainer.style.display = 'none'
      form.reset()

      $('#forgotPasswordModal').modal('hide')
    } else {
      const errorContainer = document.querySelector('#forgot-password-error')
      errorContainer.innerHTML =
        result.message ||
        'Произошла ошибка при отправке запроса. Пожалуйста, попробуйте позже.'
      errorContainer.style.display = 'block'
    }
  })
