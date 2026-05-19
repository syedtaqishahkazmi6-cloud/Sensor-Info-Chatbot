# SensorLab HCI Pro

A Streamlit-based sensor exploration interface that turns local sensor specification files into an interactive chat-like user experience.

## Overview

`SensorLab HCI Pro` is a desktop web app for searching and browsing sensor descriptions stored in the project database. It includes:

- A polished Streamlit user interface with a cyber-styled theme engine
- Fuzzy search across sensor names, categories, and description content
- Sensor preview and full-detail display modes
- Support for sensor text metadata and optional sensor images
- Persistent session state for chat history, theming, and quick actions

## Project Structure

- `app.py` - main Streamlit application
- `requirements.txt` - Python dependencies
- `database/text_data/` - sensor description text files
- `database/image_data/` - optional sensor images referenced by filename

## Prerequisites

- Python 3.10+ (or compatible version)
- Windows, macOS, or Linux
- A virtual environment is recommended

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the App

From the project root directory:

```powershell
streamlit run app.py
```

Then open the URL shown in the terminal, usually `http://localhost:8501`.

## Usage

- Type a sensor name, ID, category, or keyword in the chat input.
- Available commands include `help`, `list sensors`, `what can you do`, and greetings such as `hi`.
- When a sensor match is found, the app will show a preview and offer full details on request.
- Use the sidebar to change themes, select custom accent/text colors, reset the session, and show the sensor list.

## Data Format

Sensor entries are stored as plain `.txt` files in `database/text_data/`. Each file should include human-readable fields such as `Sensor Name:`, `Category:`, and additional description lines.

Optional images can be added to `database/image_data/` using the same base filename as the text file.

## Customization

- Add new sensor text files under `database/text_data/`.
- Add matching sensor images under `database/image_data/` using the same file key.
- Adjust theme colors or add new sidebar controls in `app.py`.

## Dependencies

- `streamlit==1.31.0`
- `Pillow==10.2.0`

## Notes

- The app uses fuzzy matching and keyword search to locate sensors.
- Sensor list generation is based on the files present in `database/text_data/`.
- Clearing chat or session history is handled via confirmation buttons in the interface.

## Deployment

This project is designed for Streamlit deployment. Vercel is not recommended because Streamlit requires a persistent Python server and websocket support.

### Deploy to Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. Visit https://streamlit.io/cloud and log in with GitHub.
3. Click **New app**.
4. Select your repository, branch, and set the app file path to `app.py`.
5. Click **Deploy**.

Streamlit Cloud will build the app using `requirements.txt` and give you a public URL such as `https://<your-app-name>.streamlit.app`.

### Upload to GitHub from your local machine

1. Open a terminal in the project folder:

```powershell
cd Z:\sensor_bot_project
```

2. Initialize git:

```powershell
git init
```

3. Add files:

```powershell
git add .
```

4. Commit:

```powershell
git commit -m "Initial Streamlit SensorLab deployment setup"
```

5. Create a GitHub repository in your browser.
6. Follow the instructions GitHub shows for pushing an existing repository, for example:

```powershell
git remote add origin https://github.com/<your-username>/<repo-name>.git
 git branch -M main
 git push -u origin main
```

Once the code is on GitHub, connect the repo to Streamlit Cloud and deploy.
