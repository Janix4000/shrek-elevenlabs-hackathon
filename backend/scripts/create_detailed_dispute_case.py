#!/usr/bin/env python3
"""
Create a detailed subscription cancellation dispute case with comprehensive evidence.

This demonstrates how to:
1. Create a subscription transaction with detailed metadata
2. Wait for the dispute to be created
3. Submit comprehensive evidence to contest the dispute
"""

import sys
import os
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stripe_integration import StripeClient


def create_detailed_subscription_case():
    """Create a comprehensive subscription cancellation dispute case"""

    print("\n" + "="*80)
    print("CREATING DETAILED SUBSCRIPTION CANCELLATION DISPUTE CASE")
    print("="*80)
    print("Scenario: Customer claims subscription was canceled but continued to be charged")
    print("Reality: Customer did NOT follow cancellation procedure and continued using service")
    print("="*80 + "\n")

    client = StripeClient()

    # Step 1: Create Customer with billing details
    print("📋 Step 1: Creating customer with complete billing details...")

    import stripe
    customer = stripe.Customer.create(
        email="disputed.subscription@example.com",
        name="Robert Disputer",
        phone="+1-555-123-4567",
        address={
            "line1": "123 Main Street",
            "line2": "Apt 4B",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
        }
    )
    print(f"   ✓ Customer created: {customer.id}")
    print(f"   ✓ Email: {customer.email}")
    print(f"   ✓ Name: {customer.name}")
    print(f"   ✓ Phone: {customer.phone}")
    print(f"   ✓ Address: {customer.address.line1}, {customer.address.city}, {customer.address.state} {customer.address.postal_code}")

    # Step 2: Create detailed subscription charge with comprehensive metadata
    print("\n💳 Step 2: Creating subscription charge with detailed metadata...")

    purchase_date = datetime.now() - timedelta(days=45)
    last_billing = datetime.now() - timedelta(days=15)

    # Essential metadata (Stripe limit: 50 keys)
    detailed_metadata = {
        # Customer & Billing
        "customer_id": customer.id,
        "customer_name": "Robert Disputer",
        "customer_email": "disputed.subscription@example.com",
        "customer_phone": "+1-555-123-4567",
        "billing_address": "123 Main Street, Apt 4B, New York, NY 10001, US",

        # Product
        "product_name": "Premium Digital Workspace",
        "product_type": "digital_subscription",
        "subscription_tier": "premium",
        "billing_cycle": "monthly",

        # Dates
        "subscription_start": purchase_date.isoformat(),
        "billing_period_start": last_billing.isoformat(),
        "billing_period_end": (last_billing + timedelta(days=30)).isoformat(),
        "purchase_ip": "192.168.1.45",

        # Service Usage (KEY EVIDENCE)
        "service_used": "true",
        "total_logins": "127",
        "logins_after_charge": "23",
        "last_login": (datetime.now() - timedelta(hours=8)).isoformat(),
        "files_uploaded": "47",
        "uploads_after_charge": "8",
        "data_stored_gb": "23.4",
        "api_calls_after_charge": "342",

        # Cancellation Status (KEY EVIDENCE)
        "cancellation_requested": "false",
        "support_contact": "none",
        "subscription_status": "active",
        "auto_renew_enabled": "true",

        # Policy Acceptance
        "policy_accepted": "true",
        "policy_accepted_date": purchase_date.isoformat(),
        "terms_version": "2.1",

        # Communication / Email History
        "email_welcome_sent": purchase_date.isoformat(),
        "email_welcome_opened": "true",
        "email_renewal_reminder_sent": (last_billing - timedelta(days=7)).isoformat(),
        "email_renewal_reminder_opened": "true",
        "email_final_reminder_sent": (last_billing - timedelta(days=3)).isoformat(),
        "email_final_reminder_opened": "true",
        "email_final_reminder_amount": "$29.99",
        "email_invoice_sent": last_billing.isoformat(),
        "email_invoice_opened": "true",
        "customer_contacted_support": "false",

        # Previous Charges
        "previous_charges": "2",
        "previous_disputes": "0",

        # Dispute Info
        "scenario": "subscription_canceled",
        "reason_code": "13.2",
        "merchant_position": "no_cancellation_request",
        "evidence_strength": "strong",
    }

    charge = client.create_charge(
        amount=2999,  # $29.99
        currency="usd",
        source="tok_createDispute",  # Will trigger dispute
        # Note: customer_id stored in metadata; Stripe customer object has full billing details
        description="Premium Digital Workspace - Monthly Subscription Renewal",
        metadata=detailed_metadata
    )

    print(f"   ✓ Charge created: {charge.id}")
    print(f"   ✓ Amount: ${charge.amount/100:.2f}")
    print(f"   ✓ Description: {charge.description}")
    print(f"   ✓ Customer linked: {customer.id} (with full billing details)")
    print(f"   ✓ Billing details: name, email, phone, complete address")
    print(f"   ✓ Metadata fields: {len(detailed_metadata)} (including billing info)")

    # Step 3: Wait for dispute
    print("\n⏳ Step 3: Waiting for dispute to be created...")
    print("   (In test mode, this usually takes 5-10 seconds)")

    dispute = None
    for i in range(15):
        time.sleep(1)
        print(f"   Checking... ({i+1}/15)", end="\r")
        disputes = client.get_charge_disputes(charge.id)
        if disputes:
            dispute = disputes[0]
            break

    print("\n")

    if not dispute:
        print("   ⚠ Dispute not created yet. Check Stripe Dashboard in a few minutes.")
        print(f"   Charge ID: {charge.id}")
        print(f"   Dashboard: https://dashboard.stripe.com/test/payments/{charge.id}")
        return None

    print(f"   ✓ Dispute created: {dispute.id}")
    print(f"   ✓ Reason: {dispute.reason}")
    print(f"   ✓ Status: {dispute.status}")
    print(f"   ✓ Amount: ${dispute.amount/100:.2f}")

    # Step 4: Prepare comprehensive evidence
    print("\n📝 Step 4: Preparing comprehensive evidence...")

    evidence = {
        # Customer Information
        "customer_email_address": "disputed.subscription@example.com",
        "customer_name": "Robert Disputer",
        "customer_purchase_ip": "192.168.1.45",
        "billing_address": "123 Main Street, Apt 4B, New York, NY 10001, USA",

        # Product Description
        "product_description": (
            "Premium Digital Workspace - Annual Subscription Plan. "
            "Includes unlimited cloud storage, real-time collaboration tools, "
            "video conferencing, project management features, and 24/7 customer support. "
            "Service is billed monthly at $29.99/month with automatic renewal."
        ),

        # Service Date
        "service_date": last_billing.strftime("%B %d, %Y"),

        # Cancellation Policy
        "cancellation_policy_disclosure": (
            "Our cancellation policy was clearly displayed during checkout and included in the "
            "Terms of Service that the customer accepted on " + purchase_date.strftime("%B %d, %Y") + ". "
            "The policy states: 'Subscriptions automatically renew each billing period. "
            "To cancel, customers must log into their account settings and click 'Cancel Subscription' "
            "OR email support@example.com at least 5 days before the next billing date. "
            "Cancellations take effect at the end of the current billing period.' "
            "The customer accepted this policy by checking the acknowledgment box and clicking 'Subscribe Now'."
        ),

        # Cancellation Rebuttal
        "cancellation_rebuttal": (
            "The customer claims they canceled their subscription, however our records show:\n\n"
            "1. NO CANCELLATION REQUEST: We have no record of any cancellation request through our "
            "account portal, email, phone, or chat support.\n\n"
            "2. CONTINUED ACTIVE USE: The customer has actively used the service AFTER the disputed charge:\n"
            "   • 23 logins since the charge date (" + last_billing.strftime("%b %d, %Y") + ")\n"
            "   • Most recent login: " + (datetime.now() - timedelta(hours=8)).strftime("%b %d, %Y at %I:%M %p") + "\n"
            "   • 8 files uploaded after the charge\n"
            "   • 342 API calls made after the charge\n"
            "   • Currently storing 23.4 GB of data\n\n"
            "3. ACKNOWLEDGMENT OF CHARGES: Customer opened billing reminder email sent 3 days before charge.\n\n"
            "4. NO PRIOR COMPLAINTS: Customer has never contacted support regarding cancellation issues.\n\n"
            "5. SUBSCRIPTION STILL ACTIVE: Customer's account remains active with auto-renew enabled.\n\n"
            "The customer's continued and extensive use of the service demonstrates they intended to "
            "maintain their subscription. This appears to be buyer's remorse or an attempt to receive "
            "service without payment, rather than a legitimate cancellation claim."
        ),

        # Access Activity Log
        "access_activity_log": (
            "=== SERVICE ACCESS LOG ===\n\n"
            "Subscription Start: " + purchase_date.strftime("%Y-%m-%d") + "\n"
            "Disputed Charge Date: " + last_billing.strftime("%Y-%m-%d") + "\n"
            "Total Account Logins: 127\n"
            "Logins After Disputed Charge: 23\n\n"
            "RECENT ACTIVITY (Last 15 Days):\n"
            + (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") + " - Login from IP 192.168.1.45 (New York, NY)\n"
            + (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M") + " - Uploaded 3 files (4.2 MB)\n"
            + (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M") + " - Login from IP 192.168.1.45\n"
            + (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M") + " - Used video conference feature (42 minutes)\n"
            + (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d %H:%M") + " - Login from IP 192.168.1.45\n"
            + (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M") + " - Edited 7 documents\n"
            + (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M") + " - Login from IP 192.168.1.45\n"
            + (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M") + " - Shared 2 folders with collaborators\n"
            + (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d %H:%M") + " - Login from IP 192.168.1.45\n"
            + (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M") + " - Uploaded 5 files (8.7 MB)\n\n"
            "FEATURES USED AFTER CHARGE:\n"
            "• Cloud Storage: 23.4 GB actively stored\n"
            "• Document Editing: 47 documents created/modified\n"
            "• Collaboration: 12 shared workspaces\n"
            "• Video Calls: 3 sessions (total 127 minutes)\n"
            "• API Integration: 342 API calls\n\n"
            "Customer has shown consistent, active engagement with the platform, "
            "demonstrating clear intent to continue using the subscription service."
        ),



        # Refund Policy
        "refund_policy_disclosure": (
            "Our refund policy is clearly stated in our Terms of Service (accepted "
            + purchase_date.strftime("%B %d, %Y") + ") and displayed on our pricing page:\n\n"
            "'REFUND POLICY: Subscription fees are non-refundable. If you cancel your subscription, "
            "you will continue to have access until the end of your current billing period, but no "
            "refund will be issued for the current period. To avoid future charges, cancel at least "
            "5 days before your next billing date.'\n\n"
            "This policy was acknowledged by the customer at signup via checkbox confirmation."
        ),

        # Refund Refusal Explanation
        "refund_refusal_explanation": (
            "We cannot issue a refund for the following reasons:\n\n"
            "1. SERVICE WAS DELIVERED: Customer had full access to all premium features during the billing period.\n\n"
            "2. SERVICE WAS ACTIVELY USED: Extensive usage logs prove customer actively used the service "
            "after the charge (23 logins, 8 file uploads, 342 API calls).\n\n"
            "3. NO CANCELLATION REQUEST: Customer never submitted a cancellation request through any channel "
            "(account portal, email, phone, or chat).\n\n"
            "4. TERMS ACCEPTED: Customer explicitly accepted our no-refund policy at signup.\n\n"
            "5. ADVANCE NOTICE PROVIDED: Customer was notified 7 days and 3 days before the charge with "
            "clear cancellation instructions. Customer opened the reminder email but took no action.\n\n"
            "6. CONTINUED SUBSCRIPTION: Customer's subscription remains active with auto-renew enabled, "
            "and they continue to store 23.4 GB of data on our platform.\n\n"
            "This charge is legitimate and in accordance with the customer's agreed subscription terms."
        ),

        # Additional Context (All narrative evidence goes here)
        "uncategorized_text": (
            "=== COMPREHENSIVE DISPUTE EVIDENCE ===\n\n"
            "=== EMAIL COMMUNICATION HISTORY ===\n"
            + purchase_date.strftime("%Y-%m-%d") + " - Welcome Email sent and opened\n"
            + (last_billing - timedelta(days=7)).strftime("%Y-%m-%d") + " - Renewal reminder sent and opened\n"
            + (last_billing - timedelta(days=3)).strftime("%Y-%m-%d") + " - Final billing reminder ($29.99) sent and opened\n"
            + last_billing.strftime("%Y-%m-%d") + " - Invoice & receipt sent\n"
            "Customer opened billing reminders but never contacted support about cancellation.\n\n"
            "=== RECEIPT/INVOICE ===\n"
            "Invoice #INV-2024-" + last_billing.strftime("%m%d") + "\n"
            "Item: Premium Digital Workspace - Monthly Subscription\n"
            "Period: " + last_billing.strftime("%b %d") + " - " + (last_billing + timedelta(days=30)).strftime("%b %d, %Y") + "\n"
            "Amount: $29.99 USD\n"
            "Transaction ID: (will be added)\n"
            "Status: Paid\n\n"
            "=== ADDITIONAL EVIDENCE & CONTEXT ===\n\n"
            "CUSTOMER ACCOUNT DETAILS:\n"
            "• Account Created: " + purchase_date.strftime("%B %d, %Y") + "\n"
            "• Account Status: Active (currently logged in)\n"
            "• Subscription Type: Premium Monthly ($29.99/month)\n"
            "• Auto-Renew: Enabled\n"
            "• Payment Method: Visa ****4242 (expires 12/2025)\n"
            "• Previous Charges: 2 successful charges with no disputes\n"
            "• Account Age: 45 days\n\n"
            "SUBSCRIPTION HISTORY:\n"
            "• " + (last_billing - timedelta(days=60)).strftime("%Y-%m-%d") + ": First charge $29.99 - Successful\n"
            "• " + (last_billing - timedelta(days=30)).strftime("%Y-%m-%d") + ": Second charge $29.99 - Successful\n"
            "• " + last_billing.strftime("%Y-%m-%d") + ": Third charge $29.99 - DISPUTED\n\n"
            "PLATFORM USAGE METRICS:\n"
            "• Total Files: 47 (23.4 GB)\n"
            "• Shared Workspaces: 12\n"
            "• Collaborators Added: 5\n"
            "• Projects Created: 8\n"
            "• Video Conference Minutes: 247\n"
            "• Document Edits: 1,284\n"
            "• API Integrations: 3 active\n\n"
            "CANCELLATION POLICY ENFORCEMENT:\n"
            "Our cancellation process is simple and accessible:\n"
            "1. Log into account → Settings → Subscription → 'Cancel Subscription'\n"
            "2. Or email support@example.com\n"
            "3. Cancellation takes effect at end of current period\n"
            "4. Automatic confirmation email sent immediately\n\n"
            "The customer has not used either method. Our system shows zero cancellation attempts.\n\n"
            "DISPUTE PATTERN ANALYSIS:\n"
            "This appears to be an illegitimate dispute based on:\n"
            "• Continued active service usage after the charge\n"
            "• No prior cancellation attempt or support contact\n"
            "• Customer opened billing reminders but took no action\n"
            "• Account still active with auto-renew enabled\n"
            "• Pattern suggests buyer's remorse rather than legitimate complaint\n\n"
            "MERCHANT POSITION:\n"
            "We respectfully request this dispute be resolved in our favor. The customer:\n"
            "1. Agreed to automatic recurring billing\n"
            "2. Was notified multiple times before the charge\n"
            "3. Never requested cancellation through any channel\n"
            "4. Actively used the service before and after the charge\n"
            "5. Continues to use the service while disputing payment\n\n"
            "This charge is valid, authorized, and for services actively consumed by the customer."
        ),
    }

    print(f"   ✓ Evidence prepared with {len([v for v in evidence.values() if v])} fields")
    print(f"   ✓ Total evidence characters: {sum(len(str(v)) for v in evidence.values() if v):,}")

    # Step 5: Evidence prepared but NOT submitted
    print("\n📋 Step 5: Evidence prepared (NOT submitted)")
    print("   ✓ Evidence is ready but NOT yet submitted to Stripe")
    print("   ✓ All evidence fields prepared with detailed information")
    print("   ℹ You can submit evidence manually via Stripe Dashboard or API")
    print(f"   ℹ Evidence due by: {datetime.fromtimestamp(dispute.evidence_details.due_by).strftime('%B %d, %Y')}")

    updated_dispute = dispute

    # Summary
    print("\n" + "="*80)
    print("✅ DETAILED DISPUTE CASE CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"Customer: {customer.name} ({customer.email})")
    print(f"Charge: {charge.id} (${charge.amount/100:.2f})")
    print(f"Dispute: {dispute.id}")
    print(f"Reason: {dispute.reason} (auto-assigned by Stripe test mode)")
    print(f"Scenario Type: subscription_canceled (in metadata)")
    print(f"Status: {updated_dispute.status}")
    print(f"\nℹ️  NOTE: In test mode, Stripe auto-assigns dispute reason as '{dispute.reason}'.")
    print("   The actual scenario 'subscription_canceled' is stored in metadata and evidence.")
    print("\n📊 Evidence Summary:")
    print(f"  • Customer details: email, name, IP, billing address")
    print(f"  • Product description: Comprehensive service details")
    print(f"  • Cancellation policy: Full disclosure with acceptance proof")
    print(f"  • Cancellation rebuttal: Detailed explanation why claim is invalid")
    print(f"  • Access logs: 23 logins, 8 uploads, 342 API calls after charge")
    print(f"  • Customer communications: 4 emails sent, reminders opened")
    print(f"  • Service date: Billing period clearly stated")
    print(f"  • Receipt: Full invoice with transaction details")
    print(f"  • Refund policy: Non-refund terms accepted at signup")
    print(f"  • Additional context: Usage metrics, account history, merchant position")
    print("\n🎯 Merchant Position: STRONG CASE TO WIN")
    print("   Evidence proves:")
    print("   ✓ No cancellation request was ever made")
    print("   ✓ Customer actively used service after charge")
    print("   ✓ Customer was notified and acknowledged upcoming charge")
    print("   ✓ Service delivered as promised")
    print("   ✓ Terms and policies clearly accepted")
    print("\n📍 View in Dashboard:")
    print(f"   • Dispute: https://dashboard.stripe.com/test/disputes/{dispute.id}")
    print(f"   • Charge: https://dashboard.stripe.com/test/payments/{charge.id}")
    print(f"   • Customer: https://dashboard.stripe.com/test/customers/{customer.id}")
    print("="*80 + "\n")

    return {
        "customer": customer,
        "charge": charge,
        "dispute": dispute,
        "evidence": evidence,
    }


if __name__ == "__main__":
    result = create_detailed_subscription_case()
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
