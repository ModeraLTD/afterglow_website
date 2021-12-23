import os

PRODUCT_TEMPLATE =      """<div class="product">
                            <img src={imgUrl}>
                            <div class="details">
                                <h3>{serviceName}</h3>
                                <div class="pricetime">
                                    <h4>{price}</h4>
                                    <h4>{length}</h4>
                                </div>
                                <div class="actions">
                                    <button onclick="addToBasket('{serviceName}');" class="addToBasket">Add to basket</button>
                                    <button onclick="help('{serviceName}');" class="help">?</button>
                                </div>
                            </div>
                        </div>"""

CATEGORY_TEMPLATE =    """<div class="category" id="{cat}">
                            <div class="products">
                                {products}
                            </div>
                        </div>"""

def formatProduct(dbObj):
    rv = PRODUCT_TEMPLATE.format(
        imgUrl = getImg(dbObj),
        serviceName = dbObj.name,
        price = dbObj.price,
        length = formatLength(dbObj.length),
    )

    return rv, dbObj.category

def groupProds(prods):
    cats = {
        "SKIN": "",
        "HEALTH": "",
        "NON_INV": "",
        "APP": "",
    }

    for prod in prods:
        cats[prod[1]] += prod[0] + "\n\n"
    
    return cats

def getImg(dbObj):
    if os.path.isfile(f"css/images/{dbObj.name}.png"):
        return "{% static 'css/images/" + dbObj.name + ".png' %}"
    elif len(dbObj.imgUrl) > 0:
        return f"'{dbObj.imgUrl}'"
    else:
        return "'https://via.placeholder.com/100'"

def formatLength(length):
    s = ""

    if length.hour > 0:
        s += f"{length.hour}h"
    
    if length.minute > 0:
        s += f"{length.minute}"
    
    return s