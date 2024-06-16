document.addEventListener('DOMContentLoaded', function() {
    var morningRadio = document.getElementById('morning');
    var afternoonRadio = document.getElementById('afternoon');

    morningRadio.addEventListener('change', function() {
        if (morningRadio.checked) {
            document.getElementById('cost').textContent = '新台幣 2000 元';
        }
    });

    afternoonRadio.addEventListener('change', function() {
        if (afternoonRadio.checked) {
            document.getElementById('cost').textContent = '新台幣 2500 元';
        }
    });
});