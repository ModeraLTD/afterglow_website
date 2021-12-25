import os

PRODUCT_TEMPLATE =      """<div class="product">
                            <img src={imgUrl}>
                            <div class="details">
                                <h3>{serviceName}</h3>
                                <div class="pricetime">
                                    <h4>{price}</h4>
                                    <h4>{time}</h4>
                                </div>
                                <div class="actions">
                                    <button id={prodID} onclick="toggleBasket('{prodID}');" class="{buttonClass}">{buttonText}</button>
                                    <button onclick="help('{serviceName}');" class="help">?</button>
                                </div>
                            </div>
                        </div>"""

CATEGORY_TEMPLATE =    """<div class="category" id="{cat}">
                            <div class="products">
                                {products}
                            </div>
                        </div>"""

def formatProduct(dbObj, request):
    inbasket = dbObj.prodID in request.session['basket']

    rv = PRODUCT_TEMPLATE.format(
        imgUrl = getImg(dbObj),
        serviceName = dbObj.name,
        price = dbObj.price,
        prodID = dbObj.prodID,
        time = formatTime(dbObj.time),
        buttonClass = "addToBasket added" if inbasket else "addToBasket",
        buttonText = "Remove from basket" if inbasket else "Add to basket",
    )

    return {
        "html": rv,
        "category": dbObj.category,
        "name": dbObj.name,
    }

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

def formatTime(time):
    if time >= 60:
        hr = time // 60
        min = time % 60
        if min == 0:
            return f'{hr} hr'  
        else: 
            return f'{hr} hr {min} min'
    else:
        return f'{time} min'
