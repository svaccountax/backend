
from flask import Blueprint, session, redirect, render_template, request
from functools import wraps
from db import get_db_connection

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/admin/callbacks")
@admin_required
def admin_callbacks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, phone, email, created_at, status
        FROM callback_requests
        ORDER BY created_at DESC
    """)
    callbacks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin_callbacks.html", callbacks=callbacks)


@admin_bp.route("/admin/callbacks/update/<int:id>", methods=["POST"])
@admin_required
def update_callback_status(id):
    status = request.form.get("status")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE callback_requests
        SET status = %s
        WHERE id = %s
    """, (status, id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/admin/callbacks")


@admin_bp.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/")
