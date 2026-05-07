import os
import datetime

class TeamLogger:
    def __init__(self, filename="index.html"):
        self.filename = filename
        self._initialize_html()

    def _initialize_html(self):
        """Creates the website structure if it doesn't exist."""
        if not os.path.exists(self.filename):
            header = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/picocss@1/css/pico.min.css">
    <title>Group Project Logs</title>
</head>
<body>
    <main class="container">
        <hgroup>
            <h1>System Activity Log</h1>
            <h2>Project Status Dashboard</h2>
        </hgroup>
        <table role="grid">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Component</th>
                    <th>Level</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody id="log-content">
"""
            with open(self.filename, "w") as f:
                f.write(header)

    def log(self, component, level, message):
        """Adds a new row to the log website."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simple color logic for levels
        badge_color = "#2ecc71" # Green for INFO
        if level.upper() == "ERROR": badge_color = "#e74c3c" # Red
        if level.upper() == "WARNING": badge_color = "#f1c40f" # Yellow

        entry = f"""
                <tr>
                    <td>{now}</td>
                    <td><kbd>{component}</kbd></td>
                    <td style="color:{badge_color}"><strong>{level}</strong></td>
                    <td>{message}</td>
                </tr>"""
        
        with open(self.filename, "a") as f:
            f.write(entry)

# --- TEST THE LOGGER ---
if __name__ == "__main__":
    my_logger = TeamLogger()
    my_logger.log("API", "INFO", "Server started successfully")
    my_logger.log("Database", "ERROR", "Connection timeout on port 5432")
