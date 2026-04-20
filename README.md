# uwa-unireview
Web application for browsing, submitting, and discussing honest reviews of UWA units before you enrol.

## Team
| UWA ID | Full Name | GitHub Username | Role |
|----------|------------|-----------------|---------------------|
| 24667496 | Nidhi Sorathiya | @nisorathiya | Team Lead/Full-stack developer |
| 24500079 | Nevis Herlangga | @nxherl | Documentation/Backend developer |
| 24726135 | Md Mahabub Islam | @ProgMahabub21 | Backend developer |
| 25167515 | Xingyan Guo | @laomeile | Frontend developer |

## How to Run the Application

### 1. Clone the repository
```bash
git clone https://github.com/nisorathiya/uwa-unireview.git
cd uwa-unireview
```

### 2. Create and activate a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python run.py
```

Open **http://localhost:5000** in your browser.

### Important notes
- Always activate the virtual environment before running the app
- You will see `(venv)` at the start of your terminal line when it is active
- Never commit the `venv/` folder — it is already in `.gitignore`
- Run `git pull` before starting work each day to get the latest changes from teammates

