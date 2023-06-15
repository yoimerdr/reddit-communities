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

function manageHideElement(id, hideClass = "hide") {
  const element = document.getElementById(id);
  if(element.classList.contains(hideClass))
    element.classList.remove(hideClass)
  else element.classList.add(hideClass)
}

async function generate()  {
  manageHideElement("graph")
  manageHideElement("graph-spinner")
  manageHideElement("communities-div")
  const run = pyscript.interpreter.globals.get('run');
  await run()
  manageHideElement("graph-spinner")
  manageHideElement("graph")
  manageHideElement("communities-div")
}

function addCommunities(colors, communities_proxy) {
  const div = document.getElementById("communities");
  div.innerHTML = "";
  let index = 1;

  let communities = []

  for(let item of communities_proxy) {
    let com = []
    for(let community of item)
      com.push(community)
    communities.push(com)
  }

  function getCommunities(i, color="white") {
    if(i > communities.length || i < 0)
      return ""
    let listItems = communities[i].map(item => `<li>${item}</li>`).join("\n");
    let grid = ""
    if (communities[i].length >= 35)
      grid = "display: grid; grid-template-columns: 1fr 1fr 1fr"
    return `<ul style="color: ${color}; list-style-type: none; padding: 2px; ${grid}">${listItems}</ul>`
  }
  for(let color of colors) {
    const community = document.createElement("div")
    community.innerHTML = "Community " + index
    community.style.color = color
    community.id = "community-" + index
    div.appendChild(community)

    new jBox("Tooltip",{
        attach: "#" + community.id,
        theme: "TooltipDark",
        position: {
            x: "right",
            y: "center"
        },
        outside: "x",
        pointer: "top:15",
        content: getCommunities(index - 1),
        animation: "move",
        adjustDistance: {
            top: 55,
            right: 5,
            bottom: 5,
            left: 5
        },
        zIndex: 4e3
    })
    index++
  }
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


