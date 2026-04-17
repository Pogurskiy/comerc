document.addEventListener('DOMContentLoaded', function () {
    // Quantity increment/decrement buttons
    document.querySelectorAll('.qty-input').forEach(function (wrapper) {
        var minusBtn = wrapper.querySelector('.qty-minus');
        var plusBtn = wrapper.querySelector('.qty-plus');
        var input = wrapper.querySelector('.qty-field');

        if (minusBtn && input) {
            minusBtn.addEventListener('click', function () {
                var val = parseInt(input.value, 10) || 1;
                var min = parseInt(input.min, 10) || 1;
                if (val > min) {
                    input.value = val - 1;
                }
            });
        }
        if (plusBtn && input) {
            plusBtn.addEventListener('click', function () {
                var val = parseInt(input.value, 10) || 1;
                var max = input.max ? parseInt(input.max, 10) : 9999;
                if (val < max) {
                    input.value = val + 1;
                }
            });
        }
    });

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
});
