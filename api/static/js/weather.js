function appendData(data, element) {
  console.log("appendData")
  for (const [key, value] of Object.entries(data)) {
    var div = document.createElement("div");
    var str = JSON.stringify(value, null, 2); // spacing level = 2
    div.innerHTML = key + ':' + str;

    element.appendChild(div);
  }
}

window.addEventListener('load', function () {
  let submitButton = document.getElementById("submit");
  submitButton.onclick = (e) => {
    event.preventDefault()
    var url = new URL(window.location.origin + "/api/weather"),
    params = {
      city: document.getElementById("id_city").value, 
      period: document.getElementById("id_period").value, 
    };
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    const results = document.getElementById("results");
    results.innerHTML = '<span>Fetching data...</span>';
    fetch(url).then((response) => {
      response.json().then(result => {
        results.innerHTML = '';
        appendData(result, results);
      }).catch(e => {
        results.innerHTML = '<span>Error fetching data...</span>';
      })
    }).catch((e) => {
      results.innerHTML = '<span>Error fetching data...</span>';
    })
  };
})