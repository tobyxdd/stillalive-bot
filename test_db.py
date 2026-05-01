import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

import db


class DbDuressPinTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.original_db_path = db.DB_PATH
        db.DB_PATH = self.tmp.name
        db.init_db()
        db.upsert_user(1, "owner")

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        os.unlink(self.tmp.name)

    def set_last_checkin(self, when: datetime, **fields):
        with db.get_db() as conn:
            sets = ["last_checkin = ?", "alerted = 0"]
            values = [when]
            for key, value in fields.items():
                sets.append(f"{key} = ?")
                values.append(value)
            values.append(1)
            conn.execute(
                f"UPDATE users SET {', '.join(sets)} WHERE user_id = ?", values
            )

    def test_migration_creates_duress_pin_columns(self):
        with db.get_db() as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            columns = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(users)").fetchall()
            }

        self.assertEqual(version, len(db.MIGRATIONS))
        self.assertIn("duress_pin_hash", columns)
        self.assertIn("duress_active_at", columns)

    def test_duress_pin_is_distinct_from_regular_pin(self):
        db.set_pin(1, "1234")
        db.set_duress_pin(1, "9876")

        self.assertTrue(db.verify_pin(1, "1234"))
        self.assertFalse(db.verify_pin(1, "9876"))
        self.assertTrue(db.verify_duress_pin(1, "9876"))
        self.assertFalse(db.verify_duress_pin(1, "0000"))

    def test_duress_checkin_does_not_move_last_checkin_but_suppresses_reminders(self):
        last_checkin = datetime.now(timezone.utc) - timedelta(hours=1)
        self.set_last_checkin(last_checkin, deadline_hours=48)
        before = db.get_user(1)["last_checkin"]

        db.mark_duress_checkin(1)
        db.log_checkin(1, False, "pin", "duress")

        user = db.get_user(1)
        self.assertEqual(user["last_checkin"], before)
        self.assertIsNotNone(user["duress_active_at"])
        self.assertTrue(db.is_duress_suppressed(1))
        self.assertEqual(db.get_checkin_stats()["duress"], 1)

    def test_deadline_alerts_still_select_duress_suppressed_user(self):
        nearing_deadline = datetime.now(timezone.utc) - timedelta(hours=47)
        self.set_last_checkin(
            nearing_deadline,
            deadline_hours=48,
            reminder_before=6,
        )
        db.mark_duress_checkin(1)

        self.assertEqual(db.get_users_needing_deadline_reminder(), [])

        past_deadline = datetime.now(timezone.utc) - timedelta(hours=49)
        self.set_last_checkin(past_deadline, deadline_hours=48)

        self.assertEqual(
            [user["user_id"] for user in db.get_users_past_deadline()], [1]
        )
        db.mark_alerted(1)
        self.assertFalse(db.is_duress_suppressed(1))
        self.assertIsNone(db.get_user(1)["duress_active_at"])

    def test_true_checkin_and_clear_pin_clear_duress_state(self):
        db.set_pin(1, "1234")
        db.set_duress_pin(1, "9876")
        self.set_last_checkin(datetime.now(timezone.utc) - timedelta(hours=1))
        db.mark_duress_checkin(1)

        db.checkin(1)

        self.assertFalse(db.is_duress_suppressed(1))
        self.assertIsNone(db.get_user(1)["duress_active_at"])
        self.assertTrue(db.verify_duress_pin(1, "9876"))

        db.clear_pin(1)

        self.assertFalse(db.verify_pin(1, "1234"))
        self.assertFalse(db.verify_duress_pin(1, "9876"))
        self.assertIsNone(db.get_user(1)["duress_active_at"])


if __name__ == "__main__":
    unittest.main()
