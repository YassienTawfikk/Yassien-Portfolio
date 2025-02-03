from dash_app import app
import index
from utils import clean_cache

# Clean up cache directories
clean_cache.remove_directories()

# Main execution
if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)
