// document.getElementsByClassName('product-price')[0].innerText;
// document.getElementsByClassName('product-price')[0].getAttribute('price');
function filterBrand() {
    let brands = document.getElementsByClassName('bc-item');
    let brands_products = document.getElementsByClassName('brand-name');
    let brands_names = [];

    for (let index = 0; index < brands.length; index++) {
        const element = brands[index];
        let is_checked = document.getElementById('bc-' + element.innerText).checked;
        if (is_checked === true) {
            brands_names.push(element.innerText);
        }
    }

    if (brands_names.length === 0) {}
    else {
        for (let product_index = 0; product_index < brands_products.length; product_index++) {
            let flag = false;
            for (let brand_index = 0; brand_index < brands_names.length; brand_index++) {
                if (brands_products[product_index].innerText === brands_names[brand_index].toUpperCase()) {
                    flag = true;
                    break;
                }
            }
            let el = document.getElementById('product-' + (product_index + 1));
            if (flag == false) {
                el.style.display = "none";
            }
        }
    }
}


function filterPrice() {
    let max = parseFloat(document.getElementById('maxamount').value.slice(1));
    let min = parseFloat(document.getElementById('minamount').value.slice(1));

    let array = document.getElementsByClassName('product-price');

    for (let index = 0; index < array.length; index++) {
        let value = document.getElementsByClassName('product-price')[index].getAttribute('price');
        let el = document.getElementById('product-' + (index + 1));

        if (value > max || value < min) {
            el.style.display = "none";
        }
        else {
            el.style.display = "";
        }
    }
}

function addUrlParameters(name, value) {
    const query = window.location.search.substring(1);
    let url;
    if (query.length === 0) {
        url = new URLSearchParams();
    } 
    else {
        url = new URLSearchParams(query);
    }

    if (url.get('gender') !== null && name === 'gender') {
        url.set('gender', value);
    }
    else if (url.get('tags') !== null && name === 'tags') {
        url.set('tags', value);
    }
    else {
        url.append(name, value);
    }

    window.location.replace("catalog?" + url.toString());
}