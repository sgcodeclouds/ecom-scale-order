from app.main import bp
from app.models.order import Order
from app.extensions import db
from flask import request
from app.util.app_util import generate_response
from app.middleware.auth import authenticate_token

@bp.before_request
@authenticate_token()
def before_request():
    pass

@bp.route("/", methods=["GET"])
def getOrders():
    order_id = request.args.get('order_id')
    if order_id:
        orders = Order.query.filter_by(id=order_id).all()
    else:
        orders = Order.query.all()
    response = []
    for orderp in orders: response.append(orderp.toDict())

    return generate_response(success=True, message="orders fetched", data=response), 200

@bp.route("/", methods=["POST"])
def addOrder():
    try:
        req = request.get_json()
        new_order = Order(
            payment_id = req['payment_id'],
            items = req['items'],
            order_total = req['order_total'],
            user_id = req['user_id']
        )

        db.session.add(new_order)
        db.session.commit()
        return generate_response(success=True, message="Order created", data=new_order.toDict()), 201
    except ValueError as e:
        return generate_response(success=False, message="something went wrong", errors=str(e)), 400

@bp.route("/<int:order_id>", methods=["PUT"])
def updateOrder(order_id):
    try:
        orderD = Order.query.get(order_id)
        req = request.get_json()
        # print(req)
        if 'payment_id' in req:
            orderD.payment_id = req['payment_id']
        
        db.session.commit()

        # return f"updated cart with id {cartD.id}", 200
        return generate_response(success=True, message="order updated", data=orderD.toDict()), 200
    except:
        # return "not found the cart id", 200
        return generate_response(success=False, message="order id not found", errors={"id":order_id}), 404

# @bp.route("/<int:order_id>", methods=["DELETE"])
# def deleteOrder(Order_id):
#     return generate_response(success=True, message="order deleted", data={}), 200
    
