#%%
# import needed liraries
import numpy as np
import pandas as pd
import pycountry_convert as pc


# %%
#read the original csv file
import os
os. chdir("C:\\Users\\malakm\\Documents\\Gwu\DataVisualization\\Final Project") 
dirpath = os.getcwd() # print("current directory is : " + dirpath)
print(dirpath)

#%%
#Read the original data
filepath = os.path.join(dirpath ,'international_football_results2.csv')
myData = pd.read_csv(filepath , parse_dates = ['date']) 

print('\n',myData.head(),'\n')
#print(filepath)

#%%
myData["total_score"] = myData["home_score"] + myData["away_score"]
print('\n',myData.head(),'\n')

myData.loc[myData['home_team'] == 'Czechoslovakia', 'home_team'] = "Czech Republic"
myData.loc[myData['away_team'] == 'Czechoslovakia', 'away_team'] = "Czech Republic"
myData.loc[myData['country'] == 'Czechoslovakia', 'country'] = "Czech Republic"


myData.loc[myData['home_team'] == 'German DR', 'home_team'] = "Germany"
myData.loc[myData['away_team'] == 'German DR', 'away_team'] = "Germany"
myData.loc[myData['country'] == 'German DR', 'country'] = "Germany"

myData.loc[myData['home_team'] == 'Burma', 'home_team'] = "Myanmar"
myData.loc[myData['away_team'] == 'Burma', 'away_team'] = "Myanmar"
myData.loc[myData['country'] == 'Burma', 'country'] = "Myanmar"

myData.loc[myData['home_team'] == 'Korea Republic', 'home_team'] = "South Korea"
myData.loc[myData['away_team'] == 'Korea Republic', 'away_team'] = "South Korea"
myData.loc[myData['country'] == 'Korea Republic', 'country'] = "South Korea"

myData.loc[myData['home_team'] == 'Congo DR', 'home_team'] = "Democratic Republic of the Congo"
myData.loc[myData['away_team'] == 'Congo DR', 'away_team'] = "Democratic Republic of the Congo"

myData['year'] =   myData['date'].apply(returnYear)
myData['month'] =   myData['date'].apply(returnMonth)

print('\n',myData.head(),'\n')


#%%
def getContinentCode(country):
  """
  finding continent from country name using pycountry_convert
  :param n: country name
  :return: the continent code
  """
  try:
    if country == 'Scotland':
        return "EU"
    elif country == 'England':
        return "EU"
    elif country == 'Wales':
        return "EU"
    elif country == 'Northern Ireland':
        return "EU"
    else:
        countryCode = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        return pc.country_alpha2_to_continent_code(countryCode)
  except:
    return  "UNKNOWN"

def returnYear(date):
    """
    Return the year
    """
    y = str(date)[:4]
    x = int(y)
    return x

def returnMonth(date):
    """
    Return the month
    """
    y = str(date)[5:7]
    x = int(y)
    return x


# %%

#myData['home_continent'] = getContinentCode(myData['away_team'])
myData['home_continent'] = myData['home_team'].apply(getContinentCode)
myData['away_continent'] = myData['away_team'].apply(getContinentCode)  
myData['game_continenr'] = myData['country'].apply(getContinentCode)  

# %%
#save the new CSV

myData2 = os.path.join( os.getcwd(), 'updatedData2.csv')
#myData.to_csv(myData2)  

myData = myData[myData.home_continent != 'UNKNOWN']
myData = myData[myData.away_continent != 'UNKNOWN']

#myData = myData[myData['year']>1930]
myData3 = os.path.join( os.getcwd(), 'updatedData4.csv')
myData.to_csv(myData3)  

# %%

#getting data for the racing bar chart 

allTeams = myData[['home_team', 'away_team']].to_numpy()
allTeams = np.unique(allTeams)
allTeams = pd.DataFrame(data=allTeams,columns=["team"])

allYears = np.unique(myData[['year']])
allYears = pd.DataFrame(data=allYears,columns=["year"])

testDF1 = myData.groupby(["home_team"],as_index=False)["home_score"].sum().sort_values(by=['home_score'],ascending=False)
testDF2 = myData.groupby(["away_team"],as_index=False)["away_score"].sum().sort_values(by=['away_score'],ascending=False)


testDF1 = testDF1.rename(columns={"home_team": "team", "home_score": "score1"})
testDF2 = testDF2.rename(columns={"away_team": "team", "away_score": "score2"})

