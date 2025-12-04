import React, { useState } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import Disputes from './components/Disputes';
import Automations from './components/Automations';
import AgentStudio from './components/AgentStudio';
import Integrations from './components/Integrations';
import { ViewState, DisputeStatus, KPIMetrics, Dispute } from './types';

// Mock Data
const MOCK_DISPUTES: Dispute[] = [
  {
    id: 'bBhOHQiTL4...LrXY',
    customerName: 'Trisha Fisher',
    amount: 89.95,
    timeLeftHours: 4,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 22,
    orderItems: ['Huel Black Edition Vanilla x2'],
    date: 'Sep 12th, 2024',
    paymentSource: 'visa',
    agentName: 'Fraud Detection',
    callResult: 'Required police report - Customer refused',
    chargeId: 'ch_3SaQFuAITa6PCFHj0dnBlMJP', // Add charge ID for conversation
    transcript: `Agent: ChargeGuard connected.
Agent: Hi Trisha, I see you've disputed the charge for Huel Black Edition. Can you tell me more?
Customer: I never received them. Tracking says delivered but it wasn't there.
Agent: I understand. I can see the GPS coordinates from the carrier match your address exactly.
Customer: Well, maybe my neighbor took it.
Agent: In cases of "Porch Piracy", we usually require a police report to process a refund.
Customer: That's too much work. Just refund me.`
  },
  {
    id: 'JKpnBl4uTx...mRtU',
    customerName: 'Sarah Jenkins',
    amount: 65.00,
    timeLeftHours: 56,
    status: DisputeStatus.Pending,
    confidenceScore: 92,
    orderItems: ['Huel Subscription Box'],
    date: 'Jul 17th, 2024',
    paymentSource: 'mastercard',
    agentName: 'Subscription Support',
    callResult: 'Cancelled subscription + $65 refund issued',
    transcript: `Agent: ChargeGuard connected. Good afternoon Sarah, I see you've reached out regarding your Huel subscription. How can I help you today?
Customer: Yes, hi. I want to cancel my subscription. I called last month to cancel it but I'm still being charged.
Agent: I apologize for the inconvenience. Let me pull up your account right now. Can you confirm the email address on the account?
Customer: It's sarah.jenkins@email.com
Agent: Thank you. I can see here that your Huel subscription was set to auto-renew on the 15th of each month. I don't show any previous cancellation request in our system. When did you call to cancel?
Customer: It was around June 20th. I spoke with someone and they said it would be cancelled.
Agent: I understand your frustration. Unfortunately, I'm not seeing that cancellation recorded. However, I can process the cancellation right now and issue a full refund for this month's charge since there was clearly a miscommunication.
Customer: Okay, that sounds fair. Thank you.
Agent: You're welcome. I've cancelled the subscription effective immediately and processed a $65 refund to your Mastercard ending in 4829. You should see it in 3-5 business days. Is there anything else I can help with?
Customer: No, that's all. Thanks for handling this.
Agent: My pleasure, Sarah. Have a great day!`
  },
  {
    id: 'SDFmMlb14o...Dd7A',
    customerName: 'David Ross',
    amount: 54.00,
    timeLeftHours: 18,
    status: DisputeStatus.Lost,
    confidenceScore: 10,
    orderItems: ['Huel Ready-to-Drink Chocolate x12'],
    date: 'Jul 17th, 2024',
    paymentSource: 'amex',
    agentName: 'Product Quality',
    callResult: 'Refused return policy - Call ended',
    transcript: `Agent: ChargeGuard connected. Hello, this is Alex from customer support. Am I speaking with David?
Customer: Yeah, this is David.
Agent: Great! I see you've disputed a charge for $54 for Huel Ready-to-Drink bottles. Can you tell me what the issue is?
Customer: I want a refund. The product tastes awful.
Agent: I'm sorry to hear that. Can you describe what's wrong with the taste?
Customer: It just doesn't taste good.
Agent: I understand. Have you tried our other flavors? Sometimes taste preferences vary by—
Customer: Look, I don't have time for this. Just give me my money back.
Agent: I completely understand your frustration. To process a return, we'll need you to send the unopened bottles back to us. I can email you a prepaid shipping label right now.
Customer: Why do I have to ship it back? Just refund me.
Agent: Our policy requires returned items so we can inspect them and improve our quality control. Once we receive the unopened bottles, we'll process your refund within 2 business days.
Customer: This is ridiculous. Forget it.
Agent: I apologize for the inconvenience, David. Is there anything else I can help you with today?
Customer: No. [Call ends]`
  },
  {
    id: 'KL1nA2rN3a...8XyZ',
    customerName: 'Emma Nielsen',
    amount: 75.00,
    timeLeftHours: 45,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 72,
    orderItems: ['Huel Complete Protein Vanilla x2'],
    date: 'Jan 29th, 2025',
    paymentSource: 'klarna',
    agentName: 'Delivery Issues',
    callResult: 'Filed carrier claim + $75 refund approved',
    transcript: `Agent: ChargeGuard connected. Hello, this is Sarah from billing support. Am I speaking with Emma Nielsen?
Customer: Yes, this is Emma.
Agent: Thank you. I see you've disputed a charge for $75 for Huel Complete Protein. Can you tell me what happened?
Customer: I never received the package. The tracking says it was delivered, but I checked everywhere and it's not here.
Agent: I'm very sorry to hear that. Let me look into this for you. Can you confirm the delivery address we have on file?
Customer: Yes, it's 245 Oak Street, Apartment 3B.
Agent: Thank you. I see the package was marked as delivered three days ago. Have you checked with your building manager or neighbors?
Customer: Yes, I checked with the front desk and they don't have it. My neighbors haven't seen anything either.
Agent: I understand how frustrating this must be. Let me file a claim with the carrier and we'll get this resolved for you. In the meantime, would you like us to send a replacement or process a refund?
Customer: I'd prefer a refund at this point. I'm not sure I trust another delivery here.
Agent: That's completely understandable. I'll process that refund for you today. You should see it back on your Klarna account within 5-7 business days.
Customer: Thank you so much for your help.`
  },
  {
    id: 'KL4rN5aB6c...9WvU',
    customerName: 'Lars Svensson',
    amount: 95.00,
    timeLeftHours: 12,
    status: DisputeStatus.Won,
    confidenceScore: 91,
    orderItems: ['Huel Hot & Savory Thai Green Curry x4'],
    date: 'Jan 25th, 2025',
    paymentSource: 'klarna',
    agentName: 'Product Quality',
    callResult: 'Correct item reshipped + Keep wrong item',
    transcript: `Agent: ChargeGuard connected. Hello, this is Jordan from customer support. Am I speaking with Lars?
Customer: Yes, hello.
Agent: Hi Lars. I see you've disputed a charge for $95 for Huel Hot & Savory meals. What seems to be the issue?
Customer: I received the wrong flavor. I ordered Thai Green Curry but got Tomato & Herb instead.
Agent: I'm sorry to hear that. Let me check your order confirmation. Can you give me your order number?
Customer: Yes, it's HHS-20250122-7834.
Agent: Thank you. I can see here you definitely ordered Thai Green Curry. This was clearly our mistake in fulfillment.
Customer: That would be great, thank you.
Agent: Perfect. I'm processing that now. I'll send you the correct Thai Green Curry flavor within 2-3 business days, and you can keep the Tomato & Herb - no need to return it. Consider it our apology.
Customer: I appreciate your help with this.
Agent: You're very welcome, Lars. Is there anything else I can help you with today?
Customer: No, that's all. Thank you.`
  },
    {
    id: 'F1JULakYZT...4Vn1',
    customerName: 'Marcus Well',
    amount: 82.00,
    timeLeftHours: 70,
    status: DisputeStatus.Won,
    confidenceScore: 88,
    orderItems: ['Huel Powder v3.0 Berry x2'],
    date: 'Jul 17th, 2024',
    paymentSource: 'stripe',
    agentName: 'Fraud Detection',
    callResult: 'Verified theft + Replacement shipped with signature',
    transcript: `Agent: ChargeGuard connected. Good morning Marcus, I'm calling about the Huel Powder Berry you ordered. I see there's been a dispute filed. What seems to be the problem?
Customer: Hi, yeah. I ordered Huel Powder three weeks ago and it still hasn't arrived. I've been tracking it and it says it was delivered, but I never got it.
Agent: I'm sorry to hear that. Let me look into this for you right away. Can I have your order number?
Customer: Sure, it's HUL-992847.
Agent: Thank you. I'm pulling up your order now. I can see here that according to our shipping partner, the package was delivered on July 3rd at 2:47 PM and was left at the front door. Do you have any security cameras or can you check with neighbors?
Customer: I've already checked with my neighbors and looked at my Ring camera footage. There's video of the delivery driver dropping it off, and then about 20 minutes later, you can see someone walk up and take the package. It wasn't me or anyone I know.
Agent: Oh my, I'm very sorry this happened to you. That's clearly package theft. Have you filed a police report?
Customer: Yes, I filed one yesterday. I have the report number if you need it.
Agent: That would be helpful, yes. And I want you to know we're going to make this right. Since you have video evidence and a police report, I'm authorizing a full replacement to be shipped out today with signature confirmation required. You should receive it within 2-3 business days.
Customer: Really? Thank you so much! I really needed this for my meal prep.
Agent: Absolutely. Is the shipping address still the same?
Customer: Yes, same address.
Agent: Perfect. You'll receive a confirmation email within the hour with the new tracking number. The police report number for our records?
Customer: It's PR-2024-07-8934.
Agent: Got it. Is there anything else I can help you with today, Marcus?
Customer: No, that's everything. I really appreciate your help!
Agent: You're very welcome. Have a great day!`
  },
  {
    id: 'F9v2Qjq8QM...78QF',
    customerName: 'Emily Clark',
    amount: 48.00,
    timeLeftHours: 12,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 45,
    orderItems: ['Huel Daily Greens'],
    date: 'Jul 17th, 2024',
    paymentSource: 'paypal',
    agentName: 'Subscription Support',
    callResult: 'Found confirmation email - Dispute closed',
    transcript: `Agent: ChargeGuard connected. Hi Emily, I'm reaching out about your recent Huel Daily Greens purchase. I see you've opened a dispute. What can I help you with?
Customer: Yes, I bought Daily Greens but I haven't received my order confirmation or tracking number. I'm worried it didn't go through.
Agent: I apologize for that concern. Let me check your account. When did you make the purchase?
Customer: Yesterday around noon.
Agent: Okay, I can see your order here. It looks like the confirmation email was sent to emily.clark.design@gmail.com. Is that the correct email?
Customer: Oh... I think I used my work email. Can you check emily.clark@brightwave.com?
Agent: Let me look... yes! The order confirmation and tracking information were sent to emily.clark@brightwave.com on July 16th at 12:34 PM. Can you check that inbox?
Customer: Hold on... oh my god, I see it now. I'm so sorry, I completely forgot I used my work email for the checkout.
Agent: No worries at all! These things happen. Can you see the tracking number now?
Customer: Let me check... yes! It's already shipped and arriving tomorrow. I feel so silly.
Agent: Don't worry about it! I'm just glad we sorted it out. Will you be able to close the dispute on your end?
Customer: Yes, I'll do that right now. Thank you for your patience.
Agent: Anytime! Enjoy your Daily Greens, Emily!`
  },
  {
    id: 'KL9mNp2qRs...3TuV',
    customerName: 'James Martinez',
    amount: 68.00,
    timeLeftHours: 48,
    status: DisputeStatus.Pending,
    confidenceScore: 78,
    orderItems: ['Huel Powder v3.0 Chocolate'],
    date: 'Jan 29th, 2025',
    paymentSource: 'visa',
    agentName: 'Product Quality',
    callResult: 'Firmware update applied - Awaiting feedback',
    transcript: `Agent: ChargeGuard connected. Hello James, this is Taylor from support. I see you've contacted us about the smart watch you purchased. What seems to be the issue?
Customer: Yeah, the watch doesn't work properly. The heart rate monitor is completely inaccurate and the battery dies after like 6 hours.
Agent: I'm sorry to hear you're having trouble. Let's troubleshoot this together. First, have you updated the firmware to the latest version? We released an update last week that addressed some battery and sensor issues.
Customer: No, I didn't know there was an update. How do I do that?
Agent: No problem! Open the companion app on your phone, go to Settings, then Device, and you should see "Software Update" at the bottom. Can you try that?
Customer: Okay, hold on... I see it. It says version 2.4.1 is available. Should I install it?
Agent: Yes, please do. It'll take about 5 minutes and the watch needs to be at least 50% charged.
Customer: It's at 60% now. Okay, updating... it's installing.
Agent: Perfect. While that's updating, let me also mention that for the heart rate monitor to work accurately, the watch needs to be worn snugly on your wrist, about one finger width above your wrist bone. Not too tight, but not loose either.
Customer: Oh, I've been wearing it pretty loose. That might be why.
Agent: That could definitely affect the readings. The update is finished?
Customer: Yes, just completed. It's restarting now.
Agent: Great! After it restarts, try wearing it a bit tighter and test the heart rate monitor. The battery life should also improve significantly with this update. If you're still having issues after 24 hours, please reach out and we'll process an exchange.
Customer: Okay, I'll try that. Thanks for the help.
Agent: You're welcome, James! Anything else I can help with?
Customer: No, that's all.
Agent: Have a great day!`
  },
  {
    id: 'WX4yZa5bCd...6EfG',
    customerName: 'Lisa Thompson',
    amount: 84.50,
    timeLeftHours: 68,
    status: DisputeStatus.Pending,
    confidenceScore: 65,
    orderItems: ['Yoga Mat Set'],
    date: 'Jan 29th, 2025',
    paymentSource: 'mastercard',
    agentName: 'Delivery Issues',
    callResult: 'Correct item expedited + Keep wrong item + 15% off next order',
    transcript: `Agent: ChargeGuard connected. Hi Lisa, I'm Jordan calling about your recent order. I understand there's an issue with your yoga mat set?
Customer: Yes, you shipped me the wrong item. I ordered the premium yoga mat set in purple, but I received a basic mat in blue.
Agent: I sincerely apologize for that mix-up. Let me pull up your order. Order number YM-4382, is that correct?
Customer: Yes, that's right.
Agent: I can see here you did order the Premium Deluxe Yoga Mat Set in Lavender Purple, which includes the mat, blocks, strap, and carrying case. You received a basic blue mat instead?
Customer: Exactly. Just a single blue mat, nothing else. I'm really disappointed because I was planning to use this for my classes this week.
Agent: I completely understand your frustration, and I want to make this right immediately. I'm going to send you the correct premium set with expedited shipping at no charge. You should receive it by Thursday.
Customer: Okay, that's good. What about this blue mat I got? Do I need to ship it back?
Agent: Actually, please keep it as our apology for the inconvenience. You can donate it, gift it, or use it as an extra mat.
Customer: Oh wow, that's really nice of you. Thank you!
Agent: It's the least we can do. I'm also applying a 15% discount to your next order as an additional apology. You'll receive an email confirmation with your new tracking number within the hour.
Customer: I appreciate you taking care of this so quickly.
Agent: Absolutely, Lisa. Is your shipping address still 482 Maple Grove Drive?
Customer: Yes, that's correct.
Agent: Perfect. You'll have your correct order by Thursday. Again, I apologize for the error. Enjoy your yoga practice!
Customer: Thank you so much!`
  },
  {
    id: 'HI7jKl8mNo...9PqR',
    customerName: 'Robert Anderson',
    amount: 199.00,
    timeLeftHours: 8,
    status: DisputeStatus.Lost,
    confidenceScore: 15,
    orderItems: ['Gaming Keyboard'],
    date: 'Jan 27th, 2025',
    paymentSource: 'paypal',
    agentName: 'Fraud Detection',
    callResult: 'No duplicate charge found - Escalated to PayPal',
    transcript: `Agent: ChargeGuard connected. Hello, this is Morgan from billing support. Am I speaking with Robert Anderson?
Customer: Yeah. I was charged twice for the same keyboard. I want my money back now.
Agent: I understand your concern. Let me look into this right away. Can you provide the order number or the date of purchase?
Customer: I don't have the order number. I ordered it like two weeks ago.
Agent: No problem. Let me search by your account. I see a purchase for a gaming keyboard on January 13th for $199. Is that the one?
Customer: Yeah, but I was charged twice. Check my PayPal.
Agent: I'm looking at our records now. I show only one charge of $199 that was processed on January 13th. Did you see two separate charges on your PayPal account?
Customer: Yes! Two charges of $199 each.
Agent: I understand. Sometimes what happens is you might see a pending authorization charge and then the actual charge. The pending one typically falls off within 3-5 business days. Can you check if both charges show as "Completed" or if one says "Pending"?
Customer: They both say completed.
Agent: That's unusual. Can you send me a screenshot of your PayPal transaction history showing both charges? You can email it to support@huel.com with your order number.
Customer: I'm not doing all that. Just refund me one of the charges.
Agent: I completely understand your frustration, but I need to verify the duplicate charge before I can process a refund. On our end, I only see one transaction. If there truly is a duplicate, it might be a PayPal processing error, and I'll need that documentation to issue a refund and file a report with PayPal.
Customer: This is ridiculous. Forget it, I'll just do a chargeback.
Agent: I want to help resolve this, Robert. If you can provide the screenshot, I can have this resolved within 24 hours. Would that work?
Customer: [Call disconnected]`
  },
  {
    id: 'ST0uVw1xYz...2AbC',
    customerName: 'Michelle Lee',
    amount: 45.99,
    timeLeftHours: 52,
    status: DisputeStatus.Pending,
    confidenceScore: 82,
    orderItems: ['Phone Case'],
    date: 'Jan 26th, 2025',
    paymentSource: 'stripe',
    agentName: 'Product Quality',
    callResult: 'Full refund + Keep item + 20% off code',
    transcript: `Agent: ChargeGuard connected. Hi Michelle, I'm calling about your phone case order. I see you've indicated the item wasn't as described. Can you tell me more?
Customer: Yes, the listing said it was made of genuine leather, but this is obviously fake leather or pleather. I specifically paid extra for real leather.
Agent: I understand your disappointment. That's not acceptable. Can I get your order number?
Customer: It's PC-7729.
Agent: Thank you. I'm looking at your order now. You're absolutely right - the product page does specify genuine leather. Do you still have the packaging it came in?
Customer: Yes, I do. The label on the package actually says "vegan leather" which is just fake leather.
Agent: I apologize for this discrepancy. This is clearly our error - either in the product description or fulfillment. I'm going to process a full refund for you right now, and you can keep the case.
Customer: Really? I don't have to return it?
Agent: Correct. Since we misrepresented the product, the refund is on us and you don't need to return anything. The $45.99 will be back in your account within 3-5 business days.
Customer: That's very fair. Thank you for handling this so professionally.
Agent: It's the least we can do. I'm also going to flag this product listing to our inventory team to correct the description. Would you like a discount code for a future purchase?
Customer: Sure, that would be nice.
Agent: I've emailed you a 20% off code that's valid for 90 days. Again, I apologize for the confusion.
Customer: I appreciate it. Thank you!
Agent: You're welcome, Michelle. Have a great day!`
  },
  {
    id: 'DE3fGh4iJk...5LmN',
    customerName: 'Kevin Brown',
    amount: 159.99,
    timeLeftHours: 32,
    status: DisputeStatus.Pending,
    confidenceScore: 71,
    orderItems: ['Bluetooth Speaker'],
    date: 'Jan 25th, 2025',
    paymentSource: 'amex',
    agentName: 'Delivery Issues',
    callResult: 'Replacement shipped with signature + Photos emailed',
    transcript: `Agent: ChargeGuard connected. Hello Kevin, I'm reaching out regarding your Bluetooth speaker order. I understand it arrived damaged?
Customer: Yes, the box was completely crushed when it arrived. The speaker has a huge dent on the side and it's making a rattling noise when I shake it.
Agent: I'm very sorry about that. It sounds like the package wasn't handled properly during shipping. Did you take any photos of the damage and the packaging?
Customer: Yes, I took several photos showing the damaged box and the dent on the speaker.
Agent: Perfect, that's very helpful. Can you email those to claims@huel.com with your order number BT-9384?
Customer: Sure, I can do that right now.
Agent: Thank you. While you're doing that, let me process a replacement order for you. We'll ship it with extra protective packaging and signature confirmation to prevent this from happening again. Would you like the same color, Midnight Black?
Customer: Actually, do you have it in silver?
Agent: Let me check... yes, we have the silver in stock. I'll send that instead.
Customer: Great, thank you.
Agent: You're welcome. For the damaged one, you can either return it using a prepaid label I'll email you, or if you prefer, you can keep it for parts or dispose of it - your choice.
Customer: I'll probably just toss it since it doesn't work properly.
Agent: That's fine. Your replacement will ship today and arrive by Wednesday. I've also added a $25 credit to your account as an apology for the inconvenience.
Customer: Oh, that's not necessary but thank you! I appreciate the quick resolution.
Agent: It's our pleasure, Kevin. Just email those photos when you can and you're all set.
Customer: Will do. Thanks again!
Agent: Have a great day!`
  },
  {
    id: 'OP6qRs7tUv...8WxY',
    customerName: 'Amanda Wilson',
    amount: 74.95,
    timeLeftHours: 16,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 38,
    orderItems: ['Fitness Tracker'],
    date: 'Jan 24th, 2025',
    paymentSource: 'visa',
    agentName: 'Fraud Detection',
    callResult: 'Customer authorized - Dispute closed',
    transcript: `Agent: ChargeGuard connected. Hi Amanda, I'm calling from Huel regarding a charge on your account for $74.95. I see you've disputed this transaction stating you never ordered this item. Is that correct?
Customer: Yes, I never ordered any fitness tracker. I don't even know what your company sells. This is fraudulent.
Agent: I understand your concern. Let me investigate this for you. The order was placed on January 10th at 3:22 PM from IP address 192.168.1.1 and shipped to 847 Rosewood Lane, Apartment 3B. Is that your address?
Customer: Yes, that's my address, but I didn't order anything.
Agent: I see. The email on the account is amanda.wilson.fit@gmail.com. Is that your email?
Customer: Yes, that's my email, but I'm telling you I didn't place this order!
Agent: I believe you. Let me check if the item was actually delivered. According to tracking, it was delivered to your address on January 15th. Did you receive a package around that time?
Customer: I... wait. Actually, my daughter might have ordered something. She's 16 and sometimes uses my card. Let me ask her.
Agent: Take your time.
Customer: [pause] Oh my god, I'm so sorry. She just told me she ordered it with my permission but I completely forgot. She asked me like a month ago and I said yes. I'm really sorry for wasting your time.
Agent: No need to apologize! This happens more often than you'd think. So you'd like to keep the fitness tracker then?
Customer: Yes, I'm so embarrassed. Can I cancel this dispute?
Agent: Absolutely, I'll close the dispute on our end right now. You don't need to do anything else. Is there anything else I can help you with?
Customer: No, and again, I'm really sorry.
Agent: Don't worry about it at all! Have a wonderful day, Amanda!`
  },
  {
    id: 'ZA9bCd0eEf...1GhI',
    customerName: 'Daniel Garcia',
    amount: 219.00,
    timeLeftHours: 72,
    status: DisputeStatus.Won,
    confidenceScore: 94,
    orderItems: ['Laptop Stand'],
    date: 'Jan 23rd, 2025',
    paymentSource: 'mastercard',
    agentName: 'Product Quality',
    callResult: 'Quick resolution - Refund processed',
    transcript: `Agent: Hello Daniel.\nCustomer: Issue resolved.`
  },
  {
    id: 'JK2lMn3oOp...4QrS',
    customerName: 'Jessica Taylor',
    amount: 39.99,
    timeLeftHours: 44,
    status: DisputeStatus.Pending,
    confidenceScore: 67,
    orderItems: ['Water Bottle'],
    date: 'Jan 22nd, 2025',
    paymentSource: 'paypal',
    agentName: 'Product Quality',
    callResult: 'Defective - Replacement sent',
    transcript: `Agent: Hi Jessica.\nCustomer: Defective product.`
  },
  {
    id: 'TU5vWx6yYz...7ZaB',
    customerName: 'Christopher White',
    amount: 189.50,
    timeLeftHours: 6,
    status: DisputeStatus.Lost,
    confidenceScore: 28,
    orderItems: ['Desk Lamp'],
    date: 'Jan 21st, 2025',
    paymentSource: 'stripe',
    agentName: 'Fraud Detection',
    callResult: 'Unreasonable demand - Escalated',
    transcript: `Agent: Hello Christopher.\nCustomer: Want refund immediately.`
  },
  {
    id: 'CD8eEf9gGh...0HiJ',
    customerName: 'Nicole Harris',
    amount: 94.99,
    timeLeftHours: 64,
    status: DisputeStatus.Pending,
    confidenceScore: 76,
    orderItems: ['Running Shoes'],
    date: 'Jan 20th, 2025',
    paymentSource: 'amex',
    agentName: 'Delivery Issues',
    callResult: 'Exchange for correct size processed',
    transcript: `Agent: Hi Nicole.\nCustomer: Wrong size sent.`
  },
  {
    id: 'KL1mNn2oOp...3PqR',
    customerName: 'Brandon Clark',
    amount: 149.00,
    timeLeftHours: 36,
    status: DisputeStatus.Pending,
    confidenceScore: 85,
    orderItems: ['Webcam'],
    date: 'Jan 19th, 2025',
    paymentSource: 'visa',
    agentName: 'Product Quality',
    callResult: 'Return authorized + Full refund',
    transcript: `Agent: Hello Brandon.\nCustomer: Poor quality.`
  },
  {
    id: 'ST4uVv5wWx...6XyZ',
    customerName: 'Rachel Lewis',
    amount: 67.50,
    timeLeftHours: 20,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 41,
    orderItems: ['Backpack'],
    date: 'Jan 18th, 2025',
    paymentSource: 'mastercard',
    agentName: 'Fraud Detection',
    callResult: 'Investigating unauthorized claim',
    transcript: `Agent: Hi Rachel.\nCustomer: Unauthorized charge.`
  },
  {
    id: 'AB7cDd8eEf...9FgH',
    customerName: 'Justin Walker',
    amount: 119.99,
    timeLeftHours: 58,
    status: DisputeStatus.Pending,
    confidenceScore: 72,
    orderItems: ['Huel Complete Protein Chocolate x3'],
    date: 'Jan 17th, 2025',
    paymentSource: 'paypal',
    agentName: 'Product Quality',
    callResult: 'Wrong flavor - Correct item shipped',
    transcript: `Agent: Hello Justin.\nCustomer: Not what I ordered.`
  },
  {
    id: 'IJ0kLl1mMn...2NoP',
    customerName: 'Stephanie Hall',
    amount: 54.95,
    timeLeftHours: 28,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 52,
    orderItems: ['Huel Powder v3.0 Vanilla'],
    date: 'Jan 16th, 2025',
    paymentSource: 'stripe',
    agentName: 'Product Quality',
    callResult: 'Texture complaint - Replacement offered',
    transcript: `Agent: Hi Stephanie.\nCustomer: Doesn't work properly.`
  },
  {
    id: 'QR3sTs4uUv...5VwX',
    customerName: 'Andrew Young',
    amount: 179.00,
    timeLeftHours: 71,
    status: DisputeStatus.Won,
    confidenceScore: 91,
    orderItems: ['Huel Bundle - Complete Nutrition Pack'],
    date: 'Jan 15th, 2025',
    paymentSource: 'amex',
    agentName: 'Subscription Support',
    callResult: 'Resolved - Customer satisfied',
    transcript: `Agent: Hello Andrew.\nCustomer: All good now.`
  },
  {
    id: 'YZ6aAb7cCd...8DeF',
    customerName: 'Patricia King',
    amount: 89.99,
    timeLeftHours: 42,
    status: DisputeStatus.Pending,
    confidenceScore: 69,
    orderItems: ['Huel Ready-to-Drink Variety Pack x12'],
    date: 'Jan 14th, 2025',
    paymentSource: 'visa',
    agentName: 'Product Quality',
    callResult: 'Expired product - Full refund + Replacement',
    transcript: `Agent: Hi Patricia.\nCustomer: Stopped working.`
  },
  {
    id: 'GH9iJj0kKl...1LmM',
    customerName: 'Gregory Scott',
    amount: 249.00,
    timeLeftHours: 14,
    status: DisputeStatus.ActionRequired,
    confidenceScore: 33,
    orderItems: ['Huel Starter Bundle + Shaker'],
    date: 'Jan 13th, 2025',
    paymentSource: 'mastercard',
    agentName: 'Delivery Issues',
    callResult: 'Missing shaker - Expedited shipping',
    transcript: `Agent: Hello Gregory.\nCustomer: Missing parts.`
  },
  {
    id: 'NO2pPq3rRs...4StT',
    customerName: 'Melissa Green',
    amount: 62.50,
    timeLeftHours: 54,
    status: DisputeStatus.Pending,
    confidenceScore: 79,
    orderItems: ['Huel Daily Greens'],
    date: 'Jan 12th, 2025',
    paymentSource: 'paypal',
    agentName: 'Subscription Support',
    callResult: 'Double delivery - Keep both + Credit applied',
    transcript: `Agent: Hi Melissa.\nCustomer: Color is wrong.`
  }
];

const MOCK_METRICS: KPIMetrics = {
  savedRevenue: 418282,
  deflectionRate: 64,
  activeDisputes: 7773,
  recentWins: []
};

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewState>('overview');

  const renderView = () => {
    switch (currentView) {
      case 'overview':
        return <Dashboard metrics={MOCK_METRICS} />;
      case 'disputes':
        return <Disputes disputes={MOCK_DISPUTES} />;
      case 'automations':
        return <Automations />;
      case 'agent-studio':
        return <AgentStudio />;
      case 'integrations':
        return <Integrations />;
      default:
        return <Dashboard metrics={MOCK_METRICS} />;
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[#F8FAFC] font-sans text-slate-900 overflow-hidden">
      <Header currentView={currentView} onChangeView={setCurrentView} />
      <main className="flex-1 overflow-auto">
        <div className="p-4 md:p-5 max-w-[2000px] mx-auto w-full">
          {renderView()}
        </div>
      </main>
    </div>
  );
};

export default App;
