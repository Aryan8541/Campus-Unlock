"""
Campus Unlock — Maintenance Script: Promote Primary Administrator
===================================================================
One-time maintenance script. Does NOT touch routes, templates,
migrations, or the schema. Only updates existing row data via the
ORM.

What it does:
  1. Looks up the user with email == aryanravi@gmail.com
     -> sets role = "admin", is_admin = True
  2. Looks up the user with email == admin@campusunlock.com
     -> sets role = "student", is_admin = False
  3. Commits once. Rolls back on any failure.

Idempotent: safe to run any number of times. If an account is
already in the desired state, it is left as-is (no-op update).
If either account does not exist, a friendly message is printed
and the script continues/exits cleanly — it never crashes.

Usage:
    python scripts/promote_admin.py
"""

import os
import sys

# Add the project root (one level above /scripts) to Python's import path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from models import db, User

NEW_PRIMARY_ADMIN_EMAIL = "aryanravi@gmail.com"
SEEDED_ADMIN_EMAIL = "admin@campusunlock.com"


def promote_primary_admin():
    app = create_app()

    with app.app_context():
        try:
            changed = False

            # ----------------------------------------------------------
            # 1. Promote the real account
            # ----------------------------------------------------------
            primary_user = User.query.filter_by(
                email=NEW_PRIMARY_ADMIN_EMAIL
            ).first()

            if primary_user is None:
                print(
                    f"[SKIP] No account found with email "
                    f"'{NEW_PRIMARY_ADMIN_EMAIL}'. Nothing to promote."
                )
            else:
                if primary_user.role != "admin" or not primary_user.is_admin:
                    primary_user.role = "admin"
                    primary_user.is_admin = True
                    changed = True
                    print(
                        f"[OK] Promoted '{NEW_PRIMARY_ADMIN_EMAIL}' "
                        f"(id={primary_user.id}) to admin."
                    )
                else:
                    print(
                        f"[OK] '{NEW_PRIMARY_ADMIN_EMAIL}' "
                        f"(id={primary_user.id}) is already admin. No change needed."
                    )

            # ----------------------------------------------------------
            # 2. Demote the seeded account
            # ----------------------------------------------------------
            seeded_admin = User.query.filter_by(
                email=SEEDED_ADMIN_EMAIL
            ).first()

            if seeded_admin is None:
                print(
                    f"[SKIP] No account found with email "
                    f"'{SEEDED_ADMIN_EMAIL}'. Nothing to demote."
                )
            else:
                if seeded_admin.role != "student" or seeded_admin.is_admin:
                    seeded_admin.role = "student"
                    seeded_admin.is_admin = False
                    changed = True
                    print(
                        f"[OK] Demoted '{SEEDED_ADMIN_EMAIL}' "
                        f"(id={seeded_admin.id}) to student."
                    )
                else:
                    print(
                        f"[OK] '{SEEDED_ADMIN_EMAIL}' "
                        f"(id={seeded_admin.id}) is already a student. No change needed."
                    )

            # ----------------------------------------------------------
            # 3. Commit once
            # ----------------------------------------------------------
            if changed:
                db.session.commit()
                print("[DONE] Changes committed successfully.")
            else:
                print("[DONE] No changes were necessary. Database already up to date.")

        except Exception as exc:
            db.session.rollback()
            print(f"[ERROR] Transaction rolled back due to: {exc}")
            sys.exit(1)


if __name__ == "__main__":
    promote_primary_admin()
    sys.exit(0)
