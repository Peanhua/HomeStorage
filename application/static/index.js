
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


onEditHomeUsersClicked = (home_id) => {
  const url = editHomeUsersUrl(home_id)
  location.assign(url)
}


/* Activates all entries in select_lists before submitting to the server. */
onSubmitFormClicked = (event, select_lists) => {
  //event.preventDefault()

  select_lists.forEach(list_id => {
    const list = document.getElementById(list_id)
    if(list) {
      for(let i = 0; i < list.options.length; i++) {
        option = list.options.item(i)
        option.selected = true
      }
    }
  })
}


onMoveBetweenListsClicked = (event, list_from_id, list_to_id) => {
  event.preventDefault()

  moveOne = (list_from, list_to) => {
    const ind = list_from.selectedIndex
    
    if(ind >= 0 && ind < list_from.options.length) {
      oldopt = list_from.options[ind]
      
      newopt = document.createElement("option")
      newopt.value = oldopt.value
      newopt.text = oldopt.text
      list_to.add(newopt)
      
      list_from.remove(ind)
      
      return true

    } else {
      return false
    }
  }

  const lfrom = document.getElementById(list_from_id)
  const lto   = document.getElementById(list_to_id)

  while(moveOne(lfrom, lto)) {
    /* */
  }
}
