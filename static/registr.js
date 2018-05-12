document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#submit').disabled = true;
  document.querySelector('#cPassword1').onkeyup = proverka;
  document.querySelector('#Password1').onkeyup = proverka;

  function proverka() {
    if (document.querySelector('#cPassword1').value === document.querySelector('#Password1').value && document.querySelector('#Password1').value){
      document.querySelector('#err1').innerHTML = "";
      document.querySelector('#err2').innerHTML = "";

      document.querySelector('#Password1').classList.remove('is-invalid');
      document.querySelector('#cPassword1').classList.remove('is-invalid');

      document.querySelector('#submit').disabled = false;
    }
    else{
      document.querySelector('#err1').innerHTML = "Пароли не совпадают"
      document.querySelector('#err2').innerHTML = "Пароли не совпадают"

      document.querySelector('#Password1').classList.add('is-invalid');
      document.querySelector('#cPassword1').classList.add('is-invalid');

      document.querySelector('#submit').disabled = true;
    }
  }

  document.querySelector('#login').onkeyup = () => {
    if (document.querySelector('#login').value){
      document.querySelector('#submit').disabled = false;
    }
    else{
      document.querySelector('#submit').disabled = true;
    }
  };

});