testDF1 = testDF1.sort_values(by=['team'])
testDF2 = testDF2.sort_values(by=['team'])
testDF1['total'] = ""

for  index, row in testDF1.iterrows():
    if (testDF2.loc[testDF2['team'] == row['team'] ,'score2']).size !=1:
        testDF1.at[index,"total"] = row['score1'] 
    else:
        testDF1.at[index,"total"] = row['score1'] + testDF2.loc[testDF2['team'] == row['team'],'score2'][testDF2.index[testDF2['team'] == row['team']][0]]
        #print(str(row['score1']) +   ' + ' + str(testDF2.loc[testDF2['team'] == row['team'],'score2'][testDF2.index[testDF2['team'] == row['team']][0]]))

testDF1 = testDF1.sort_values(by=['total'],ascending=False)
#allTeams = testDF1[0:49]['team']

#%%

#allTeams = testDF1[0:49]['team']

columns = ['name','value','year','lastValue','rank','games_home','games_away', 'score_home', 'score_away','wins','loses','draw_home','draw_away']
racindgBarDf = pd.DataFrame(columns=columns)

testDF1_score1 = myData.groupby(["year","home_team"],as_index=False)["home_score"].sum().sort_values(by=['home_score'],ascending=False)
testDF2_score2 = myData.groupby(["year","away_team"],as_index=False)["away_score"].sum().sort_values(by=['away_score'],ascending=False)
testDF1_score1 = testDF1_score1.rename(columns={"home_team": "team", "home_score": "score1"})
testDF2_score2 = testDF2_score2.rename(columns={"away_team": "team", "away_score": "score2"})

testDF1_play1 = myData.groupby(["year","home_team"],as_index=False)["home_score"].count().sort_values(by=['home_score'],ascending=False)
testDF2_play2 = myData.groupby(["year","away_team"],as_index=False)["away_score"].count().sort_values(by=['away_score'],ascending=False)
testDF1_play1 = testDF1_play1.rename(columns={"home_team": "team", "home_score": "home_games"})
testDF2_play2 = testDF2_play2.rename(columns={"away_team": "team", "away_score": "away_games"})

testDF1_win1 = myData.groupby(["year","home_team"],as_index=False)["home_win"].sum().sort_values(by=['home_win'],ascending=False)
testDF2_win2 = myData.groupby(["year","away_team"],as_index=False)["away_win"].sum().sort_values(by=['away_win'],ascending=False)
testDF1_win1 = testDF1_win1.rename(columns={"home_team": "team", "home_score": "home_wins"})
testDF2_win2 = testDF2_win2.rename(columns={"away_team": "team", "away_score": "away_wins"})

testDF1_draw1 = myData.groupby(["year","home_team"],as_index=False)["draw"].sum().sort_values(by=['draw'],ascending=False)
testDF2_draw2 = myData.groupby(["year","away_team"],as_index=False)["draw"].sum().sort_values(by=['draw'],ascending=False)
testDF1_draw1 = testDF1_draw1.rename(columns={"home_team": "team", "draw": "draw1"})
testDF2_draw2 = testDF2_draw2.rename(columns={"away_team": "team", "draw": "draw2"})

testDF1_Opscore1 = myData.groupby(["year","home_team"],as_index=False)["away_score"].sum().sort_values(by=['away_score'],ascending=False)
testDF2_Opscore2 = myData.groupby(["year","away_team"],as_index=False)["home_score"].sum().sort_values(by=['home_score'],ascending=False)
testDF1_Opscore1 = testDF1_Opscore1.rename(columns={"home_team": "team", "away_score": "Opscore1"})
testDF2_Opscore2 = testDF2_Opscore2.rename(columns={"away_team": "team", "home_score": "Opscore2"})

#allTeams = allTeams.head(20)
#allyears = allYears.tail(30)


	   
#%%
columns = ['name','value','year','lastValue','rank','games_home','games_away', 'score_home', 'score_away','win_home','win_away','loss_home',"loss_away",'draw_home','draw_away' ,'opp_score_home','opp_score_away']
racindgBarDf = pd.DataFrame(columns=columns)

#testDF3 = pd.merge_asof(testDF1,testDF2, on='team')

