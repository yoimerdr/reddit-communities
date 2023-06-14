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
});