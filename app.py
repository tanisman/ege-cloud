from time import sleep
from flask import Flask, stream_with_context, request, Response, flash, render_template, redirect, url_for

from database import Database

app = Flask(__name__)
app.secret_key = '!$w4wW~o|~8OVFX'  # !!change this with random key!!


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/list')
def list_items():

    def generate():  # our generator for list items
        db = Database()
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM inventory;")
            rows = cursor.fetchall()
            for row in rows:
                # yield returns iterable handle of this loop
                yield {"id": int(row[0]), "name": str(row[1]), "qty": int(row[2])}

    ''' 
        this is just an example for 'flash' usage
        in practical usage this operation would result query twice
        for 1 listing operation
    '''
    count = sum(1 for item in generate())  # count generator
    flash("Loaded {} items from database".format(count))  # show message

    # stream with context helps us to return iterable as response
    return Response(stream_with_context(stream_template("list.html", rows=generate())))


@app.route('/add', methods=("GET", "POST"))
def add_item():
    if request.method == "POST":  # add item
        item_name = request.form["item_name"]
        qty = request.form["quantity"]
        error = None
        if not item_name:
            error = "Item Name is required"
        elif not qty:
            error = "Quantity is required"

        if error is None:
            db = Database()
            with db.get_cursor() as cursor:
                cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", (item_name, qty))
            db.commit()
            return redirect(url_for("list_items"))

        flash(error)

    return render_template("add.html")  # serve page


if __name__ == '__main__':
    app.run()
