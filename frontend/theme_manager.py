# theme_manager.py

import panel as pn
from pathlib import Path

class ThemeManager:
    _instance = None
    _config_file = Path.home() / '.crp_theme_config.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.current_theme = 'dark'
        self._apply_theme()
        
    def _apply_theme(self):
        pn.state.theme = 'dark'
            
        custom_css = """
        :root {
            --background-color: #f3f4f6; /* Light grey */
            --text-color: #1f2937; /* Dark grey */
            --accent-color: #e11d48; /* Red-pink */
        }

        body {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        .panel-widget-box {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        .panel-input {
            background-color: #ffffff !important; /* White inputs */
            color: var(--text-color) !important;
        }

        .panel-button {
            background-color: var(--accent-color) !important;
            color: #ffffff !important;
        }

        .panel-button:hover {
            background-color: #f43f5e !important; /* Lighter red-pink */
            color: #ffffff !important;
        }

        .panel-tabs {
            background-color: #e5e7eb !important; /* Light grey tabs */
        }

        .panel-tab {
            color: var(--text-color) !important;
        }

        .panel-tab.active {
            background-color: var(--accent-color) !important;
            color: #ffffff !important;
        }

        .panel-widget-box * {
            color: var(--text-color) !important;
        }

        .panel-input input,
        .panel-select select,
        .panel-textarea textarea {
            color: var(--text-color) !important;
        }

        .app-header {
            background-color: #ffffff;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid var(--accent-color);
            color: var(--text-color);
        }
        """
        
        # Add the custom CSS to Panel
        pn.config.raw_css.append(custom_css)
        
        # Clear Panel's cache to refresh components
        if hasattr(pn.state, 'cache'):
            pn.state.cache.clear()

    def get_theme(self):
        """Get current theme"""
        return self.current_theme

    def create_logo(self, logo_url, width=200, height=None):
        """Create a logo widget from a URL
        
        Args:
            logo_url (str): URL of the logo image
            width (int): Width of the logo in pixels
            height (int, optional): Height of the logo in pixels. If None, maintains aspect ratio.
            
        Returns:
            panel.pane.HTML: A Panel HTML widget containing the logo
        """
        height_style = f"height: {height}px;" if height else "height: auto;"
        logo_html = f"""
        <div style="text-align: center; margin: 10px 0;">
            <img src="{logo_url}" 
                 style="width: {width}px; {height_style} max-width: 100%;" 
                 alt="Logo">
        </div>
        """
        return pn.pane.HTML(logo_html)

    def create_header(self):
        """Create a header with the logo"""
        header_html = """
        <div class="app-header">
            <img src="https://i.imgur.com/nuFPYE7.png" alt="Logo">
        </div>
        """
        return pn.pane.HTML(header_html)

theme_manager = ThemeManager() 