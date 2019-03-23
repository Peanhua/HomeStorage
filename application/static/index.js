
onEditUserClicked = (user_id) => {
  const url = editUserUrl(user_id)
  location.assign(url)
}

onDeleteUserClicked = (user_id) => {
  if(confirm("Are you sure you want to delete the user?")) {
    const req = new XMLHttpRequest()
    const url = editUserUrl(user_id)
    req.onreadystatechange = function() {
      if(this.readyState === 4) {
        if(this.status === 200) {
          location.reload()
        } else {
          alert(req.responseText)
        }
      }
    }
    req.open("DELETE", url, true)
    req.send(null)
  }
}


onEditProductClicked = (product_id) => {
  const url = editProductUrl(product_id)
  location.assign(url)
}

onDeleteProductClicked = (product_id) => {
  if(confirm("Are you sure you want to delete the product?")) {
    const req = new XMLHttpRequest()
    const url = editProductUrl(product_id)
    req.onreadystatechange = function() {
      if(this.readyState === 4) {
        if(this.status === 200) {
          location.reload()
        } else {
          alert(req.responseText)
        }
      }
    }
    req.open("DELETE", url, true)
    req.send(null)
  }
}