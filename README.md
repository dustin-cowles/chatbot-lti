# Overview

This is a simple AI-powered chatbot that allows users to ask questions relating to LMS content.

# Configuration

Flask configuration is stored in [flask_config.json](web/config/flask_config.json)
OpenAPI configuration is stored in [openai_config.json](web/config/openai_config.json)
LTI Application configuration is stored in [lti_config.json](web/config/lti_config.json)
LTI Provider configuration is stored in [provider_config.json](web/well-known/provider_config.json)

# Repo Layout

[web/config/](web/config/) -  Config files for application components.
[web/static/](web/static/) - Static files (icon, css, and js).
[web/templates/](web/templates/) - HTML template files.
[web/well-known](web/well-known) - This is where well-known configuration files are served from.

[web/main.py](web/main.py) - The Flask application and routes.
[web/lib/](web/lib/) - Support modules for the application.
[web/backends/](web/backends/) - Implementation of backend connections e.g. OpenAI.
[web/setup.py](web/setup.py) - Packaging configuration.
