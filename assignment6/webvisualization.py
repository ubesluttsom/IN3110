from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from webvisualization_plots import plot_reported_cases_per_million
from webvisualization_plots import get_countries
from webvisualization_plots import get_regions
from webvisualization_plots import get_incomes

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            "countries": get_countries(),
            "regions": get_regions(),
            "incomes": get_incomes(),
        },
    )


@app.get("/plot_reported_cases_per_million.json")
async def plot_reported_cases_per_million_json(
        countries: Optional[str]=None,
        start: Optional[str]=None,
        end: Optional[str]=None
    ):
    """Return json chart from altair"""

    # Split the countries query variable into a list of strings. Disregard
    # empty strings.

    if countries:
        countries = countries.split(',')
    elif countries == '':
        countries = None

    if start == '':
        start = None
    if end == '':
        end = None

    chart = plot_reported_cases_per_million(countries=countries,
                                            start=start,
                                            end=end)
    return chart.to_dict()
           


def main():
    """Called when run as a script

    Should launch your web app
    """
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
