# Geopulse: Multi-Location Land Use Land Cover (LULC) Analysis Tool

## Overview

Geopulse is a comprehensive web application designed for analyzing Land Use and Land Cover (LULC) changes across various locations, both within India and internationally. It leverages Google's Dynamic World dataset and is built with a modern tech stack for efficient data processing and interactive visualization.

This application allows users to explore LULC changes over time, visualize land cover maps, analyze trends, and detect changes between different land cover classes. Its architecture is optimized for serverless deployment on Vercel, making it scalable and easy to maintain.

## Features

-   **Multi-Location Support**: Analyze LULC for various locations by searching for them.
-   **Dynamic World Data**: Utilizes Google's Dynamic World dataset for accurate and up-to-date land cover information.
-   **Interactive Visualizations**: View annual land cover maps, trends, and statistics.
-   **Change Detection**: Identify and visualize changes between specific land cover classes over a period.
-   **Serverless Architecture**: Python backend deployed as serverless functions on Vercel, consuming data from HuggingFace.
-   **Modern Frontend**: Built with React, Vite, and designed for a smooth user experience.

## Currently Supported Locations

As of now, Geopulse supports Land Use Land Cover analysis for the following Indian states:

*   **Uttar Pradesh** (`up`)
*   **Maharashtra** (`mh`)
*   **West Bengal** (`wb`)

Analysis for other locations (both within India and internationally) requires sourcing and hosting the corresponding raster data, and potentially extending the geocoding logic. Please refer to the "Adding New Locations" section for more details.

## Technologies Used

**Frontend:**

*   **React**: A JavaScript library for building user interfaces.
*   **Vite**: A fast build tool for modern web projects.
*   **GSAP (GreenSock Animation Platform)**: (Planned for future UI enhancements) Robust JavaScript animation library.
*   **Framer Motion**: (Planned for future UI enhancements) A production-ready motion library for React.
*   **Luicide**: (Note: This library was not found on npm. If it's a custom or private library, please ensure its availability or provide details.)

**Backend:**

*   **Python**: For data processing and analysis.
*   **Vercel Serverless Functions**: To host the Python backend logic.
*   **Rasterio**: For reading and writing raster data.
*   **Shapely**: For geometric operations.
*   **Pandas**: For data manipulation.
*   **NumPy**: For numerical operations.
*   **Requests**: For making HTTP requests (e.g., to Nominatim and HuggingFace).
*   **Scikit-image**: For image resizing.

**Data:**

*   **Google Dynamic World Dataset**: Primary source for LULC data.
*   **HuggingFace Datasets**: Used for hosting and serving processed raster data.
*   **Nominatim (OpenStreetMap)**: For geocoding and location search.

## Local Development

To run Geopulse on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/SamparkBhol/GeoPulse.git # Replace with your actual repo URL
cd GeoPulse
```

### 2. Backend Setup (Python Serverless Functions)

Navigate to the `api` directory:

```bash
cd api
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

**Note:** To test the serverless functions locally, you'll need the Vercel CLI. Install it globally:

```bash
npm install -g vercel
```

Then, from the root of your `GeoPulse` project (not inside `api` or `frontend`):

```bash
vercel dev
```

This command will start a local development server that emulates the Vercel environment, serving both your frontend and backend API routes.

### 3. Frontend Setup (React)

Open a **new** terminal and navigate to the `frontend` directory:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Your frontend application will typically be accessible at `http://localhost:5173` (or another available port). It will automatically proxy API requests to the `vercel dev` server running in your other terminal.

## Deployment to Vercel

Geopulse is designed for seamless deployment on [Vercel](https://vercel.com/).

1.  **Push to Git Repository**: Ensure your entire `GeoPulse` project (including the `api` and `frontend` directories, and the `vercel.json` file) is pushed to a Git repository (e.g., GitHub, GitLab, Bitbucket).

2.  **Import Project in Vercel**: Log in to your Vercel account and import your Git repository as a new project. Vercel will automatically detect the `vercel.json` configuration.

3.  **Configure Environment Variables (if any)**: If you introduce any sensitive information (e.g., API keys for external services) or configurable URLs, add them as Environment Variables in your Vercel project settings.

4.  **Deploy**: Vercel will automatically build and deploy your application based on the `vercel.json` configuration. The frontend will be served as a static site, and the Python backend will be deployed as serverless functions.

## Adding New Locations (States/Countries)

To expand Geopulse's coverage to new locations, you need to consider two main aspects:

1.  **Raster Data Sourcing and Hosting**: The application relies on pre-processed raster data. For any new location, you must:
    *   Source the relevant LULC data (e.g., from Google Dynamic World or other sources).
    *   Process this data into `.tif` files following a consistent naming convention (e.g., `dw_{location_code}_{year}.tif`).
    *   Upload these `.tif` files to a publicly accessible data hosting platform, such as [HuggingFace Datasets](https://huggingface.co/datasets). The `api/hf_raster_utils.py` file currently points to `https://huggingface.co/datasets/Project 67/IndiaYearlyDynamicWorld/`. You might need to:
        *   Create new datasets on HuggingFace for different regions (e.g., `GlobalDynamicWorld`, `USADynamicWorld`).
        *   Modify the `base_url` logic in `api/hf_raster_utils.py` to dynamically select the correct dataset URL based on the location being analyzed (e.g., using the `state_code` or `country_code`).

2.  **Geocoding Integration**: The `api/geocoding.py` file uses Nominatim to search for locations. When adding new regions, ensure that:
    *   Nominatim can accurately resolve the locations you intend to support.
    *   The `detect_state_from_nominatim_result` function in `api/geocoding.py` can correctly extract a `state_code` or `country_code` that maps to your hosted raster data. You might need to extend its logic to handle new country/state names and their corresponding codes.

## Author

Project 67
