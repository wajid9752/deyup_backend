from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("login/" , user_login ),
    path("profile/" , user_profile ),
    path("plans/" , plans_api ),
    path("logout/" , logout_view ),
    path("create-payment/" , create_payment ),
    path("success/" , payment_successful ),
    path("stripe_webhook/" , stripe_webhook ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# session {
#   "after_expiration": null,
#   "allow_promotion_codes": null,
#   "amount_subtotal": 100,
#   "amount_total": 100,
#   "automatic_tax": {
#     "enabled": false,
#     "status": null
#   },
#   "billing_address_collection": null,
#   "cancel_url": "http://127.0.0.1:8000/cancel/",
#   "client_reference_id": null,
#   "consent": null,
#   "consent_collection": null,
#   "created": 1696676676,
#   "currency": "inr",
#   "currency_conversion": null,
#   "custom_fields": [],
#   "custom_text": {
#     "shipping_address": null,
#     "submit": null,
#     "terms_of_service_acceptance": null
#   },
#   "customer": "cus_Om6XNb4UA8OETQ",
#   "customer_creation": "always",
#   "customer_details": {
#     "address": {
#       "city": null,
#       "country": "IN",
#       "line1": null,
#       "line2": null,
#       "postal_code": null,
#       "state": null
#     },
#     "email": "mawazid1051@gmail.com",
#     "name": "wajid",
#     "phone": null,
#     "tax_exempt": "none",
#     "tax_ids": []
#   },
#   "customer_email": "mawazid1051@gmail.com",
#   "expires_at": 1696763076,
#   "id": "cs_test_a1UPUVJ195Hb1hHFaFwfmQjF8kgsMGCZ3DHl9zJx4BqWpOIziZg6jLxoJ7",
#   "invoice": "in_1NyYKiSCw8UwFosbH7rr2I0T",
#   "invoice_creation": null,
#   "livemode": false,
#   "locale": null,
#   "metadata": {},
#   "mode": "subscription",
#   "object": "checkout.session",
#   "payment_intent": null,
#   "payment_link": null,
#   "payment_method_collection": "always",
#   "payment_method_configuration_details": null,
#   "payment_method_options": null,
#   "payment_method_types": [
#     "card"
#   ],
#   "payment_status": "paid",
#   "phone_number_collection": {
#     "enabled": false
#   },
#   "recovered_from": null,
#   "setup_intent": null,
#   "shipping_address_collection": null,
#   "shipping_cost": null,
#   "shipping_details": null,
#   "shipping_options": [],
#   "status": "complete",
#   "submit_type": null,
#   "subscription": "sub_1NyYKiSCw8UwFosbKSH0tOHD",
#   "success_url": "http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}",
#   "total_details": {
#     "amount_discount": 0,
#     "amount_shipping": 0,
#     "amount_tax": 0
#   },
#   "url": null
# }
# customer {
#   "address": {
#     "city": null,
#     "country": "IN",
#     "line1": null,
#     "line2": null,
#     "postal_code": null,
#     "state": null
#   },
#   "balance": 0,
#   "created": 1696676767,
#   "currency": "inr",
#   "default_source": null,
#   "delinquent": false,
#   "description": null,
#   "discount": null,
#   "email": "mawazid1051@gmail.com",
#   "id": "cus_Om6XNb4UA8OETQ",
#   "invoice_prefix": "969F8B11",
#   "invoice_settings": {
#     "custom_fields": null,
#     "default_payment_method": null,
#     "footer": null,
#     "rendering_options": null
#   },
#   "livemode": false,
#   "metadata": {},
#   "name": "wajid",
#   "next_invoice_sequence": 2,
#   "object": "customer",
#   "phone": null,
#   "preferred_locales": [
#     "en-GB"
#   ],
#   "shipping": null,
#   "tax_exempt": "none",
#   "test_clock": null
# }

# stripe listen --forward-to http://127.0.0.1:8000/stripe_webhook/ --api-key "sk_test_51MgLDhSCw8UwFosbFJJFSrxF6jSSFaOock1AtpKAwnjXQjMaH2oa5xh9X7ItywbtCdLWeITPtZwsx4Np3NZaMin600MhYEImAt"