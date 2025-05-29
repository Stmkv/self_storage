function sendQRCode(orderId) {
  fetch(`/users/orders/${orderId}/send-qr/`, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Ошибка:', error))
}
