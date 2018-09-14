const dropdown = document.querySelector('.dropdown');
const sublist = document.querySelector('.Header-navSublist');

dropdown.addEventListener('click', function (event) {
  event.preventDefault();
  sublist.classList.toggle('is-visible');
});

dropdown.addEventListener('mouseenter', function (event) {
  event.preventDefault();
  sublist.classList.add('is-visible');
});

dropdown.addEventListener('mouseleave', function (event) {
  event.preventDefault();
  sublist.classList.remove('is-visible');
});