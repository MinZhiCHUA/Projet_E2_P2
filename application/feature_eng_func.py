import json

f = open('application/param_for_norm.json')
param_norm = json.load(f)

def get_garage_score(Garage_Type='None', Garage_Finish='None', Garage_Cars=0, Garage_Area=0):


    if Garage_Type == 'BuiltIn': 
        score_garage_type = 1
    elif Garage_Type == '2Types': 
        score_garage_type = 0.5
    elif Garage_Type == 'Attchd': 
        score_garage_type = 0.75
    elif Garage_Type == 'Basment': 
        score_garage_type = 0.5
    else:
        score_garage_type = 0

    if Garage_Finish == 'Fin': 
        score_garage_finish = 1
    elif Garage_Type == 'RFn': 
        score_garage_finish = 0.5
    else:
        score_garage_finish = 0

    score_garage_cars = (Garage_Cars - param_norm['garage_car_min']) /\
                            (param_norm['garage_car_max'] - param_norm['garage_car_min'])

    score_garage_area = (Garage_Area - param_norm['garage_area_min']) /\
                            (param_norm['garage_area_max'] - param_norm['garage_area_min'])

    score_garage = score_garage_type +\
                    score_garage_finish +\
                    score_garage_cars +\
                    40 * score_garage_area

    score_garage = (score_garage - param_norm['score_garage_min']) /\
                (param_norm['score_garage_max'] - param_norm['score_garage_min'])

    score_garage = score_garage * 100 // 10

    return score_garage

def get_basement_score(Bsmt_Qual='None',Bsmt_Exposure='None', BsmtFin_Type_1='NA', Bsmt_Full_Bath=0, Bsmt_Half_Bath=0, Total_Bsmt_SF=0):

    if Bsmt_Qual == 'Ex': 
        score_bsmt_qual = 1
    elif Bsmt_Qual == 'Gd': 
        score_bsmt_qual = 0.5
    else:
        score_bsmt_qual = 0

    if Bsmt_Exposure == 'Gd': 
        score_bsmt_expose = 1
    elif Bsmt_Exposure == 'Av': 
        score_bsmt_expose = 0.6
    elif Bsmt_Exposure == 'Mn': 
        score_bsmt_expose = 0.3
    elif Bsmt_Exposure == 'No': 
        score_bsmt_expose = 0.3
    else:
        score_bsmt_expose = 0

    if BsmtFin_Type_1 == 'GLQ': 
        score_bsmtfin_type1 = 1
    elif BsmtFin_Type_1 == 'NA': 
        score_bsmtfin_type1 = 0
    else:
        score_bsmtfin_type1 = 0.5

    if Bsmt_Full_Bath > 0: 
        score_bath = 1
    elif Bsmt_Half_Bath  > 0:  
        score_bath = 1
    else:
        score_bath = 0

    score_basement_sf = (Total_Bsmt_SF - param_norm['total_bsmt_sf_min']) /\
                        (param_norm['total_bsmt_sf_max'] - param_norm['total_bsmt_sf_min'])

    score_basement = score_bsmt_qual + score_bsmtfin_type1 +\
                    score_bsmtfin_type1 + score_bsmtfin_type1 +\
                    20 * score_basement_sf

    score_basement = (score_basement - param_norm['score_basement_min']) /\
                    (param_norm['score_basement_max'] - param_norm['score_basement_min'])

    score_basement= score_basement * 100 // 10

    return score_basement

def get_feature_score(Fireplaces=0, Wood_Deck_SF=0, Open_Porch_SF=0, Heating_QC='None', Paved_Drive='N', Misc_Val=0, Central_Air='N'):

    if Fireplaces > 0: 
        have_fireplace = 1
    else:
        have_fireplace = 0

    if Wood_Deck_SF > 0: 
        have_wood_deck = 1
    else:
        have_wood_deck = 0

    if Open_Porch_SF > 0: 
        have_open_porch = 1
    else:
        have_open_porch = 0

    if Heating_QC == 'Ex': 
        have_good_heating = 1
    elif Heating_QC == 'Gd': 
        have_good_heating = 0.75
    elif Heating_QC == 'TA': 
        have_good_heating = 0.5
    elif Heating_QC == 'Fa': 
        have_good_heating = 0.5
    else:
        have_good_heating = 0

    if Paved_Drive == 'Y': 
        have_paved_drive = 1
    elif Paved_Drive == 'P': 
        have_paved_drive = 0.5
    else:
        have_paved_drive = 0

    if Misc_Val > 0: 
        have_misc_val = 1
    else:
        have_misc_val = 0

    if Central_Air == 'Y': 
        have_central_air = 1
    else:
        have_central_air = 0

    score_feature = (have_fireplace +\
        have_wood_deck + have_open_porch +\
        have_good_heating + have_paved_drive +\
        have_central_air) / 6

    score_feature = (score_feature - param_norm['score_feature_min']) /\
                    (param_norm['score_feature_max'] - param_norm['score_feature_min'])

    score_feature = score_feature * 100 // 10

    return score_feature
    
