# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:49:32 2020

add
"""
import usaddress
import dataHelper
import pandas as pd
import numpy as np
import math

#might be a better way to get global variables...
dataHelper.initializeHelper()
global myFile
global myKML
global spaFiles
global conFiles
global myDB
global spaDB
global conDB
global KeepInput
global maxRange

myFile = dataHelper.myFile
myKML = dataHelper.myKML
spaFiles = dataHelper.spaFiles
conFiles = dataHelper.conFiles
myDB = dataHelper.myDB
spaDB = dataHelper.spaDB
conDB = dataHelper.conDB
KeepInput = dataHelper.KeepInput
maxRange = dataHelper.maxRange

#grouping functions
#group by name
def nameGroup():#can rename
    pass

#group by address
def addressGroup():
    uniNames = []
    
    #array with two dictionaries, first is for spa, second is for con. each dictionary holds where each member is in the database, as well as its lat and long cordinates
    members = [{},{}]#Format = [SpaDictionary{'address' = [(color=(0 or 1), index, filenumber), latitude, longitude]}, ConDictionary{'address' = [...]}]
    
    hwyAlt = ['highway']
    
    #assign groups
    for d in range(len(spaDB)+len(conDB)):
        if d < len(spaDB):
            address = spaDB[d]['ADDRESS']
            latitude = spaDB[d]['LATITUDE']
            longitude = spaDB[d]['LONGITUDE']
            sel = 0
        else:
            address = conDB[d-len(spaDB)]['Street Address']
            latitude = conDB[d-len(spaDB)]['Latitude']
            longitude = conDB[d-len(spaDB)]['Longitude']
            sel = 1
            
        stNum = [None]*len(address)
        for a in range(len(address)):
            parseme = address[a].lower()
            if parseme == '':
                continue
            parseme = parseme.split('\n', 1)[0]
            parseme = parseme.split('(', 1)[0]
            parseme = parseme.split('@', 1)[0]
            parseme = parseme.split(' of ', 1)[0]
            parseme = parseme.split(' for ', 1)[0]
            parseme = parseme.split(' and ', 1)[0]
            parseme = parseme.replace(',', '')
            parseme = parseme.replace('.', '')
            parseme = parseme.replace('old ', '')
            parseme = parseme.replace('saint ', '')
            parseme = parseme.replace('the ', '')
            for alt in hwyAlt:
                parseme = parseme.replace(alt, 'hwy')
                
            #check if highway
            if '-' in parseme:
                highCh = parseme.split('-', 1)[1]
                highCh = parseme.split(' ')[0]
                if highCh.isnumeric():
                    nameHold = 'hwy '+ highCh
                    if nameHold not in uniNames:
                        uniNames.append(nameHold)
                    
                    if nameHold not in members[sel]:
                        members[sel][nameHold] = [[],[],[]]
    
                    members[sel][nameHold][0].append((sel,a,d-sel*len(spaDB)))
                    members[sel][nameHold][1].append(latitude[a])
                    members[sel][nameHold][2].append(longitude[a])
                    continue
                    
    
            parseme = parseme.replace('-', '')
            
            highCh = parseme.split(' ')
            if 'hwy' in highCh:
                locID = highCh.index('hwy')
                if locID < len(highCh)-1 and highCh[locID+1].isnumeric():
                    nameHold = 'hwy '+ highCh[locID+1]
                    if nameHold not in uniNames:
                        uniNames.append(nameHold)
                    
                    if nameHold not in members[sel]:
                        members[sel][nameHold] = [[],[],[]]
    
                    members[sel][nameHold][0].append((sel,a,d-sel*len(spaDB)))
                    members[sel][nameHold][1].append(latitude[a])
                    members[sel][nameHold][2].append(longitude[a])
                    continue
            
            if highCh[0].isnumeric():
                stNum[a] = highCh[0]#if want to store number
            else:
                parseme = '123 ' + parseme
            parsed = usaddress.parse(parseme)
            
            nameHold = ''
            for p in range(len(parsed)):
                if parsed[p][1] == 'StreetName':
                    wordCh = ''.join([i for i in parsed[p][0] if not i.isdigit()])
                    if len(wordCh) > 2:
                        nameHold = wordCh #=wordCh+nameHold for longer address fields
                        break
                        
            if len(nameHold) > 0:     
                if nameHold not in uniNames:
                    uniNames.append(nameHold)
    
                if nameHold not in members[sel]:
                        members[sel][nameHold] = [[],[],[]]
                        
                members[sel][nameHold][0].append((sel,a,d-sel*len(spaDB)))
                members[sel][nameHold][1].append(latitude[a])
                members[sel][nameHold][2].append(longitude[a])
    
    return members
    #Usage example
    """
    for name in uniNames:#for each unique address
        if name in members[0]:#if there are spatial points that are part of the group
            membersB = members[0][name][0]
            latB = members[0][name][1]
            longB = members[0][name][2]
            
        if name in members[1]:#if there are continuity points that are part of the group
            membersR = members[1][name][0]
            latR = members[1][name][1]
            longR = members[1][name][2]
        
        for m in range(len(membersB)):#for each spatial point in address group
            color = membersB[m][0]#1 or 0
            index = membersB[m][1]
            originFile = membersB[m][2]
            
            latitude = latB[m]
            longitude = longB[m]
        
        for m in range(len(membersR)):#for each continuity point in address group
            color = membersR[m][0]
            index = membersR[m][1]
            originFile = membersR[m][2]
            
            latitude = latR[m]
            longitude = longR[m]
    """

#group by proximity
#def proximityGroup():#can rename
if(True):
    pairsB = [None]*len(spaFiles)         
    for s in range(len(spaFiles)):
        pairsB[s] = pd.read_csv('closest_pairsB'+str(s)+'.csv')
    
    pairsR = [None]*len(conFiles)         
    for c in range(len(conFiles)):
        pairsR[c] = pd.read_csv('closest_pairsR'+str(c)+'.csv')
        
    
    members = [[],[]]
    keyPoint = [[],[]]
    for s in range(len(spaDB)):
        members[0].append([])
        keyPoint[0].append([])
        for idB in range(spaDB[s].shape[0]):
            members[0][s].append([[],[]])
            keyPoint[0][s].append(False)
            
            idR = pairsB[s].at[idB,'Con Id']
            idRO = int(pairsB[s].at[idB,'Con Ori'])
            
            idB2 = pairsR[idRO].at[idR,'Spa Id']
            idBO2 = pairsR[idRO].at[idR,'Spa Ori']
                           
            if idB == idB2 and s == idBO2:
                keyPoint[0][s][idB] = True
            
            for c in range(len(pairsR)):
                locID = pairsR[c].index[(idB == pairsR[c]['Spa Id']) & (s == pairsR[c]['Spa Ori'])]
                for m in locID:
                    members[0][s][idB][0].append((1,m,c))
                    members[0][s][idB][1].append(math.sqrt(pairsR[c].at[m,'Distance^2']))
                    
    for c in range(len(conDB)):
        members[1].append([])
        keyPoint[1].append([])
        for idR in range(conDB[c].shape[0]):
            members[1][c].append([[],[]])
            keyPoint[1][c].append(False)
            
            idB = pairsR[c].at[idR,'Spa Id']
            idBO = int(pairsR[c].at[idR,'Spa Ori'])
            
            idR2 = pairsB[idBO].at[idB,'Con Id']
            idRO2 = pairsB[idBO].at[idB,'Con Ori']
            
                           
            if idR == idR2 and c == idRO2:
                keyPoint[1][c][idR] = True
            
            for s in range(len(pairsB)):
                locID = pairsB[s].index[(idR == pairsB[s]['Con Id']) & (c == pairsB[s]['Con Ori'])]
                for m in locID:
                    members[1][c][idR][0].append((0,m,s))
                    members[1][c][idR][1].append(math.sqrt(pairsB[s].at[m,'Distance^2']))
    
    pairsHold = [pairsB,pairsR]
    leaway = 1
    def searchMembers(idC, idP):
        keyPoint[idC[0]][idC[2]][idC[1]] = False
        baseDist = math.sqrt(pairsHold[idC[0]][idC[2]].at[idC[1],'Distance^2'])
        
        memInfo = members[idC[0]][idC[2]][idC[1]]
        memID = memInfo[0]
        memDist = memInfo[1]
        
        memHold = []
        for m in range(len(memID)):
            if memID[m] != idP and (((memDist[m] - baseDist) <=  baseDist*leaway) ):#or len(members[memID[m][0]][memID[m][2]][memID[m][1]][0])==0):
                memHold = memHold+searchMembers(memID[m],idC)
        return [idC]+memHold
        
        
    def getDist(id1, id2):
        if id1[0] == 0:
            lat1 = spaDB[id1[2]].at[id1[1],'LATITUDE']
            long1 = spaDB[id1[2]].at[id1[1],'LONGITUDE']
        else:
            lat1 = conDB[id1[2]].at[id1[1],'Latitude']
            long1 = conDB[id1[2]].at[id1[1],'Longitude']
        
        if id2[0] == 0:
            lat2 = spaDB[id2[2]].at[id2[1],'LATITUDE']
            long2 = spaDB[id2[2]].at[id2[1],'LONGITUDE']
        else:
            lat2 = conDB[id2[2]].at[id2[1],'Latitude']
            long2 = conDB[id2[2]].at[id2[1],'Longitude']
        
        return math.hypot(lat2-lat1, long2-long1)
        
        
        
    clusters = []
    for s in range(len(members[0])):
        for idB in range(len(members[0][s])):
            if keyPoint[0][s][idB] and len(members[0][s][idB][0])>1:
                startID = (0,idB,s)
                clusterHold = searchMembers(startID, startID)
                if len(clusterHold)>2:
                    pastlen = 0
                    currlen = len(clusterHold)
                    while pastlen != currlen:
                        break#experimental
                        pastlen = currlen
                        for i in range(len(clusterHold)):
                            baseID = clusterHold[i]
                            baseDist = math.sqrt(pairsHold[baseID[0]][baseID[2]].at[baseID[1],'Distance^2'])
                            for j in range(len(clusterHold)):
                                if i != j:
                                    tipID = clusterHold[j]
                                    if baseID[0] == tipID[0]:
                                        memIDs = members[tipID[0]][tipID[2]][tipID[1]][0]
                                        for ID in memIDs:
                                            if ID not in clusterHold and abs(getDist(baseID,ID) - baseDist) <=  baseDist*leaway:
                                                #clusterHold = clusterHold+searchMembers(ID,ID)
                                                clusterHold.append(ID)
                                                #print('added at cluster', len(clusters))
                        #currlen = len(clusterHold)
                    clusters.append(clusterHold)
    pastClusterLen = len(clusters)
    
    for c in range(len(members[1])):
        for idR in range(len(members[1][c])):
            if keyPoint[1][c][idR] and len(members[1][c][idR][0])>1:
                startID = (1,idR,c)
                clusterHold = searchMembers(startID, startID)
                if len(clusterHold)>2:
                    pastlen = 0
                    currlen = len(clusterHold)
                    while pastlen != currlen:
                        break#experimental
                        pastlen = currlen
                        for i in range(len(clusterHold)):
                            baseID = clusterHold[i]
                            baseDist = math.sqrt(pairsHold[baseID[0]][baseID[2]].at[baseID[1],'Distance^2'])
                            for j in range(len(clusterHold)):
                                if i != j:
                                    tipID = clusterHold[j]
                                    if baseID[0] == tipID[0]:
                                        memIDs = members[tipID[0]][tipID[2]][tipID[1]][0]
                                        for ID in memIDs:
                                            if ID not in clusterHold and abs(getDist(baseID,ID) - baseDist) <=  baseDist*leaway:
                                                #clusterHold = clusterHold+searchMembers(ID,ID)
                                                clusterHold.append(ID)
                                                #print('added at cluster', len(clusters)-pastClusterLen+1)
                        #currlen = len(clusterHold)
                    clusters.append(clusterHold)
    
    
    lineFile = open("clusterChecks.kml", "w+")
    lineFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://earth.google.com/kml/2.0\"><Document>\n")
    
    
    for shape in clusters:
        baseP = shape[0]
        if baseP[0] == 0:
            baseLat = spaDB[baseP[2]].at[baseP[1],'LATITUDE']
            baseLong = spaDB[baseP[2]].at[baseP[1],'LONGITUDE']
        else:
            baseLat = conDB[baseP[2]].at[baseP[1],'Latitude']
            baseLong = conDB[baseP[2]].at[baseP[1],'Longitude']
        
        for s in range(len(shape)-1):
            tipP = shape[s+1]
            if tipP[0] == 0:
                tipLat = spaDB[tipP[2]].at[tipP[1],'LATITUDE']
                tipLong = spaDB[tipP[2]].at[tipP[1],'LONGITUDE']
            else:
                tipLat = conDB[tipP[2]].at[tipP[1],'Latitude']
                tipLong = conDB[tipP[2]].at[tipP[1],'Longitude']
            lineFile.write("<Placemark><LineString><coordinates>%f,%f,0.0 %f,%f,0.0</coordinates></LineString><Style><LineStyle><color>#ffff00ff</color><width>1.0</width></LineStyle></Style></Placemark>\n" % (baseLong,baseLat,tipLong,tipLat))
    lineFile.write("</Document></kml>\n")
    lineFile.close()

    
    clusterDB = pd.DataFrame(columns = ['PS_NETWORK_KEY-Spatial','POWER_SUPPLY_NAME','Continuity PS Name','Mac Address','Latitude','Longitude'])
    clusterIndex = 1
    for shape in clusters:
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
        
            new_row = {'PS_NETWORK_KEY-Spatial':spa_ID,'POWER_SUPPLY_NAME':spa_Name,'Continuity PS Name':con_Name,'Mac Address':con_Mac,'Latitude':ps_Lat,'Longitude':ps_Long}
            clusterDB = clusterDB.append(new_row, ignore_index=True)
        
        new_row = {'PS_NETWORK_KEY-Spatial':str(clusterIndex),'POWER_SUPPLY_NAME':'','Continuity PS Name':'','Mac Address':'','Latitude':np.nan,'Longitude':np.nan}
        clusterDB = clusterDB.append(new_row, ignore_index=True)
        clusterIndex+=1
    clusterDB.to_excel('clustersFound.xlsx',index=False)
                
    
    
                            
                            
                    
                    
    
    
"""
ideas:
if a spa is closer to a spa than con, or the other way around, its part of a cluster

if a spa is the closest spa point to multiple con points, or vise versa, mark all involved as part of cluster (point that are not in continuity are at risk)
^flatten long and lat distance into just distance from the spa point, if closest con point more closer to a con than the spa, add to cluster

any point who's closest point is part of a cluster gets added to the cluster



"""



#pairing functions (if spa and cont grouped seperately)
#takes grouped spatial clusters and adds continuity points if they are involved via proximity
def Method1(spaGroups):
    #find local in spa data
    pairsR = [None]*len(conFiles)         
    for c in range(len(conFiles)):
        pairsR[c] = pd.read_csv('closest_pairsR'+str(c)+'.csv')  
    
    for g in range(len(spaGroups)):
        idB = spaGroups[g][index]
        idBO = spaGroups[g][originFile]

        for i in range(len(pairsR)):
            locID = pairsR[i].index[(idB[p] == pairsR[i]['Spa Id']) & (idBO[p] == pairsR[i]['Spa Ori'])]

            for m in locID:
                spaGroups[g][color] = red
                spaGroups[g][index] = m
                spaGroups[g][originFile] = i
                
    return spaGroups


def Method2():#can rename
    pass