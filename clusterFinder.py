# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:49:32 2020

"""
import usaddress
import dataHelper

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
                        nameHold = wordCh
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
        
        for m in range(len(membersR)):#for each spatial point in address group
            color = membersR[m][0]
            index = membersR[m][1]
            originFile = membersR[m][2]
            
            latitude = latR[m]
            longitude = longR[m]
    """

#group by proximity




#pairing functions (if spa and cont grouped seperately)
#

