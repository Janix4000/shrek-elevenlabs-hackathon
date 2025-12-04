#!/usr/bin/env python3
"""
Format email communication history from charge metadata.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


def format_email_history(metadata):
    """Format email history from metadata into readable text"""

    emails = []

    # Welcome email
    if metadata.get('email_welcome_sent'):
        date = datetime.fromisoformat(metadata['email_welcome_sent']).strftime('%Y-%m-%d')
        status = "sent and opened" if metadata.get('email_welcome_opened') == 'true' else "sent"
        emails.append(f"{date} - Welcome Email {status}")

    # Renewal reminder
    if metadata.get('email_renewal_reminder_sent'):
        date = datetime.fromisoformat(metadata['email_renewal_reminder_sent']).strftime('%Y-%m-%d')
        status = "sent and opened" if metadata.get('email_renewal_reminder_opened') == 'true' else "sent"
        emails.append(f"{date} - Renewal reminder {status}")

    # Final reminder
    if metadata.get('email_final_reminder_sent'):
        date = datetime.fromisoformat(metadata['email_final_reminder_sent']).strftime('%Y-%m-%d')
        status = "sent and opened" if metadata.get('email_final_reminder_opened') == 'true' else "sent"
        amount = metadata.get('email_final_reminder_amount', '')
        amount_text = f" ({amount})" if amount else ""
        emails.append(f"{date} - Final billing reminder{amount_text} {status}")

    # Invoice
    if metadata.get('email_invoice_sent'):
        date = datetime.fromisoformat(metadata['email_invoice_sent']).strftime('%Y-%m-%d')
        status = "sent and opened" if metadata.get('email_invoice_opened') == 'true' else "sent"
        emails.append(f"{date} - Invoice & receipt {status}")

    # Build the formatted text
    output = "=== EMAIL COMMUNICATION HISTORY ===\n"
    output += "\n".join(emails)

    # Add support contact note
    contacted_support = metadata.get('customer_contacted_support', 'false')
    if contacted_support == 'false':
        output += "\nCustomer opened billing reminders but never contacted support about cancellation."
    else:
        output += "\nCustomer contacted support regarding cancellation."

    return output


def main():
    if len(sys.argv) < 2:
        print("\n📧 EMAIL HISTORY FORMATTER")
        print("="*80)
        print("\nUsage:")
        print("  venv/bin/python scripts/format_email_history.py ch_XXXXX")
        print("\nExample:")
        print("  venv/bin/python scripts/format_email_history.py ch_3SaQFuAITa6PCFHj0dnBlMJP")
        print()
        return 1

    charge_id = sys.argv[1]

    if not charge_id.startswith("ch_"):
        print("Error: Charge ID must start with 'ch_'")
        return 1

    client = StripeClient()
    charge = client.get_charge(charge_id)

    if not charge.metadata:
        print("Error: No metadata found for this charge")
        return 1

    print("\n" + "="*80)
    print(f"EMAIL HISTORY FOR CHARGE: {charge_id}")
    print("="*80 + "\n")

    formatted_history = format_email_history(charge.metadata)
    print(formatted_history)

    print("\n" + "="*80 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
