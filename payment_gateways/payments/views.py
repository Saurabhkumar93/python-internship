# payments/views.py

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = 'sk_test_51QCw9H055q6k2Z6WvHUhQmoBkI6pcwOqA9tOXnNRst6LAhuP8yZxKX3Qxu6Y76TRTlxRW6D3vSuFgEFvkZqoh3OV00BDNUaObm'
WEBHOOK_SECRET = 'whsec_FoYdGlmKmW54HflkA4fjctjzEvgg9mw1'

def home(request):
    return render(request, 'payments/home.html', {
        'stripe_publishable_key': 'pk_test_51QCw9H055q6k2Z6W5YklXY4wmDRldsY6KTSqyXWGi2Hghyrhq9NSnks57MSxMCwOexgfU7rxJ4SyQIbprDvKFFy400O0zYNsZo',
    })

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Create a Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card', 'amazon_pay'],  # Supports wallets like Google Pay & Apple Pay too
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Test Product',
                            },
                            'unit_amount': 50000,  # ₹500 in paise
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )

            # Print the session details on the backend
            print(f"Checkout Session Created: {session.id}")

            return JsonResponse({'id': session.id})

        except Exception as e:
            print(f"Error creating checkout session: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        # Verify the webhook signature to ensure it's from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    # Handle the checkout session completion event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch payment details using the session ID
        payment_intent_id = session.get('payment_intent')
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Print transaction details
        print(f"Payment Successful! ID: {payment_intent.id}")
        print(f"Amount: {payment_intent.amount / 100} {payment_intent.currency.upper()}")
        print(f"Status: {payment_intent.status}")
        print(f"Customer Email: {session.get('customer_details', {}).get('email')}")

    return HttpResponse(status=200)

def success(request):
    return render(request, 'payments/success.html')

def cancel(request):
    return render(request, 'payments/cancel.html')
