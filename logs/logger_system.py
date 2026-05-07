import os
import datetime

class TeamLogger:
    def __init__(self, filename="index.html"):
        # This saves the index.html one folder UP from /logs, into the main directory
        self.filename = os.path.join(os.path.dirname(__file__), "..", filename)
        self._initialize_html()

    def _initialize_html(self):
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
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        badge_color = "#2ecc71" 
        if level.upper() == "ERROR": badge_color = "#e74c3c"
        if level.upper() == "WARNING": badge_color = "#f1c40f"

        entry = f"""
                <tr>
                    <td>{now}</td>
                    <td><kbd>{component}</kbd></td>
                    <td style="color:{badge_color}"><strong>{level}</strong></td>
                    <td>{message}</td>
                </tr>"""
        with open(self.filename, "a") as f:
            f.write(entry)

if __name__ == "__main__":
    my_logger = TeamLogger()
    my_logger.log("API", "INFO", "Logging system initialized")
    my_logger.log("Network", "WARNING", "High latency detected in hub simulation")
