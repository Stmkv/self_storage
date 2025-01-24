document.querySelectorAll('.SelfStorage__btn2_green').forEach(button => {
  button.addEventListener('click', function () {
    const warehouseId = this.dataset.warehouseId

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
                          <div class="col-12 col-lg-3">
                        <a href="/order/?box_id=${box.id}&box_type=${box.box_type}&warehouse_id=${box.warehouse_id}&price=${box.price_per_month}" class="btn my-2 w-100 text-white fs_24 SelfStorage__bg_orange SelfStorage__btn2_orange border-8">
                          Оформить заказ
                        </a>
                          </div>
                      </a>
                    `
          })
        }
      })
      .catch(error => console.error('Ошибка загрузки боксов:', error))
  })
})
