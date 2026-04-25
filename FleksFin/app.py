from decimal import Decimal
from typing import Dict, List, Optional

from flask import Flask, render_template, request
from utils.input_validator import validate_full_mode, validate_simple_mode
from controllers.predict_ffr import build_result, INDUSTRY_AVERAGE_CRO, decimal_to_display

app = Flask(__name__)


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
