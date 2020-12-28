# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:12:54 2020

@author: richa
"""

#Note, currently, empty rows will throw off this script, make sure to to get rid of them before running
#https://www.excel-easy.com/examples/delete-blank-rows.html

import pandas as pd
import numpy as np
import math

global myFile
global myKML
global spaFiles
global conFiles
global myDB
global spaDB
global conDB
global KeepInput
global maxRange

#Settings
#your dataset file name goes below
myFile = 'Datasets - NGAN.xlsx'
#your kml file name goes below
myKML = 'targets.kml'

#spaFiles_BS = ['Big South Spatial 1- Blue .csv','Big South Spatial 2- Blue .csv','Big South Spatial 3- Blue .csv','Big South Spatial 4- Blue .csv', 'Atlanta Spatial 1 - Blue.csv','Atlanta Spatial 2 - Blue.csv','Atlanta Spatial 3- Blue.csv']
#conFiles_BS = ['Big South Continuity 1 - Red.csv','Big South Continuity 2 - Red.csv','Big South Continuity 3 - Red.csv','Big South Continuity 4 - Red.csv','Big South Continuity 5 - Red.csv','Big South Continuity 6 - Red.csv','Big South Continuity 7 - Red.csv','Big South Continuity 8 - Red.csv']
#spaFiles_KS = ['Keystone Spatial 1 - Blue.csv','Keystone Spatial 2 - Blue.csv']
#conFiles_KS = ['Keystone Continuity 1 - Red v2.xlsx','Keystone Continuity 2 - Red v2.xlsx']
#spaFiles_TW = ['Twin Cities Spatial 1 - Blue.csv','Twin Cities Spatial  2- Blue.csv','Twin Cities KS MO Spacial - Blue.csv']
#conFiles_TW = ['Twin Cities Continuity - Red.xlsx','Twin Cities Continuity - Red 2.xlsx']
spaFiles_MW = ['MtnWest Spatial 1 - Blue.csv','MtnWest Spatial 2 - Blue.csv','MtnWest Spatial 3 - Blue.csv','MtnWest Spatial 4 - Blue.csv']
conFiles_MW = ['MtnWest Continuity 1 - Red.xlsx','MtnWest Continuity 2 - Red.xlsx','MtnWest Continuity 3 - Red.xlsx','MtnWest Continuity 4 - Red.xlsx']

spaFiles = spaFiles_MW
conFiles = conFiles_MW

myDB =  pd.read_excel(myFile, converters={'PS_NETWORK_KEY-Spatial':str,'POWER_SUPPLY_NAME':str,'Continuity PS Name':str,'Mac Address':str,'Good Latitude':float,'Good Longitude':float,'Status':str,'Comment':str})

spaDB = [None]*len(spaFiles)
for s in range(len(spaFiles)):
    if spaFiles[s][len(spaFiles[s])-1] == 'v':
        spaDB[s] = pd.read_csv(spaFiles[s], converters={'PS_NETWORK_KEY-Spatial':str,'POWER_SUPPLY_NAME':str,'SUPPORT_ARUG':str,'ADDRESS':str,'LATITUDE':float,'LONGITUDE':float})
    if spaFiles[s][len(spaFiles[s])-1] == 'x':
        spaDB[s] = pd.read_excel(spaFiles[s], converters={'PS_NETWORK_KEY-Spatial':str,'POWER_SUPPLY_NAME':str,'SUPPORT_ARUG':str,'ADDRESS':str,'LATITUDE':float,'LONGITUDE':float})

conDB = [None]*len(conFiles)
for c in range(len(conFiles)):
    if conFiles[c][len(conFiles[c])-1] == 'v':
        conDB[c] = pd.read_csv(conFiles[c], converters={'Power Supply Name':str,'MAC Address':str,'Street Address':str,'Type':str,'Latitude':float,'Longitude':float})
    if conFiles[c][len(conFiles[c])-1] == 'x':
        conDB[c] = pd.read_excel(conFiles[c], converters={'Power Supply Name':str,'MAC Address':str,'Street Address':str,'Type':str,'Latitude':float,'Longitude':float})

KeepInput = 0

maxRange = 0.00025285



#saves min distance of each blue to any red (lengthy process, only needs to be done once)
def findClosestReds():
    for s in range(len(spaDB)):
        minIdR = np.zeros(spaDB[s].shape[0])#, dtype=int)
        minIdO = np.zeros(spaDB[s].shape[0])#, dtype=int)
        
        for c in range(len(conFiles)):
            for idR in range(conDB[c].shape[0]):
                rowR = conDB[c].iloc[idR]
                latR = rowR['Latitude']
                longR = rowR['Longitude']
    
                latB = spaDB[s]['LATITUDE']
                longB = spaDB[s]['LONGITUDE']
    
                latDiff = latB-latR
                longDiff = longB-longR
    
                dists = (latDiff*latDiff)+(longDiff*longDiff)#distance squared
    
                if idR==0 and c==0:
                    minD = dists
                    continue
    
                minIdR = np.where(dists < minD, idR, minIdR)
                minIdO = np.where(dists < minD, c, minIdO)
                minD = np.where(dists < minD, dists, minD)
    
        pairsCSV = pd.DataFrame(columns = ['Con Id','Con Ori','Distance^2'])
        pairsCSV['Con Id'] = minIdR
        pairsCSV['Con Ori'] = minIdO
        pairsCSV['Distance^2'] = minD
        pairsCSV.to_csv('closest_pairsB'+str(s)+'.csv', index=False)
    print('done')


#saves min distance of each red to any blue (lengthy process, only needs to be done once)
def findClosestBlues():
    for c in range(len(conDB)):
        minIdB = np.zeros(conDB[c].shape[0])#, dtype=int)
        minIdO = np.zeros(conDB[c].shape[0])#, dtype=int)
        
        for s in range(len(spaDB)):
            for idB in range(spaDB[s].shape[0]):
                rowB = spaDB[s].iloc[idB]
                latB = rowB['LATITUDE']
                longB = rowB['LONGITUDE']
    
                latR = conDB[c]['Latitude']
                longR = conDB[c]['Longitude']
    
                latDiff = latR-latB
                longDiff = longR-longB
    
                dists = (latDiff*latDiff)+(longDiff*longDiff)#distance squared
    
                if idB==0 and s==0:
                    minD = dists
                    continue
    
                minIdB = np.where(dists < minD, idB, minIdB)
                minIdO = np.where(dists < minD, s, minIdO)
                minD = np.where(dists < minD, dists, minD)
    
        pairsCSV = pd.DataFrame(columns = ['Spa Id','Spa Ori','Distance^2'])
        pairsCSV['Spa Id'] = minIdB
        pairsCSV['Spa Ori'] = minIdO
        pairsCSV['Distance^2'] = minD
        pairsCSV.to_csv('closest_pairsR'+str(c)+'.csv', index=False)
    print('done')


#finds current dataset in full dataset, and runs checks
def locateFromLocal():
    if 'PS_NETWORK_KEY-Spatial' in myDB.columns:
        myNames = myDB['PS_NETWORK_KEY-Spatial']
    elif 'ID' in myDB.columns:
        myNames = myDB['ID']
    idB = np.zeros(len(myNames), dtype=int)
    idBO = np.zeros(len(myNames), dtype=int)
    idR = np.zeros(len(myNames), dtype=int)
    idRO = np.zeros(len(myNames), dtype=int)
    dists = np.zeros(len(myNames), dtype=float)
    predicted = np.zeros(len(myNames), dtype=int)
    warnB = np.zeros(len(myNames), dtype=int)
    warnR = np.zeros(len(myNames), dtype=int)
    multiB = np.zeros(len(myNames), dtype=int)
    multiR = np.zeros(len(myNames), dtype=int)
    
    #find local in spa data
    for m in range(len(myNames)):
        for s in range(len(spaDB)):
            if 'PS_NETWORK_KEY-Spatial' in spaDB[s].columns:
                locID = spaDB[s].index[myNames[m] == spaDB[s]['PS_NETWORK_KEY-Spatial']]
            elif 'ID' in spaDB[s].columns:
                locID = spaDB[s].index[myNames[m] == spaDB[s]['ID']]
            if len(locID)>0:
                idB[m] = locID[0]
                idBO[m] = s
                break
    
    pairsB = [None]*len(spaFiles)         
    for s in range(len(spaFiles)):
        pairsB[s] = pd.read_csv('closest_pairsB'+str(s)+'.csv')
        
    pairsR = [None]*len(conFiles)         
    for c in range(len(conFiles)):
        pairsR[c] = pd.read_csv('closest_pairsR'+str(c)+'.csv')  
    
    #check data
    for p in range(len(idB)):
        dists[p] = pairsB[idBO[p]].at[idB[p],'Distance^2']
        
        idR[p] = pairsB[idBO[p]].at[idB[p],'Con Id']
        idRO[p] = pairsB[idBO[p]].at[idB[p],'Con Ori']
        
        idB2 = pairsR[idRO[p]].at[idR[p],'Spa Id']
        idBO2 = pairsR[idRO[p]].at[idR[p],'Spa Ori']
        
        if idB[p] == idB2 and idBO[p] == idBO2:
            predicted[p] = 1
        else:
            predicted[p] = 0
                
        found = 0
        equalDist = 0
        for i in range(len(pairsR)):
            locID = pairsR[i].index[(idB[p] == pairsR[i]['Spa Id']) & (idBO[p] == pairsR[i]['Spa Ori'])]
            #found+=len(locID)
            
            for m in locID:
                found+=1
                if abs(math.sqrt(pairsR[i].at[m,'Distance^2']) - math.sqrt(dists[p])) < 0.0001:
                    equalDist+=1
                    
            if equalDist>1:
                break
                
        if found<=1:
            warnB[p] = 0
        else:
            warnB[p] = 1
            
        if equalDist<=1:
            multiR[p] = 0
        else:
            multiR[p] = 1
            
        found = 0
        equalDist = 0
        for i in range(len(pairsB)):
            locID = pairsB[i].index[(idR[p] == pairsB[i]['Con Id']) & (idRO[p] == pairsB[i]['Con Ori'])]
            #found+=len(locID)
            
            for m in locID:
                found+=1
                if abs(math.sqrt(pairsB[i].at[m,'Distance^2']) - math.sqrt(dists[p])) < 0.0001:
                    equalDist+=1
                    
            if equalDist>1:
                break
                
                
        if found<=1:
            warnR[p] = 0
        else:
            warnR[p] = 1
        
        if equalDist<=1:
            multiB[p] = 0
        else:
            multiB[p] = 1
            
            
    localPairsCSV = pd.DataFrame(columns = ['Spa Id','Spa Ori','Con Id','Con Ori','Distance^2','Predicted','Spa Warn','Con Warn','Multi Spa','Multi Con'])
    localPairsCSV.index.name = 'Local Id'
    localPairsCSV['Spa Id'] = idB
    localPairsCSV['Spa Ori'] = idBO
    localPairsCSV['Con Id'] = idR
    localPairsCSV['Con Ori'] = idRO
    localPairsCSV['Distance^2'] = dists
    localPairsCSV['Predicted'] = predicted
    localPairsCSV['Spa Warn'] = warnB
    localPairsCSV['Con Warn'] = warnR
    localPairsCSV['Multi Spa'] = multiB
    localPairsCSV['Multi Con'] = multiR
        
    localPairsCSV.to_csv('local_closest_pairs.csv')



#generates input file from pairs file
#Note: for case input field, input the number 1 for 'No Street View' status, 2 for 'Obstructed View' status, 3 for 'Could Not Find' status, and 4 for 'See Comment' status
def generateInputFile():
    pairsCSV = pd.read_csv('local_closest_pairs.csv')
    idL = pairsCSV['Local Id']
    idB = pairsCSV['Spa Id']
    idBO = pairsCSV['Spa Ori']
    idR = pairsCSV['Con Id']
    idRO = pairsCSV['Con Ori']
    dists = pairsCSV['Distance^2']
    predicted = pairsCSV['Predicted']
    warnB = pairsCSV['Spa Warn']
    warnR = pairsCSV['Con Warn']
    multiB = pairsCSV['Multi Spa']
    multiR = pairsCSV['Multi Con']
    
    inputCSV = pd.DataFrame(columns = ['S_Latitude','S_Longitude','S_Type','C_Latitude','C_Longitude','C_Type','S_Address','C_Address',
                                       'Id_Info','IDist_Ratio','Notes','INPUT->','Case','New Lat','New Long','Comment','New Name','New Mac'])
    
    
    for i in range(len(idL)):
        inputCSV.at[i,'S_Latitude'] = spaDB[int(idBO[i])].at[idB[i],'LATITUDE']
        inputCSV.at[i,'S_Longitude'] = spaDB[int(idBO[i])].at[idB[i],'LONGITUDE']
        if 'SUPPORT_ARUG' in spaDB[int(idBO[i])].columns:
            inputCSV.at[i,'S_Type'] = spaDB[int(idBO[i])].at[idB[i],'SUPPORT_ARUG']
        inputCSV.at[i,'S_Address'] = spaDB[int(idBO[i])].at[idB[i],'ADDRESS']
        if predicted[i]:
            inputCSV.at[i,'C_Latitude'] = conDB[int(idRO[i])].at[idR[i],'Latitude']
            inputCSV.at[i,'C_Longitude'] = conDB[int(idRO[i])].at[idR[i],'Longitude']
            if 'Type' in conDB[int(idRO[i])].columns:
                inputCSV.at[i,'C_Type'] = conDB[int(idRO[i])].at[idR[i],'Type']
            elif 'Meter Number' in conDB[int(idRO[i])].columns:
                inputCSV.at[i,'C_Type'] = conDB[int(idRO[i])].at[idR[i],'Meter Number']
            elif 'Aerial/Underground' in conDB[int(idRO[i])].columns:
                inputCSV.at[i,'C_Type'] = conDB[int(idRO[i])].at[idR[i],'Aerial/Underground']
            elif 'Aerial / Underground' in conDB[int(idRO[i])].columns:
                inputCSV.at[i,'C_Type'] = conDB[int(idRO[i])].at[idR[i],'Aerial / Underground']
            inputCSV.at[i,'C_Address'] = conDB[int(idRO[i])].at[idR[i],'Street Address']
            inputCSV.at[i,'Id_Info'] = 'L:'+str(int(idL[i]))+';'+'S:'+str(int(idB[i]))+';'+'SO:'+str(int(idBO[i]))+';'+'C:'+str(int(idR[i]))+';'+'CO:'+str(int(idRO[i]))
        else:
            inputCSV.at[i,'Id_Info'] = 'L:'+str(int(idL[i]))+';'+'S:'+str(int(idB[i]))+';'+'SO:'+str(int(idBO[i]))
       
        inputCSV.at[i,'IDist_Ratio'] = dists[i]/maxRange
        
        note = ''
        if multiB[i]:
            note = note+'Mu_S,'
        if multiR[i]:
            note = note+'Mu_C,'
        if warnB[i]:
            note = note+'Ch_S,'
        if warnR[i] and predicted[i]:
            note = note+'Ch_C,'
        if (inputCSV.at[i,'S_Type'] == 'Underground' and inputCSV.at[i,'C_Type'] == 'Aerial') or (inputCSV.at[i,'S_Type'] == 'Aerial' and inputCSV.at[i,'C_Type'] == 'Underground'): 
            note = note+'M,'
        
        inputCSV.at[i,'Notes'] = note
        
        
        if KeepInput == 1:
            oldInputCSV = pd.read_csv('input.csv', converters={'Id Info':str,'Comment':str,'New_Name':str,'New_Mac':str})
            inputCSV.at[i,'Case'] = oldInputCSV.at[i,'Case']
            inputCSV.at[i,'New Lat'] = oldInputCSV.at[i,'New Lat']
            inputCSV.at[i,'New Long'] = oldInputCSV.at[i,'New Long']
            inputCSV.at[i,'Comment'] = oldInputCSV.at[i,'Comment']
            inputCSV.at[i,'New Name'] = oldInputCSV.at[i,'New Name']
            inputCSV.at[i,'New Mac'] = oldInputCSV.at[i,'New Mac']
        else:
            if pd.isnull(myDB.at[i,'Status']):
                inputCSV.at[i,'Case'] = ''
            elif myDB.at[i,'Status'].lower() == 'no street view':
                inputCSV.at[i,'Case'] = 1
            elif myDB.at[i,'Status'].lower() == 'obstructed view':
                inputCSV.at[i,'Case'] = 2
            elif myDB.at[i,'Status'].lower() == 'could not find':
                inputCSV.at[i,'Case'] = 3
            elif myDB.at[i,'Status'].lower() == 'see comment':
                inputCSV.at[i,'Case'] = 4
            else:
                print('Error: Status Unfamiliar')
                inputCSV.at[i,'Case'] = myDB.at[i,'Status']
            
            inputCSV.at[i,'New Lat'] = myDB.at[i,'Good Latitude']
            inputCSV.at[i,'New Long'] = myDB.at[i,'Good Longitude']
            inputCSV.at[i,'Comment'] = myDB.at[i,'Comment']
            if pd.isnull(myDB.at[i,'Continuity PS Name']):
                if predicted[i]:
                    inputCSV.at[i,'New Name'] = conDB[int(idRO[i])].at[idR[i],'Power Supply Name']
                    inputCSV.at[i,'New Mac'] = conDB[int(idRO[i])].at[idR[i],'MAC Address']
                else:
                    inputCSV.at[i,'New Name'] = 'Not in Continuity'
                    inputCSV.at[i,'New Mac'] = ''
            else:
                inputCSV.at[i,'New Name'] = myDB.at[i,'Continuity PS Name']
                inputCSV.at[i,'New Mac'] = myDB.at[i,'Mac Address']
    
    
    inputCSV.to_csv('input.csv', index=False)

#generates kml file for lines that can be uploaded to Google Earth Pro
def generateConnecters():
    inputCSV = pd.read_csv('input.csv', converters={'Id_Info':str,'Comment':str,'New Name':str,'New Mac':str})#,'S_Latitude':float,'S_Longitude':float,'C_Latitude':float,'C_Longitude':float

    latB = inputCSV['S_Latitude']
    longB = inputCSV['S_Longitude']
    
    latR = inputCSV['C_Latitude']
    longR = inputCSV['C_Longitude']
    
    notes = inputCSV['Notes']
    
    lineFile = open("connecters.kml", "w+")
    lineFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://earth.google.com/kml/2.0\"><Document>\n")
    
    for i in range(len(latB)):
        if pd.notna(latR[i]):
            if pd.isnull(notes[i]) == False and ('Mu_C' in notes[i] or 'Mu_S' in notes[i]):
                lineFile.write("<Placemark><LineString><coordinates>%f,%f,0.0 %f,%f,0.0</coordinates></LineString><Style><LineStyle><color>#ffff00ff</color><width>1.0</width></LineStyle></Style></Placemark>\n" % (longB[i],latB[i],longR[i],latR[i]))
            else:
                lineFile.write("<Placemark><LineString><coordinates>%f,%f,0.0 %f,%f,0.0</coordinates></LineString></Placemark>\n" % (longB[i],latB[i],longR[i],latR[i]))
        
    lineFile.write("</Document></kml>\n")
    lineFile.close()

#parses kml file and saves back into input file
def parseKML():
    targetsF = open(myKML, 'r') 
    targetsL = targetsF.readlines()
    shapes = []
    pM_Lat = []
    pM_Long = []
    l = 0
    while l < len(targetsL):
        if '<LinearRing>' in targetsL[l]:
            l+=2
            line = targetsL[l]
            if '<' in line:
                continue
            shapes.append([[],[]])
            cordinates = line.split(' \n')[0]
            cordinates = cordinates.split('\t')
            cordinates = cordinates[len(cordinates)-1].split(' ')
            for c in cordinates:
                splitCords = c.split(',')
                shapes[len(shapes)-1][0].append(float(splitCords[1]))
                shapes[len(shapes)-1][1].append(float(splitCords[0]))
        if '<Point>' in targetsL[l]:
            l+=2
            line = targetsL[l]
            cordinates = line.split('>')[1]
            cordinates = cordinates.split('<')[0]
            
            splitCords = cordinates.split(',')
            pM_Lat.append(float(splitCords[1]))
            pM_Long.append(float(splitCords[0]))
        l+=1
        
        
    #fill in cordinates using placemarks    
    inputCSV = pd.read_csv('input.csv', converters={'Id_Info':str,'Comment':str,'New Name':str,'New Mac':str})

    loc_Lat = inputCSV['S_Latitude']
    loc_Long = inputCSV['S_Longitude']
    
    minId = np.zeros(len(pM_Lat),dtype=int)
    minD = np.full(len(pM_Lat),np.inf)
    for i in range(len(loc_Lat)):
        latDiff = pM_Lat-loc_Lat[i]
        longDiff = pM_Long-loc_Long[i]
    
        dists = (latDiff*latDiff)+(longDiff*longDiff)#distance squared
    
        minId = np.where(dists < minD, i, minId)
        minD = np.where(dists < minD, dists, minD)
    
    redunCheck = set(minId)
    for r in redunCheck:
        if np.count_nonzero(minId == r)  > 1:
            #print("Caution, %d placemarks paired with a single Spatial at row %d in datasheet" % (minId.count(r),r+2))
            dupes = np.where(minId == r)[0]
            minDist = np.inf
            for d in dupes:
                if minD[d]>minDist:
                    minId[d] = -1#disable
                else:
                    minDist = minD[d]
                
            
            
        
        
    for i in range(len(minId)):
        if minId[i] != -1:
            if np.isnan(inputCSV.at[minId[i],'New Lat']) and np.isnan(inputCSV.at[minId[i],'New Long']):
                inputCSV.at[minId[i],'New Lat'] = pM_Lat[i]
                inputCSV.at[minId[i],'New Long'] = pM_Long[i]
            
    
    #records clusters using shapes
    sMembers = []
    for s in range(len(shapes)):
        sMembers.append([])
        nrmDirs = []
        for v in range(len(shapes[s][0])-1):
            #v2 = (v+1)%len(shapes[s][0])
            v2 = v+1
            lat1 = shapes[s][0][v]
            long1 = shapes[s][1][v]
            
            lat2 = shapes[s][0][v2]
            long2 = shapes[s][1][v2]
            
            #get nrm UV
            magnitude = math.hypot(lat2-lat1, long2-long1)
            nrmDirs.append([-(long2-long1)/magnitude,(lat2-lat1)/magnitude])
        minBounds = np.full(len(nrmDirs),np.inf)
        maxBounds = np.full(len(nrmDirs),-np.inf)
        for n in range(len(nrmDirs)):
            for v in range(len(shapes[s][0])-1):
                lat = shapes[s][0][v]
                long = shapes[s][1][v]
                dotLen = lat*nrmDirs[n][0]+long*nrmDirs[n][1]
                minBounds[n] = min(dotLen,minBounds[n])
                maxBounds[n] = max(dotLen,maxBounds[n])
        
        for d in range(len(spaDB)+len(conDB)):
            if d < len(spaDB):
                latitude = spaDB[d]['LATITUDE']
                longitude = spaDB[d]['LONGITUDE']
                sel = 0
            else:
                latitude = conDB[d-len(spaDB)]['Latitude']
                longitude = conDB[d-len(spaDB)]['Longitude']
                sel = 1
                
            inside = np.ones(len(latitude))
            for n in range(len(nrmDirs)):
                dotPos = latitude*nrmDirs[n][0]+longitude*nrmDirs[n][1]
                inside = np.where((dotPos>maxBounds[n]) | (dotPos<minBounds[n]), 0, inside)
            
            for i in np.where(inside == 1)[0]:
                sMembers[s].append((sel,i,d-sel*len(spaDB)))
        if len(sMembers[s]) == 0:
            print("Caution, no points found inside polygon near coordinates %f, %f" % (shapes[s][0][0],shapes[s][1][0]))
    
    #creates clusters datasheet from shapes
    clusterDB = pd.DataFrame(columns = ['PS_NETWORK_KEY-Spatial','POWER_SUPPLY_NAME','Continuity PS Name','Mac Address','Region','Division','Latitude','Longitude'])
    
    for shape in sMembers:
        #not in continuity
        if len(shape) == 0:
            continue
        if len(shape) == 1 and shape[0][0] == 0:
            spaID = shape[0]
            
            loc_nameCol = ''
            spa_nameCol = ''
            if 'PS_NETWORK_KEY-Spatial' in myDB.columns:
                loc_nameCol = 'PS_NETWORK_KEY-Spatial'
            elif 'ID' in myDB.columns:
                loc_nameCol = 'ID'
            if 'PS_NETWORK_KEY-Spatial' in spaDB[spaID[2]].columns:
                spa_nameCol = 'PS_NETWORK_KEY-Spatial'
            elif 'ID' in spaDB[spaID[2]].columns:
                spa_nameCol = 'ID'
    
            localID = np.where(myDB[loc_nameCol] == spaDB[spaID[2]].at[spaID[1],spa_nameCol])[0]
            if len(localID)>0:
                inputCSV.at[localID[0],'New Name'] = 'Not in Continuity'
                inputCSV.at[localID[0],'New Mac'] = ''
            continue
        #pair
        if len(shape) == 2 and shape[0][0] != shape[1][0]:
            if shape[0][0] == 0:
                spaID = shape[0]
                conID = shape[1]
            else:
                spaID = shape[1]
                conID = shape[0]
    
            loc_nameCol = ''
            spa_nameCol = ''
            if 'PS_NETWORK_KEY-Spatial' in myDB.columns:
                loc_nameCol = 'PS_NETWORK_KEY-Spatial'
            elif 'ID' in myDB.columns:
                loc_nameCol = 'ID'
            if 'PS_NETWORK_KEY-Spatial' in spaDB[spaID[2]].columns:
                spa_nameCol = 'PS_NETWORK_KEY-Spatial'
            elif 'ID' in spaDB[spaID[2]].columns:
                spa_nameCol = 'ID'
    
            localID = np.where(myDB[loc_nameCol] == spaDB[spaID[2]].at[spaID[1],spa_nameCol])[0]
            if len(localID)>0:
                inputCSV.at[localID[0],'New Name'] = conDB[conID[2]].at[conID[1],'Power Supply Name']
                inputCSV.at[localID[0],'New Mac'] = conDB[conID[2]].at[conID[1],'MAC Address']
            continue
        
        #cluster
        region = ''
        division = ''
        for mem in shape:
            if mem[0] == 0:
                loc_nameCol = ''
                spa_nameCol = ''
                if 'PS_NETWORK_KEY-Spatial' in myDB.columns:
                    loc_nameCol = 'PS_NETWORK_KEY-Spatial'
                elif 'ID' in myDB.columns:
                    loc_nameCol = 'ID'
    
                if 'PS_NETWORK_KEY-Spatial' in spaDB[mem[2]].columns:
                    spa_nameCol = 'PS_NETWORK_KEY-Spatial'
                elif 'ID' in spaDB[mem[2]].columns:
                    spa_nameCol = 'ID'
    
    
                if loc_nameCol != '' and spa_nameCol != '':
                    localID = np.where(myDB[loc_nameCol] == spaDB[mem[2]].at[mem[1],spa_nameCol])[0]
                    if len(localID)>0:
                        region = myDB.at[localID[0],'Region']
                        division = myDB.at[localID[0],'Division']
                        break
    
        for mem in shape:
            spa_Name = ''
            spa_ID = ''
            con_Name = ''
            con_Mac = ''
            ps_Lat = np.nan
            ps_Long = np.nan
    
    
            if mem[0] == 0:
                if 'PS_NETWORK_KEY-Spatial' in spaDB[mem[2]].columns:
                    spa_ID = spaDB[mem[2]].at[mem[1],'PS_NETWORK_KEY-Spatial']
                elif 'ID' in spaDB[mem[2]].columns:
                    spa_ID = spaDB[mem[2]].at[mem[1],'ID']
                    
                spa_Name = spaDB[mem[2]].at[mem[1],'POWER_SUPPLY_NAME']
                ps_Lat = spaDB[mem[2]].at[mem[1],'LATITUDE']
                ps_Long = spaDB[mem[2]].at[mem[1],'LONGITUDE']
            else:
                con_Name = conDB[mem[2]].at[mem[1],'Power Supply Name']
                con_Mac = conDB[mem[2]].at[mem[1],'MAC Address']
                ps_Lat = conDB[mem[2]].at[mem[1],'Latitude']
                ps_Long = conDB[mem[2]].at[mem[1],'Longitude']
    
            new_row = {'PS_NETWORK_KEY-Spatial':spa_ID,'POWER_SUPPLY_NAME':spa_Name,'Continuity PS Name':con_Name,'Mac Address':con_Mac,'Region':region,'Division':division,'Latitude':ps_Lat,'Longitude':ps_Long}
            clusterDB = clusterDB.append(new_row, ignore_index=True)
    
        new_row = {'PS_NETWORK_KEY-Spatial':'','POWER_SUPPLY_NAME':'','Continuity PS Name':'','Mac Address':'','Region':'','Division':'','Latitude':np.nan,'Longitude':np.nan}
        clusterDB = clusterDB.append(new_row, ignore_index=True)
    
    clusterDB.to_excel('clusters.xlsx',index=False)
    inputCSV.to_csv('input.csv', index=False)

#parses input fields input file and saves back into original file
#Warning! Make sure you get rid of all the degree signs from long and lat within the input file, otherwise this won't work
def sendtoResults():
    inputCSV = pd.read_csv('input.csv', converters={'Id_Info':str,'Comment':str,'New Name':str,'New Mac':str})
    
    caseN = inputCSV['Case']
    latN = inputCSV['New Lat']
    longN = inputCSV['New Long']
    commentN = inputCSV['Comment']
    nameN = inputCSV['New Name']
    macN = inputCSV['New Mac']
    idInfo = inputCSV['Id_Info']
    warn = False
    
    for i in range(len(caseN)):
        parsed = idInfo[i].split(';')
        predicted = 0;
        for p in parsed:
            arg = p.split(':')
            if arg[0] == 'L':
                idL = int(arg[1])
            if arg[0] == 'S':
                idB = int(arg[1])
            if arg[0] == 'SO':
                idBO = int(arg[1])
            if arg[0] == 'C':
                idR = int(arg[1])
                predicted = 1
            if arg[0] == 'CO':
                idRO = int(arg[1])
        
        myDB.at[idL,'Good Latitude'] = latN[i]
        myDB.at[idL,'Good Longitude'] = longN[i]
        myDB.at[idL,'Continuity PS Name'] = nameN[i]
        myDB.at[idL,'Mac Address'] = macN[i]
        
        myDB.at[idL,'Status'] = ''
        
        if caseN[i] == 1:
            myDB.at[idL,'Status'] = 'No Street View'
        if caseN[i] == 2:
            myDB.at[idL,'Status'] = 'Obstructed View'
        if caseN[i] == 3:
            myDB.at[idL,'Status'] = 'Could Not Find'
        if caseN[i] == 4:
            myDB.at[idL,'Status'] = 'See Comment'
        if caseN[i] == 5:
            warn = True
            myDB.at[idL,'Status'] = 'See Comment'
            if 'cluster' not in commentN[i]:
                commentN[i] = 'cluster situation, '+commentN[i]
                
        myDB.at[idL,'Comment'] = commentN[i]
        
        
    myDB.to_excel(myFile, index=False)
    
    if warn:
        print('Ignore the warning above')
