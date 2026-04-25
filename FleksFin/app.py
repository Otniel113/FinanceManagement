from decimal import Decimal
from typing import Dict, List, Optional

from flask import Flask, render_template, request
from utils.input_validator import validate_full_mode, validate_simple_mode

app = Flask(__name__)

# Dummy threshold for the UI prototype.
# Replace this value later with the actual industry average or ML model output.
INDUSTRY_AVERAGE_CRO = Decimal("0.12")


def decimal_to_display(value: Decimal, places: int = 4) -> str:
    """Format a Decimal value for display without converting through float."""
    quantizer = Decimal("1").scaleb(-places)
    return str(value.quantize(quantizer))


def build_result(cro: Decimal) -> Dict[str, str]:
    """Build the prediction result payload consumed by the view."""
    is_flexible = cro >= INDUSTRY_AVERAGE_CRO

    if is_flexible:
        return {
            "cro": decimal_to_display(cro),
            "ffr": "1 - Fleksibel",
            "title": "Perusahaan terindikasi fleksibel secara finansial",
            "description": (
                "CRO berada di atas rata-rata industri dummy, sehingga perusahaan "
                "memiliki bantalan kas yang relatif lebih kuat."
            ),
            "badge_class": "text-bg-success",
            "box_class": "result-flexible",
        }

    return {
        "cro": decimal_to_display(cro),
        "ffr": "0 - Tidak Fleksibel",
        "title": "Perusahaan terindikasi belum fleksibel secara finansial",
        "description": (
            "CRO berada pada atau di bawah rata-rata industri dummy, sehingga "
            "ketahanan likuiditas perlu dievaluasi lebih lanjut."
        ),
        "badge_class": "text-bg-danger",
        "box_class": "result-not-flexible",
    }


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    errors: List[str] = []
    result: Optional[Dict[str, str]] = None
    active_tab = "full"
    form_values: Dict[str, str] = {}

    if request.method == "POST":
        mode = request.form.get("mode", "full")
        active_tab = "simple" if mode == "simple" else "full"
        form_values = request.form.to_dict(flat=True)

        if active_tab == "simple":
            errors, cro = validate_simple_mode(request.form)
        else:
            errors, cro = validate_full_mode(request.form)

        if not errors and cro is not None:
            result = build_result(cro)

    return render_template(
        "index.html",
        active_tab=active_tab,
        errors=errors,
        form_values=form_values,
        industry_average=decimal_to_display(INDUSTRY_AVERAGE_CRO),
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
