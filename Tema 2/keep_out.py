import re

rpath = ''

if re.match('^/users', rpath):
    # /users
    if re.match('^/users/?$', rpath, re.IGNORECASE):
        print("all users")
    else:
        user_search = re.search('^/users/([a-z0-9]+)/?$', rpath, re.IGNORECASE)
        if user_search:
            user_id = user_search.group(1)
            print("one user", user_id)
        else:
            user_search = re.search('^/users/([a-z0-9]+)/orders/?$', rpath, re.IGNORECASE)
            if user_search:
                user_id = user_search.group(1)
                print("all orders", user_id)
            else:
                order_search = re.search('^/users/([a-z0-9]+)/orders/([a-z0-9]+)/?$', rpath, re.IGNORECASE)
                if order_search:
                    user_id = order_search.group(1)
                    order_id = order_search.group(2)
                    print("id order", user_id, order_id)
                else:
                    order_search = re.match('^/users/([a-z0-9]+)/orders/([a-z0-9]+)/products/?$', rpath,
                                            re.IGNORECASE)
                    if order_search:
                        user_id = order_search.group(1)
                        order_id = order_search.group(2)
                        print("all products", user_id, order_id)
                    else:
                        product_search = re.search(
                            '^/users/([a-z0-9]+)/orders/([a-z0-9]+)/products/([a-z0-9]+)/?$',
                            rpath, re.IGNORECASE)
                        if product_search:
                            user_id = product_search.group(1)
                            order_id = product_search.group(2)
                            product_id = product_search.group(3)
                            print("id product", user_id, order_id, product_id)
                        else:
                            print("bad")
