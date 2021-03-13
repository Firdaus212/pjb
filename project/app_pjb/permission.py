from flask import render_template
from flask_principal import Permission, RoleNeed
from functools import wraps
#Define related roles
admin="admin"
admin_permission=Permission(RoleNeed(admin))
def admin_authority(function):
  @wraps(function)
  def decorated_view(* args, ** kwargs):
    if admin_permission.can():
      return function(* args, ** kwargs)
    else:
      return render_template('403.html', data=None)
  return decorated_view