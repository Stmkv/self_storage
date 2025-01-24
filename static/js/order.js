document.addEventListener('DOMContentLoaded', function () {
  const calculateBtn = document.getElementById('calculate-cost-btn')
  const submitBtn = document.getElementById('submit-btn')
  const costDisplay = document.getElementById('calculated-cost')

  calculateBtn.addEventListener('click', function () {
    const startDateInput = document.getElementById('id_start_date')
    const endDateInput = document.getElementById('id_end_date')
    const price = new URLSearchParams(window.location.search).get('price')
    const parsedPrice = Number(price.replace(',', '.'))

    const startDate = new Date(startDateInput.value)
    console.log(startDate)
    const endDate = new Date(endDateInput.value)
    console.log(endDate)
    if (!startDateInput.value || !endDateInput.value || startDate >= endDate) {
      costDisplay.textContent = 'Введите корректные даты!'
      costDisplay.classList.add('text-danger')
      costDisplay.classList.remove('text-success')
      return
    }
    const days = (endDate - startDate) / (1000 * 60 * 60 * 24)
    console.log(days)
    const SumPrice = days * (Number(parsedPrice) / 30)
    console.log(SumPrice)
    costDisplay.textContent = `Стоимость аренды: ${Math.floor(SumPrice)} ₽`
    costDisplay.classList.add('text-success')
    costDisplay.classList.remove('text-danger')

    submitBtn.style.display = 'inline-block'
  })
})
