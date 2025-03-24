from config.config import module_error_message

from bs4 import BeautifulSoup

def GetProducts(page_source):
    products_list = []

    html = page_source
    soup = BeautifulSoup(html, 'html.parser')

    lifestyle = 1
    # Mosaic view for lifestyle product
    div_all_products = soup.find("div", {"id": "mosaic_with_owner"})
    # List view for all other product
    if not div_all_products:
        div_all_products = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['mb-lg'])
        lifestyle = 0
    if not div_all_products:
        print("Not found div_all_products")
        return None  
    
    product_ul_class = div_all_products.find(lambda tag: tag.name == "ul" and tag.get('data-test-id') == 'listing-column')
    list_item = product_ul_class.find_all("li")
    for item in list_item:
        product = {}
        
        article = item.find("a", {"class": "absolute inset-0"})

        if (article != None):
            #getting url

            url = "https://www.leboncoin.fr" + article.get('href')
            id = int(url.split("/")[-1].split(".")[0])
            
            product['url'] = url
            product['id'] = id

            #title
            title_span = article.find("span", {"class", "hidden"})
            if title_span:
                product_title = title_span.text.strip()
                if product_title:
                    product['title'] = product_title
            
            #price
            p_price = item.find("p", {"data-test-id": "price"})
            if p_price:
                product_price = p_price.find("span", {"class": ""})
                if product_price:
                    product['price'] = product_price.text.strip()
            
            # Image
            # Find the second image in product_a_class (you can complete this part)
            # For example, to find the second image source:
            image = item.find("img", {"alt": ""})
            product['img_src'] = image.get("src") if image else None

            # Marque only if lifestyle view
            if lifestyle == 1:
                marque = item.find("div", {"data-test-id": "ad-params-light"})
                product['marque'] = marque.text
            else:
                product['marque'] = None
            
            # Ville et date
            div_date_ville = item.find("div", {"class": "flex h-full flex-col justify-between"})
            if div_date_ville:
                span_date_ville = div_date_ville.find_all("span")
                p_date_ville = div_date_ville.find_all("p")
                span_date_ville_string = []
                if span_date_ville != None:
                    for span in span_date_ville:
                        if span != None:
                            span_date_ville_string.append(span.text.strip())
                if p_date_ville != None:
                    for p in p_date_ville:
                        if p != None:
                            span_date_ville_string.append(p.text.strip())
                
                if any(s in s in ["Livraison", "Achat en cours"] for s in span_date_ville_string):
                    ville = span_date_ville_string[5]
                    date = span_date_ville_string[6]
                    etat = span_date_ville_string[1]
                else:
                    ville = span_date_ville_string[4]
                    date = span_date_ville_string[5]
                    etat = None
                    
                product['ville'] = ville if ville else "non spécifié"
                product['date'] = date if date else "non spécifié"

                if etat:
                    product['etat'] = etat
                else:
                    product['etat'] = "Main propre"
            
            # No more authors shown in search pages
            # #author
            # author = item.find("div", {"class": "mb-md flex items-center gap-sm"})
            # author = author.find("span")
            # product['author'] = author.text if author else None

            products_list.append(product)
    return products_list

if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)