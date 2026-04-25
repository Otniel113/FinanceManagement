document.addEventListener('DOMContentLoaded', function () {
    const currencyInputs = document.querySelectorAll('.format-currency');
    const fullForm = document.getElementById('full-mode-form');

    // Format numbers with commas
    function formatNumber(val) {
        let numericValue = val.replace(/\D/g, "");
        if (numericValue) {
            return parseInt(numericValue, 10).toLocaleString('en-US');
        }
        return "";
    }

    // Apply formatting on input
    currencyInputs.forEach(input => {
        // Format initial value if present
        if (input.value) {
            input.value = formatNumber(input.value);
        }

        input.addEventListener('input', function (e) {
            e.target.value = formatNumber(e.target.value);
        });
    });

    // Remove commas before submit
    if (fullForm) {
        fullForm.addEventListener('submit', function () {
            currencyInputs.forEach(input => {
                input.value = input.value.replace(/,/g, "");
            });
        });
    }
});