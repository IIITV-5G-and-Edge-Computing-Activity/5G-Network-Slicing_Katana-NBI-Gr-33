""" Katana North-Bound Interface - Implemented with Flask"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'katana')))

# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from katana.api.ems import EmsView
from katana.api.function import FunctionView
from katana.api.gst import GstView
from katana.api.nfvo import NFVOView
from katana.api.nslist import NslistView
from katana.api.policy import PolicyView
from katana.api.resource import ResourcesView
from katana.api.slice import SliceView
from katana.api.slice_des import Base_slice_desView
from katana.api.vim import VimView
from katana.api.wim import WimView
from katana.api.bootstrap import BootstrapView
from katana.api.locations import LocationView
from katana.api.alerts import AlertView


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    # Ensure instance folder exists
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
    os.makedirs(instance_path, exist_ok=True)
    
    app = Flask(__name__, 
                instance_path=instance_path,
                instance_relative_config=True)

    # Enable CORS for the app
    CORS(app)

    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    # Register views
    views = [
        VimView, WimView, EmsView, NFVOView, 
        SliceView, FunctionView, Base_slice_desView,
        GstView, ResourcesView, PolicyView, NslistView,
        BootstrapView, LocationView, AlertView
    ]
    
    for view in views:
        view.register(app, trailing_slash=False)

    return app

# For local development
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)
