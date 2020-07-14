from random import seed, randint

product_name_words = ['T-shirt', 'Dress', 'Jeans', 'Hoodie', 'Socks',\
                    'Long Sleeves', 'Short', 'Fashionable', 'Modern', 'New',\
                    'Life', 'Nature', 'Tracksuit', 'Polo', 'Anzug',\
                    'Blue', 'Grey', 'Red', 'Green', 'Orange']

brands = ['Nike', 'Addidas', 'Puma', 'Under Armor', 'Gucci', 'Versachi', 'Louis Vitton', 'Supreme',\
        'Addidas', 'O bag', 'Cassio', 'Nike', 'Addidas', 'Nike', 'Reebok']

tags = ['Clothes', 'Long', 'Short', 'Summer 2019', 'Winter 2019', 'Designer', 'Geeky', 'Sports',\
        'Fitness', 'Running', 'Basketball', 'Football', 'Volleyball', 'Hockey', 'Others']

def generate_prodcut_name(words):
    seed(randint(0, 10000))
    index = randint(0, 19 - len(words))
    res = list(set(product_name_words)^set(words))
    words.append(res[index])

    if len(words) >= 3:
        name = str(words[0] + ' ' + words[1] + ' ' + words[2])
        words.clear()
        return name

    else:
        return generate_prodcut_name(words)


f = open("data.txt", "w+")
empty = []

#inserting the brands
for i in range (15):
    f.write('INSERT INTO brands (brandname) VALUES (' + '\'' + str(brands[i]) + '\'' + ');\n')

#insertign genders
f.write('\n')
f.write('INSERT INTO genders(gender) VALUES(\'Men\');\n')
f.write('INSERT INTO genders(gender) VALUES(\'Women\');\n')
f.write('INSERT INTO genders(gender) VALUES(\'Unisex\');\n')


#inserting the products
f.write('\n')
for i in range (10000):
    f.write('INSERT INTO products(name, brand_id, price, gender_id, overall_raiting, description)VALUES (' + '\'' + str(generate_prodcut_name(empty)) + '\', ' + str(randint(1, 15)) + ', '+ str(randint(1, 1000)) + ', ' + str(randint(1, 3)) + ', ' + str(0) + ', ' +'\'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmodtempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiatnulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officiadeserunt mollit anim id est laborum.\');\n')


#inserting tags
f.write('\n')
for i in range (15):
    f.write('INSERT INTO tags(tag) VALUES (' + '\'' + str(tags[i]) + '\'' + ');\n')

#givving products at least 1 tag
f.write('\n')
for i in range (10000):
    f.write('INSERT INTO products_tags(product_id, tag_id) VALUES (' + str(i+1) + ', ' + str(randint(1, 15)) + ');\n')


#insering the statuses
f.write('\n')
f.write('INSERT INTO status(status) VALUES(\'Processing\');\n')
f.write('INSERT INTO status(status) VALUES(\'Accepted\');\n')
f.write('INSERT INTO status(status) VALUES(\'Confirmed\');\n')
f.write('INSERT INTO status(status) VALUES(\'Sent\');\n')
f.write('INSERT INTO status(status) VALUES(\'Finished\');\n')

#inserting payment method
f.write('\n')
f.write('INSERT INTO payment_methods(payment_method) VALUES(\'Pay at delivery\');\n')

#inserting orders
f.write('\n')
for i in range (1000):
    f.write('INSERT INTO orders(user_id, status_id, date, payment_method_id, is_paid, address_id) VALUES(' + str(1) + ', ' +  str(randint(1, 5)) + ', ' + '\'' + str(randint(1, 30)) + '/' + str(randint(1, 12)) + '/' + str(2019) + '\'' + ', ' + str(1) + ', ' + '\'' + 'false' + '\', ' + str(1) + ');\n')


#inserting products in the orders
f.write('\n')
for i in range (1000):
    f.write('INSERT INTO ordered_products(order_id, product_id, product_price, product_quantity) VALUES(' + str(i+1) + ', ' + str(randint(1, 10000)) + ', ' + str(100) + ', ' + str(1) + ');\n')


f.close()