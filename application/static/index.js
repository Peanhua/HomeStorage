
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
        if(this.status === 204) {
          location.reload()
        } else if(this.status == 405) {
          alert(req.responseText)
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


onStockAdjustClicked = (product_id, amount) => {
  const cur = document.getElementById("curquant_" + product_id)
  const curval = parseInt(cur.value)
  const change = document.getElementById("change_" + product_id)
  const newquant = document.getElementById("newquant_" + product_id)

  
  let changeval = parseInt(change.value) + amount
  let newcur = (curval + changeval)

  if(newcur < 0) {
    newcur    = 0
    changeval = -curval
  } else if(changeval > 9999) {
    changeval = 9999
    newcur    = curval + changeval
  }
  
  change.value = changeval
  newquant.innerHTML = newcur
}



onShowReportClicked = (report_id) => {
  const homeselect = document.getElementById("home_select_" + report_id)
  const home_id = homeselect.options[homeselect.selectedIndex].value
  
  const param1input = document.getElementById("param1_" + report_id)
  const param1 = param1input.value
  
  const url = showReportUrl(report_id, home_id, param1)
  location.assign(url)
}



onDeleteStorageClicked = (storage_id) => {
  const req = new XMLHttpRequest()
  const url = deleteStorageUrl(storage_id)
  req.onreadystatechange = function() {
    if(this.readyState === 4) {
      if(this.status === 200) {
        location.assign(req.responseText)
      } else {
        alert(req.responseText)
      }
    }
  }
  req.open("DELETE", url, true)
  req.send(null)
}
