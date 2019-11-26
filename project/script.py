import json
import requests

name = []
address = []
image_url = []
with open('/home/yashwant/Documents/hotel/project/data.json') as f:
    data = json.load(f)
    hotel_info = {}
    for i,x in enumerate(data['hotels']):
        hotel = []
        name.append(x['name']['en'])
        address.append(x['address']['en'])
        url = []
        for y in x['photos']:
            url.append(y['url'])
        image_url.append(url)


print(name[0])
        # hotel.append(name)
        # print(hotel)
        # print('\n')
        # hotel.append(address)
        # print(hotel)
        # hotel.append(url)
        # print(hotel)
        # print('\n')
        # hotel_info[i] = hotel
        # print(hotel_info[i],end='\n')\

    # for x in name:
        # print(x,end='\n')
# count = 0
# for x in image_url:
#     print(x,end='\n')
#     count = count + 1

# print(count)

# image_responses = {}
# i = 0
# for each in image_url:
#     image = []
#     j = 0 
#     for x in each:
#         image[j] = requests.get(each)
#         j = j+ 1
#     image_responses[i] = image
#     i = i + 1






