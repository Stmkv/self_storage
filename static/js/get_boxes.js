document.querySelectorAll('.SelfStorage__btn2_green').forEach(button => {
  button.addEventListener('click', function () {
    const warehouseId = this.dataset.warehouseId
    if (!warehouseId) {
      console.error('ID склада отсутствует!')
      return
    }

    console.log(`Отправляется запрос для склада с ID: ${warehouseId}`)

    fetch(`/warehouses/${warehouseId}/boxes/`, {
      method: 'GET',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        console.log('Данные боксов:', data)

        const boxesContainer = document.querySelector('#pills-tabContent')
        boxesContainer.innerHTML = ''
        if (!data.boxes || data.boxes.length === 0) {
          boxesContainer.innerHTML =
            '<p class="fs_24 text-center">Нет свободных боксов</p>'
        } else {
          data.boxes.forEach(box => {
            boxesContainer.innerHTML += `
                      <a href="#" class="row text-decoration-none py-3 px-4 mt-5 SelfStorage__boxlink">
                          <div class="col-12 col-md-4 col-lg-3 d-flex justify-content-center align-items-center">
                              <span class="SelfStorage_green fs_24 me-2">Бокс №${box.number}</span>
                          </div>
                          <div class="col-6 col-md-4 col-lg-3 d-flex justify-content-center align-items-center">
                              <span class="fs_24">${box.box_type}</span>
                          </div>
                          <div class="col-6 col-md-4 col-lg-3 d-flex justify-content-center align-items-center">
                              <span class="fs_24">Цена: ${box.price_per_month} ₽</span>
                          </div>
                      </a>
                  `
          })
        }
      })
      .catch(error => console.error('Ошибка загрузки боксов:', error))
  })
})
