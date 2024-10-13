document.addEventListener('DOMContentLoaded', () => {
  const ary_th = document.querySelectorAll('.list th');
  for (const th of ary_th) {
    th.className = 'text-center p-1'
  }
});