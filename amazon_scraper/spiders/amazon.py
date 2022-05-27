import os
import scrapy
import js2xml
from urllib.parse import urlencode
from amazon_scraper.items import AmazonProduct
from dotenv import load_dotenv
load_dotenv()

pages = [ #'https://www.amazon.com/Bounty-Quick-Size-Towels-Family-Regular/dp/B07MHJFRBJ/?_encoding=UTF8&pd_rd_w=vAvXs&pf_rd_p=68e05c0e-c711-4878-b092-eedd8a648e16&pf_rd_r=H78GYXS3MKQ390JB6WW9&pd_rd_r=d89a760f-bb44-45e7-8394-3496e585edea&pd_rd_wg=UzJat&ref_=pd_gw_dtech_gw_qda_april_de_xcat_2',
        # 'https://www.amazon.com/dp/B07KFPMKKL/ref=s9_acsd_al_bw_c2_x_5_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=Z2Z6JCT498KXTCXT9GYB&pf_rd_t=101&pf_rd_p=044e545f-3f38-4112-a6fb-50abb642850a&pf_rd_i=23874220011',
        'https://www.amazon.com/Yueshico-Stainless-Watermelon-Vegetable-Kitchen/dp/B07MYXN2L9/ref=lp_23874220011_1_4',
        # 'https://www.amazon.com/dp/B09Q556SZL/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B09Q556SZL&pd_rd_w=UU0pP&content-id=amzn1.sym.3be1c5b9-5b41-4830-a902-fa8556c19eb5&pf_rd_p=3be1c5b9-5b41-4830-a902-fa8556c19eb5&pf_rd_r=A609V4626RDM0YB9DMX9&pd_rd_wg=3cDPC&pd_rd_r=2cecd61f-3668-496d-b964-d2477a179abd&s=kitchen',
        ]

def get_url(url):
    payload = {'api_key': os.environ.get('PROXY_API_KEY'), 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']



    def start_requests(self):
        for page in pages:
            yield scrapy.Request(url = get_url(page), callback=self.parse)


    def parse(self, response):
        amazon_product = AmazonProduct()
        amazon_product['asin'] = response.xpath('//*[@id="ASIN"]').attrib['value']
        amazon_product['item_name'] = response.xpath('//*[@id="productTitle"]//text()').get().strip()
        amazon_product['bullet_point'] = response.css('#feature-bullets').css('.a-list-item::text').getall()
        js = response.xpath("//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()").extract_first()
        xml = js2xml.parse(js)                                                  
        selector = scrapy.Selector(root=xml)                                   
        image_array = selector.xpath('//property[@name="colorImages"]//property[@name="hiRes"]/string/text()').extract()
        amazon_product['images'] = image_array
        amazon_product['image_count'] = len(image_array)

        yield amazon_product
