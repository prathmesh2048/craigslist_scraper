from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from .import models
# Create your views here.
# BASE_URL = 'https://pune.craigslist.org/search/sss?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    page = requests.get(f'https://www.olx.in/items/q-{search}?isSearchCall=true')
    soup = BeautifulSoup(page.content, 'html.parser')
    datas = soup.find_all('li', class_='EIR5N')
    final_postings = []
    header1_list = []
    header2_list = []
    header3_list = []
    page_img_list = []
    for data in datas:
        page0 = data.find('a', class_="fhlkh")
        page1 = data.find('div', class_='IKo3_')
        try:
            header1 = page1.find('span', class_='_2tW1I').text
        except:
            header1 = 'NOT AVAILAIBLE' # contains title
        try:
            header2 = page1.find('span', class_='_2TVI3').text
        except:
            header2 = 'NOT AVAILAIBLE' # contains description
        try:
            header3 = page1.find('span', class_='_89yzn').text  # contains prices
        except:
            header3 = "NOT AVAILABLE"
        page_img = data.find('a').find('img')['src']
        header1_list.append(header1)
        header2_list.append(header2)
        header3_list.append(header3)
        page_img_list.append(page_img)
        final_postings.append((header1, header2, header3, page_img))
    print(header3_list)
    stuff_for_frontend = {
         'search': search,
         'final_postings': final_postings
        # 'header1_list': header1_list,
        # 'header2_list': header2_list,
        # 'header3_list': header3_list,
        # 'page_img_list': page_img_list,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

