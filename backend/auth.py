from models import db, User
import bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, request, jsonify