var graphZoomEnabled = true
function graphZoom() {
  $("#image-graph").elevateZoom({
    lensSize: 300,
    zoomType: "lens",
    scrollZoom: true,
    lensShape: "round",
    zoomEnabled: graphZoomEnabled
  })
}
function addZoomToGraph(enabled=true) {
  graphZoomEnabled = enabled
  const image = document.getElementById("graph").querySelector("img");
  image.setAttribute("data-zoom-image", image.src);
  image.id = "image-graph"
  graphZoom()
}

window.addEventListener('DOMContentLoaded', function() {
  let numberInput = document.getElementById('number');
  let submitBtn = document.getElementById("form-submit")
  function validateNumberInout() {
    let number = parseInt(numberInput.value);

    if(number > 5000) {
      numberInput.value = 5000
      submitBtn.disabled = false;
    }
    else submitBtn.disabled = number < 50 || isNaN(number);
  }
  numberInput.addEventListener('keyup', validateNumberInout);
  numberInput.addEventListener("input", validateNumberInout);
  let zoomElement = document.getElementById("zoom");
  zoomElement.addEventListener("change", () => {
    graphZoomEnabled = zoomElement.value === "use";
    console.log(graphZoomEnabled)
    graphZoom()
    console.log(zoomElement)
  })
});