def get_age_score(Year_Built=2022):
    
    score_age = Year_Built - 2022

    score_age = (score_age - param_norm['score_age_min']) /\
                    (param_norm['score_age_max'] - param_norm['score_age_min'])

    score_age = abs(score_age * 100 // 10)

    return score_age

def get_condition_score(Exter_Qual='NA', Bsmt_Qual='NA', Kitchen_Qual='NA', Overall_Qual=5):

    if Exter_Qual == 'Ex': 
        external_quality = 1
    elif Exter_Qual == 'Gd': 
        external_quality = 0.5
    else:
        external_quality = 0

    if Bsmt_Qual == 'Ex': 
        basement_quality = 1
    elif Bsmt_Qual == 'Gd': 
        basement_quality = 0.5
    else:
        basement_quality = 0

    if Kitchen_Qual == 'Ex': 
        kitchen_quality = 1
    elif Kitchen_Qual == 'Gd': 
        kitchen_quality = 0.5
    else:
        kitchen_quality = 0

    score_condition= (Overall_Qual +\
                        external_quality +\
                        basement_quality +\
                        kitchen_quality) / 4

    score_condition = (score_condition - param_norm['score_condition_min']) /\
                    (param_norm['score_condition_max'] - param_norm['score_condition_min'])


    score_condition = score_condition * 100 // 10

    return score_condition

def get_neighborhood_score(Neighborhood='Veenker'):

    return Neighborhood

def get_external_score(Mas_Vnr_Type='None', Foundation='NA'):


    if Mas_Vnr_Type == 'None': 
        mas_vnr_type_score = 0.3
    elif Mas_Vnr_Type == 'BrkCmn': 
        mas_vnr_type_score = 0.3
    elif Mas_Vnr_Type == 'BrkFace': 
        mas_vnr_type_score = 0.6
    elif Mas_Vnr_Type == 'Stone': 
        mas_vnr_type_score = 1
    else:
        mas_vnr_type_score = 0

    if Foundation == 'BrkTil': 
        foundation_score = 0.25
    elif Foundation == 'CBlock': 
        foundation_score = 0.25
    elif Foundation == 'BrkFace': 
        foundation_score = 0.5
    elif Foundation == 'Wood': 
        foundation_score = 0.5
    elif Foundation == 'PConc': 
        foundation_score = 1
    else:
        foundation_score = 0

    score_combine = foundation_score + mas_vnr_type_score

    score_combine_norm = (score_combine - param_norm['score_combine_min']) /\
                    (param_norm['score_combine_max'] - param_norm['score_combine_min'])

    score_external = score_combine_norm

    score_external = (score_external - param_norm['score_external_min']) /\
                    (param_norm['score_external_max'] - param_norm['score_external_min'])

    score_external = score_external* 100 // 10

    return score_external

def get_ext_area_score(Lot_Area=5000, Mas_Vnr_Area=0, Open_Porch_SF=0, Wood_Deck_SF=0, Pool_Area=0):


    total_ext_area = Lot_Area+\
                    Mas_Vnr_Area +\
                    Open_Porch_SF +\
                    Wood_Deck_SF +\
                    Pool_Area
    total_ext_area_norm = (total_ext_area -\
                    param_norm['total_ext_area_norm_min'] ) /\
                    (param_norm['total_ext_area_norm_max'] - param_norm['total_ext_area_norm_min'])

    score_ext_area= total_ext_area_norm
                    
    return score_ext_area

def get_internal_score(score_internal= 350):

        score_internal = (score_internal - param_norm['gr_liv_area_min']) /\
                                (param_norm['gr_liv_area_max'] - param_norm['gr_liv_area_min'])

        return score_internal

def get_room_score(Half_Bath=0, Full_Bath=1, TotRms_AbvGrd=2):

    Total_Bath = 0.5 * Half_Bath + Full_Bath

    total_room_tmp = (TotRms_AbvGrd - param_norm['totrms_abvgrd_min']) /\
                            (param_norm['totrms_abvgrd_max'] - param_norm['totrms_abvgrd_min'])

    total_bath_tmp = (Total_Bath - param_norm['Total_Bath_min']) /\
                            (param_norm['Total_Bath_max'] - param_norm['Total_Bath_min'])     

    score_room_tmp = 3 * total_room_tmp + total_bath_tmp

    score_room_tmp = (score_room_tmp - param_norm['score_room_tmp_min']) /\
                            (param_norm['score_room_tmp_max'] - param_norm['score_room_tmp_min'])

    score_room = score_room_tmp * 100 // 10

    return score_room