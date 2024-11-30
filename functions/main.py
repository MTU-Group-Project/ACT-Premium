from firebase_functions import https_fn
from firebase_admin import initialize_app
import stripe
import status

stripe.api_key = "sk_test_51QKcauDGbrVfwZ9wnSzI0I9l4aOnySfGsU95QJgK1TsrbTyBtx6H5MCpckVZnMPo9K4Vvggt156UGT894Lh2XHZY00sUxL2YuN"

@https_fn.on_request()
def act_premium_buy(req: https_fn.Request):
    payment = stripe.PaymentIntent.create(amount=1099, currency="eur")

    return {
        "secret": payment.client_secret,
        "id": payment.id
    }


@https_fn.on_request()
def act_premium_purchased(req: https_fn.Request):
    # Get payment ID from URL parameter
    if "payment_id" not in req.args:
        raise status.BadRequest("No payment_id provided")

    pay_id = req.args["payment_id"]

    pay_intent = stripe.PaymentIntent.retrieve(pay_id)

    if pay_intent.status != "succeeded":
        pay_intent.confirm()

    if pay_intent.statement_descriptor == "succeeded":
          return {"status": 1}
    else:
          return {"status": 0}