for  indexT, rowT in allTeams.iterrows():
	for  indexY, rowY in allYears.iterrows():
		#temp1 = myData[myData['year']==rowY['year'] & myData['year']]
		myIndex = (indexT)*(allYears.size) + indexY
		# populate home score per country per year
		if (testDF1_score1.loc[(testDF1_score1['team'] == rowT['team']) & (testDF1_score1['year'] == rowY['year']),'score1']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'score_home']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'score_home'] = testDF1_score1.loc[(testDF1_score1['team'] ==rowT['team'] ) & (testDF1_score1['year'] == rowY['year']),'score1'].values[0] 

		# populate away score per country per year
		if (testDF2_score2.loc[(testDF2_score2['team'] == rowT['team']) & (testDF2_score2['year'] == rowY['year']),'score2']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'score_away']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'score_away'] = testDF2_score2.loc[(testDF2_score2['team'] ==rowT['team'] ) & (testDF2_score2['year'] == rowY['year']),'score2'].values[0]
    	
        # populate home opp score per country per year
		if (testDF1_Opscore1.loc[(testDF1_Opscore1['team'] == rowT['team']) & (testDF1_Opscore1['year'] == rowY['year']),'Opscore1']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'opp_score_home']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'opp_score_home'] = testDF1_Opscore1.loc[(testDF1_Opscore1['team'] ==rowT['team'] ) & (testDF1_Opscore1['year'] == rowY['year']),'Opscore1'].values[0] 
	
    		# populate away opp score per country per year
		if (testDF2_Opscore2.loc[(testDF2_Opscore2['team'] == rowT['team']) & (testDF2_Opscore2['year'] == rowY['year']),'Opscore2']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'opp_score_away']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'opp_score_away'] = testDF2_Opscore2.loc[(testDF2_Opscore2['team'] ==rowT['team'] ) & (testDF2_Opscore2['year'] == rowY['year']),'Opscore2'].values[0] 
		
		# populate home draws per country per year
		if (testDF1_draw1.loc[(testDF1_draw1['team'] == rowT['team']) & (testDF1_draw1['year'] == rowY['year']),'draw1']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'draw_home']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'draw_home'] = testDF1_draw1.loc[(testDF1_draw1['team'] ==rowT['team'] ) & (testDF1_draw1['year'] == rowY['year']),'draw1'].values[0]				 
		
		# populate away draws per country per year
		if (testDF2_draw2.loc[(testDF2_draw2['team'] == rowT['team']) & (testDF2_draw2['year'] == rowY['year']),'draw2']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'draw_away']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'draw_away'] = testDF2_draw2.loc[(testDF2_draw2['team'] ==rowT['team'] ) & (testDF2_draw2['year'] == rowY['year']),'draw2'].values[0]   

		# populate home play per country per year
		if (testDF1_play1.loc[(testDF1_play1['team'] == rowT['team']) & (testDF1_play1['year'] == rowY['year']),'home_games']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'games_home']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'games_home'] = testDF1_play1.loc[(testDF1_play1['team'] ==rowT['team'] ) & (testDF1_play1['year'] == rowY['year']),'home_games'].values[0] 
  
		# populate away play per country per year
		if (testDF2_play2.loc[(testDF2_play2['team'] == rowT['team']) & (testDF2_play2['year'] == rowY['year']),'away_games']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'games_away']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'games_away'] = testDF2_play2.loc[(testDF2_play2['team'] ==rowT['team'] ) & (testDF2_play2['year'] == rowY['year']),'away_games'].values[0] 

		# populate home wins per country per year
		if (testDF1_win1.loc[(testDF1_win1['team'] == rowT['team']) & (testDF1_win1['year'] == rowY['year']),'home_win']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'win_home']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'win_home'] = testDF1_win1.loc[(testDF1_win1['team'] ==rowT['team'] ) & (testDF1_win1['year'] == rowY['year']),'home_win'].values[0]		 
		
		# populate away wins per country per year
		if (testDF2_win2.loc[(testDF2_win2['team'] == rowT['team']) & (testDF2_win2['year'] == rowY['year']),'away_win']).size !=1:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'win_away']= 0
		else:
			racindgBarDf.at[myIndex,'name']=rowT['team'] 
			racindgBarDf.at[myIndex,'year']=rowY['year'] 
			racindgBarDf.at[myIndex,'win_away'] = testDF2_win2.loc[(testDF2_win2['team'] ==rowT['team'] ) & (testDF2_win2['year'] == rowY['year']),'away_win'].values[0] 
				   

#%%%
racindgBarDf = racindgBarDf[(racindgBarDf['games_home']!=0) & (racindgBarDf['games_away']!=0)]
finalData = os.path.join( os.getcwd(), 'finalData9.csv')
racindgBarDf.to_csv(finalData, index = None)  



# %%
