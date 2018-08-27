document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#star1').onclick = star1;
    document.querySelector('#star2').onclick = star2;
    document.querySelector('#star3').onclick = star3;
    document.querySelector('#star4').onclick = star4;
    document.querySelector('#star5').onclick = star5;

  function star1() {
    document.querySelector('#star2').classList.add('starw');
    document.querySelector('#star2').classList.remove('stara');
    document.querySelector('#star3').classList.add('starw');
    document.querySelector('#star3').classList.remove('stara');
    document.querySelector('#star4').classList.add('starw');
    document.querySelector('#star4').classList.remove('stara');
    document.querySelector('#star5').classList.add('starw');
    document.querySelector('#star5').classList.remove('stara');

    document.querySelector("#r1").checked=true;
  }

  function star2() {
    document.querySelector('#star2').classList.add('stara');
    document.querySelector('#star2').classList.remove('starw');

    document.querySelector('#star3').classList.add('starw');
    document.querySelector('#star3').classList.remove('stara');
    document.querySelector('#star4').classList.add('starw');
    document.querySelector('#star4').classList.remove('stara');
    document.querySelector('#star5').classList.add('starw');
    document.querySelector('#star5').classList.remove('stara');

    document.querySelector("#r2").checked=true;
  }

  function star3() {
    document.querySelector('#star2').classList.add('stara');
    document.querySelector('#star2').classList.remove('starw');
    document.querySelector('#star3').classList.add('stara');
    document.querySelector('#star3').classList.remove('starw');

    document.querySelector('#star4').classList.add('starw');
    document.querySelector('#star4').classList.remove('stara');
    document.querySelector('#star5').classList.add('starw');
    document.querySelector('#star5').classList.remove('stara');

    document.querySelector("#r3").checked=true;
  }

  function star4() {
    document.querySelector('#star2').classList.add('stara');
    document.querySelector('#star2').classList.remove('starw');
    document.querySelector('#star3').classList.add('stara');
    document.querySelector('#star3').classList.remove('starw');
    document.querySelector('#star4').classList.add('stara');
    document.querySelector('#star4').classList.remove('starw');

    document.querySelector('#star5').classList.add('starw');
    document.querySelector('#star5').classList.remove('stara');

    document.querySelector("#r4").checked=true;
  }

  function star5() {
    document.querySelector('#star2').classList.add('stara');
    document.querySelector('#star2').classList.remove('starw');
    document.querySelector('#star3').classList.add('stara');
    document.querySelector('#star3').classList.remove('starw');
    document.querySelector('#star4').classList.add('stara');
    document.querySelector('#star4').classList.remove('starw');
    document.querySelector('#star5').classList.add('stara');
    document.querySelector('#star5').classList.remove('starw');
    document.querySelector("#r5").checked=true;
  }
});
