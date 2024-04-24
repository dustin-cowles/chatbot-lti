# Overview

This is a simple AI-powered chatbot that allows users to ask questions relating to LMS content.

# DISCLAIMER
This is a hack week project completed in order to learn more about the Open AI API and exposed models.
This is in no way production ready but may serve as a resource for learning how one might go about creating an Open API backed application.
It has only been tested with Canvas, but should work with any LTI 1.3 compliant LMS.

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
