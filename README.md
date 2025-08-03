# Covid19-Interactive-Dashboard
An interactive web dashboard built with Python and Plotly Dash to visualize global COVID-19 statistics. The application fetches live data from the disease.sh public API.

## Features

-   **Live Global Stats:** Displays up-to-date worldwide totals for confirmed cases, deaths, and recoveries in summary cards.
-   **Interactive World Map:** A choropleth map visualizes the distribution of confirmed cases by country. You can hover over countries to see their specific data.
-   **Historical Data Trend:** A line chart shows the historical trend of global confirmed cases over time.
-   **Responsive Layout:** The dashboard is designed to be usable on different screen sizes.
-   **Live API Data:** All data is fetched in real-time from a reliable public API, so no static data files are needed.

## Technology Stack

-   **Python**
-   **Plotly Dash:** The core framework for building the interactive web application.
-   **Pandas:** For data manipulation and processing.
-   **Requests:** To fetch data from the API.

## Setup and Usage

A virtual environment is recommended for this project.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Anjali-Ajesh/covid-19-dashboard.git](https://github.com/Anjali-Ajesh/covid-19-dashboard.git)
    cd covid-19-dashboard
    ```

2.  **Install Dependencies:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install the required libraries
    pip install dash pandas requests
    ```

3.  **Run the Dashboard:**
    Execute the Python script from your terminal.
    ```bash
    python covid_dashboard.py
    ```
    The application will start a local web server. Open your browser and navigate to the URL shown in the terminal (usually `http://127.0.0.1:8050/`) to view the dashboard.
