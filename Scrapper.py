import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_rating(review):
    rating = review.find('span', class_ = "a-icon-alt").text
    rating = rating.split("out")[0].strip()
    rating = float(rating)
    return rating

def get_star(rating):
    rating = int(rating)
    star = "⭐" * rating
    return star

def get_variant(product, review):
    variant = review.find('span', {'data-hook': 'format-strip-linkless'})
    # Filtering the 'None' type data..
    try:
        if variant != None:
            variant = variant.text
        elif variant == None:
            variant = product + " (Unavailable, Generated_from_Title)"
    except:
        variant = "Unavaliable"
    return variant

def get_vote(review):
    vote = review.find('span', class_ = "a-size-base a-color-tertiary cr-vote-text")
    if vote != None:
        vote = vote.text
    else:
        vote = "None"
    return vote

def get_review_images(review):
    img_links = []
    raw_img_links = []
    if review.find('div', class_ = "review-image-tile-section") == None:
        img_links.append("Not Available")
    else:
        raw_img_links = review.find_all('img', alt = "Customer image")
    for individual_links in raw_img_links:
        media_link = individual_links.get('data-src')
        if media_link != None:
            img_links.append(media_link)
    return ', '.join(img_links)

def scrape(url):
    soup = get_response(url)
    product = soup.find('span', class_ = "a-size-large product-title-word-break").text.strip()
    print("\t\t\tP R O D U C T     :   ", product)
    fetched_reviews = []
    for review in soup.find_all('div', {'class': 'review'}):
        customer_name = review.find('span', class_ = "a-profile-name").text
        rating = get_rating(review)
        date = review.find('span', class_ = "a-size-base a-color-secondary review-date").text
        comment = review.find('a', class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").text.strip()
        body = review.find('div', class_ = "a-expander-content reviewText review-text-content a-expander-partial-collapse-content").text.strip()
        variant = get_variant(product, review)
        vote = get_vote(review)
        img_links = get_review_images(review)

        #['Customer Name', 'Variant', 'Rating(Out of 5)', 'Rating', 'Date of Review', 'Comment', 'Review', 'Images attatched by Customer', 'Votes on the Review']
        fetched_reviews.append([customer_name, variant, rating, get_star(rating), date, comment, body, img_links, vote])

        # Printing the details..
        print("\n\n\n\nNAME      :   ", customer_name)
        print("VARIANT   :   ", variant)
        print("RATING    :   ", rating)
        print("DATE      :   ", date.encode("utf-8"))       # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("COMMENT   :   ", comment.encode("utf-8"))    # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("BODY      :   ", body.encode("utf-8"))       # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("IMAGES    :   ", img_links)
        print("VOTE      :   ", vote)

    # Save to CSV..
    save_to_csv(product, fetched_reviews)
    
def save_to_csv(product, fetched_reviews):
    page_visit_details = datetime.now().strftime("%B %d %Y, %H-%M-%S")
    # Applying this filter because the file cannot be saved into the system with these special characters in file name..
    replace_characters = [':', '\\', '|', '/', '*', '?', '"', '<', '>']
    for char in replace_characters:
        if char in product:
            product = product.replace(char, "")
    # Too long name seems to be an issue while adding these files in github so set the limit of the filename to 60 characters..
    product = product[0:60]
    file_path = product + '(Product Page, Visited on ' + str(page_visit_details) + ').csv'
    # write the information to a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Customer Name', 'Variant', 'Rating(Out of 5)', 'Rating', 'Date of Review', 'Comment', 'Review', 'Images attatched by Customer', 'Votes on the Review'])
        csv_writer.writerows(fetched_reviews)
    
    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)
    # Print the absolute path
    print("\n\n___________________________________________________________________________________________________________________________________")
    print("-----------------------------------------------------------------------------------------------------------------------------------\n\n")
    print(f'The absolute path of the CSV file is: {absolute_path}\nVisited on {page_visit_details}')

def save_to_json():
    pass

#url = 'https://p-nt-www-amazon-in-kalias.amazon.in/New-Apple-iPhone-12-128GB/dp/B08L5VJWCV?th=1'
#url = 'https://p-nt-www-amazon-in-kalias.amazon.in/dp/B0BDJH6GL8?th=1'
#url = 'https://p-nt-www-amazon-in-kalias.amazon.in/Xiaomi-Storage-Snapdragon-Flagship-Cameras/dp/B09XBCCQJT?th=1'
url = 'https://p-nt-www-amazon-in-kalias.amazon.in/dp/B00NXEINKE/ref=sspa_dk_detail_1?pd_rd_i=B00NXEINKE&pd_rd_w=TJ9mM&content-id=amzn1.sym.6c74ac28-0eba-4461-ba39-7b1bc57f1b6e&pf_rd_p=6c74ac28-0eba-4461-ba39-7b1bc57f1b6e&pf_rd_r=PWTRNSS1TADH4GY2SYR0&pd_rd_wg=N93dj&pd_rd_r=4fd17522-0fb1-4d8d-ade8-6764077133af&s=electronics&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy&th=1'

if __name__ == "__main__":
    scrape(url)