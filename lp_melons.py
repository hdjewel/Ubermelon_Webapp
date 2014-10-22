from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""

    # this is where we add the logic to get the qty from the "session cart"
    #   that was "built" the "add_to_cart" function.
    # then use the melon ids in the "cart" create a list of melons.  
    # The melon details can be retrieved using the "model.get_melon_by_id".
    # get_melon_by_id returns id, melon_type, common_name, price, imgurl,
    #    flesh_color, rind_color, seedless
    # Before passing the "melons" remember to calculate the "total price"
    # and add it to the retrieved list of attributes.
    if "cart" in session:
        melons = []
        running_total = 0
        for key in session["cart"]:

            melon =  model.get_melon_by_id(key)

            total_price = melon.price * session["cart"][key]
            print total_price

            melons = melons + [[melon.common_name, session["cart"][key], 
                               melon.price, total_price]]
            print "melons =",
            print melons
            running_total = running_total + total_price
            print "Order total = ", running_total

        session["order total"] = running_total
        print "session = ", session
    return render_template("cart.html", melons = melons)

    # return render_template("cart.html")

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

     # add logicc here to populate the "Sessions dynamic database"
     #  if "add ot cart button pressed " --- no if needed cause this is called 
     #                                        when the button is pressed
     #  if items exists in sessions 
     #     if key exist in sessions
     #         add 1 to quanty of the key
     #     else
     #        append "melon name as key: [qty = 1 , price]  ** calculate
     #                             total before deplaying the cart page" 
     #  otherwise
     #     add "melon name key : [qty = 1, price] "    
    
    # the following lines print to the "terminal window"
    id = str(id)    
    print 0.0 , "0 +++++++++++++++++++++++++++++++++++"
    print "id = ",
    print id
    if "cart" in session:
        print "  value = ",
        print session["cart"].get(id)
        if str(id) in session["cart"]:
                # session[id][1] += 1
            session["cart"][id] += 1
            print "1.0 ###################################"
            print session
        else:
            put_first_melon_in_cart(id)            
        print "1.1 ###################################"
        print session
    else:
        session["cart"] ={}
        put_first_melon_in_cart(id)
        print "1.2 ###################################"
        print session

    # return "Oops! This needs to be implemented!"
    # return "Successfully added to cart! id = %r qty =%r" % (id, session[id])

    #???flash "Successfully added to cart! id = %r qty =%r" % (id, session[id])

    flash("The melon was successfully added to the cart.")
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    request.object
    # return "Oops! This needs to be implemented"
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

def put_first_melon_in_cart(id):
    session["cart"][id] = 1

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
