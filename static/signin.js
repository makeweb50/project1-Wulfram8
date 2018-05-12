document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#submit').disabled = true;
  document.querySelector('#login').onkeyup = check;
  document.querySelector('#password').onkeyup = check;

  function check() {
    if (document.querySelector('#login').value && document.querySelector('#password').value) {
      document.querySelector('#submit').disabled = false;
    }
    else{
      document.querySelector('#submit').disabled = true;
    }
  }
});
