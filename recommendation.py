from project.model import Facilities
from user_list import L as user_list
import numpy as np

def classify(x):
    if x == 1 :
        return 0
    if x == 2 :
        return 0.4
    if x == 3 : 
        return 0.8
    if x == 4 :
        return 1

def score_matrix_func():
    x = Facilities.query.all()
    f_list = [] # facility list
    for x in x :
        facilities = []
        if x.gym is True:
            facilities.append(1)
        else:
            facilities.append(0)

        if x.FoodBeverages is True:
            facilities.append(1)
        else:
            facilities.append(0)

        if x.Parking is True:
            facilities.append(1) 
        else:
            facilities.append(0)

        if x.Tv is True:
            facilities.append(1) 
        else:
            facilities.append(0)
        
        if x.wifi is True:
            facilities.append(1) 
        else:
            facilities.append(0)
        
        f_list.append(facilities)  
        # print(f_list)
    

    score_matrix = np.zeros((len(user_list),len(f_list)))
    # print(score_matrix.shape)
    for i in range(len(user_list)):
        a = classify(user_list[i][0])
        b = classify(user_list[i][1])
        c = classify(user_list[i][2])
        d = classify(user_list[i][3])
        for j in range(len(f_list)):
            score_matrix[i][j] = (a* f_list[j][0] + b*f_list[j][1] + c*f_list[j][2] + d*f_list[j][3]) / (a + b + c + d + 1e-9)

           
    # print(score_matrix.shape)
    similarity_hotel = score_matrix.T.dot(score_matrix) + 1e-9
    # print(similarity_hotel.shape)
    norms = np.array([np.sqrt(np.diagonal(similarity_hotel))])
    similarity_hotel = similarity_hotel/(norms*norms.T)
    return similarity_hotel

similarity_hotel = score_matrix_func()

# a = np.zeros(similarity_hotel.shape)[0]
# print(a.shape)
# similarity_hotel[1][1]
# print(similarity_hotel.shape)
# score_matrix_func()