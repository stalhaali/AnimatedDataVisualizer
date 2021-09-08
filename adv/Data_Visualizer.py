import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import bar_chart_race as bcr
  


def create_gif(doc = "C:/Users/taha4/Desktop/Anthro/test.csv", high=True, background="C:/Users/taha4/Desktop/Anthro/Nikop1.png"):
    df = pd.read_csv(doc)
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)
    #del df["date"]
    #color = ["blue", "red", "pink", "white"]
    color = []
    for i in range(len(df.columns)):
        color.append(input("What colour represents " + df.columns[i] + "?"))
    
    fig = plt.figure()
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('No of Deaths')
    plt.xlabel('Dates')
    
    

    def buildmebarchart(i=int):
    
        plt.legend(df.columns)
        p = plt.plot(df[:i].index, df[:i].values) #note it only returns the dataset, up to the point i
        for i in range(0,4):
            p[i].set_color(color[i]) #set the colour of each curve

            
    animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
    
    plt.show()
    
def create_bar(doc = "C:/Users/Talha/Desktop/coursera/coursera-2021/project1/animateddatavisualizer/test.csv", high=True, background="C:/Users/taha4/Desktop/Anthro/Nikop1.png"):
    
    df = pd.read_csv(doc)
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)
    df = df.loc[df.first_valid_index():df.last_valid_index()]
    
    html = bcr.bar_chart_race(
    df=df,
    period_fmt='%B %d, %Y',
    title='COVID-19 Confirmed Cases by Country')

    return html
  
    
