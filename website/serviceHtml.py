import os
import random
import string

CHARSET = list(string.ascii_lowercase)

PRODUCT_TEMPLATE =      """<div class="product">
                            <img src={imgUrl}>
                            <div class="details">
                                <h3>{serviceName}</h3>
                                <div class="pricetime">
                                    <h4>{price}</h4>
                                    <h4>{length}</h4>
                                </div>
                                <div class="actions">
                                    <button id={prodID} onclick="addToBasket('{serviceName}', '{prodID}');" class="addToBasket">Add to basket</button>
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
        prodID = genProdID(),
    )

    return {
        "html": rv,
        "category": dbObj.category,
        "name": dbObj.name,
    }

def genProdID():
    return ''.join([random.choice(CHARSET) for i in range(16)])

def groupProds(prods):
    cats = {
        "SKIN": "",
        "HEALTH": "",
        "NON_INV": "",
        "APP": "",
    }

    sortedProds = [(i['name'], i['category'], i['html']) for i in prods]
    sortedProds.sort()

    for prod in sortedProds:
        cats[prod[1]] += prod[2] + "\n\n"
    
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