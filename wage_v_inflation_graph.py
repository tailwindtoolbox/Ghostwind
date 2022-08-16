from operator import mod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3



inflation_data = pd.read_csv("/Users/charan/Documents/UC_San_Diego_Data_Science_Course/Final_Project/Inflation(CPI)(7_21_22).csv")
wage_data = pd.read_csv("/Users/charan/Documents/UC_San_Diego_Data_Science_Course/Final_Project/Unit_Labour_Costs(7_21_22).csv")
plt.style.use('fivethirtyeight')

def curate_wage_data(country):
    c_wage_data = wage_data[wage_data["LOCATION"].str.contains(country)]
    c_wage_data = c_wage_data[c_wage_data["MEASURE"].str.contains("PC_CHGPP")]
    c_wage_data = c_wage_data[c_wage_data["FREQUENCY"].str.contains("A")]
    c_wage_data = c_wage_data[c_wage_data["SUBJECT"].str.contains("EMP")]
    return c_wage_data

def curate_inflation_data(country):
    c_inflation_data = inflation_data[inflation_data["LOCATION"].str.endswith(country)]
    c_inflation_data = c_inflation_data[c_inflation_data["MEASURE"].str.endswith("AGRWTH")]
    c_inflation_data = c_inflation_data[c_inflation_data["FREQUENCY"].str.endswith("A")]
    c_inflation_data = c_inflation_data[c_inflation_data["SUBJECT"].str.endswith("TOT")]
    return c_inflation_data

def graph_wage(country):
    c_wage_data=curate_wage_data(country)
    c_inflation_data=curate_inflation_data(country)
    X = c_wage_data["TIME"].values
    Y = c_wage_data["Value"].values
    itime = c_inflation_data["TIME"].values
    wtime = c_wage_data["TIME"].values
    startpos=0
    #print(itime)
    #print(wtime)
    istart = int(itime[0])
    wstart = int(wtime[0])
    #print("istart")
    #print(istart)
    #print("wstart")
    #print(wstart)
    if(istart>wstart):
        while(wstart<istart):
            startpos+=1
            wstart+=1
            #print(wstart)
        X=X[startpos:]
        Y=Y[startpos:]
    
    #print(itime)
    #print(wtime)
    X=[pd.to_datetime(d) for d in X]
    plt.plot(X,Y)
    #print(str(int(max(X))) +" "+ str(int(min(Y))-1) +" "+ str(int(max(Y))+1))
    #plt.axis([0,(int(max(X))-int(min(X))),int(min(Y))-1,int(max(Y))+1])
    plt.xlabel("Year")
    plt.ylabel("Annual Growth Rate(%)")
    plt.title('Unit labour costs by Employee for '+country)
    #plt.xticks(yearticks)
    plt.show()

def graph_inflation(country):
    c_inflation_data=curate_inflation_data(country)
    c_wage_data=curate_wage_data(country)
    X = c_inflation_data["TIME"].values
    Y = c_inflation_data["Value"].values
    
    itime = c_inflation_data["TIME"].values
    wtime = c_wage_data["TIME"].values
    
    startpos=0
    istart = int(itime[0])
    wstart = int(wtime[0])
    #print("istart")
    #print(istart)
    #print("wstart")
    #print(wstart)
    if(wstart>istart):
        while(istart<wstart):
            startpos+=1
            istart+=1
            #print(istart)
        X=X[startpos:]
        Y=Y[startpos:]
    #print(itime)
    #print(wtime)
    #print(str(int(max(X))) +" "+ str(int(min(Y))-1) +" "+ str(int(max(Y))+1))
    #plt.axis([0,(int(max(X))-int(min(X))),int(min(Y))-1,int(max(Y))+1])

    X=[pd.to_datetime(d) for d in X]
    plt.plot(X,Y)
    #plt.xticks(yearticks)
    plt.xlabel("Year")
    plt.ylabel("Consumer Price Index")
    plt.title('Inflation for '+country)
    plt.show()

def graph_wage_vs_inflation(country):
    c_inflation_data=curate_inflation_data(country)
    c_wage_data=curate_wage_data(country)
    xtime = c_inflation_data["TIME"].values
    ytime = c_wage_data["TIME"].values
    X = c_inflation_data["Value"].values
    Y = c_wage_data["Value"].values
    startpos=0
    xstart = int(xtime[0])
    ystart = int(ytime[0])
    #print(xstart)
    #print(ystart)
    if(xstart>ystart):
        while(ystart<xstart):
            #print("ystar: "+ str(ystart))
            startpos+=1
            ystart+=1
        Y=Y[startpos:]
        ytime=ytime[startpos:]
    elif(ystart>xstart):
        while(xstart<ystart):
            #print("xstart: "+str(xstart))
            startpos+=1
            xstart+=1
        X=X[startpos:]
        xtime = xtime[startpos:]
        
    #size = min(len(X),len(Y))
    #print(startpos)
    #print(X)
    #print(Y)
    #print(str(len(X))+ " "+str(len(Y)))
    print("Correlation: " + str(np.corrcoef(X,Y)[0,1]))
    plt.scatter(X,Y)
    plt.title('Unit Labour Costs vs Inflation for '+ country)
    plt.xlabel("Inflation(CPI)")
    plt.ylabel("Unit Labour Costs(Annual Growth Rate)")
    coef = np.polyfit(X,Y,1)
    poly1d_fn = np.poly1d(coef) 
    plt.plot(X,poly1d_fn(X),'--k')
    plt.show()

def graph_all(country):
    fig,ax = plt.subplots()
    ###################
    #inflation vs time#
    ###################
    plt.subplot(2,2,1)
    c_inflation_data=curate_inflation_data(country)
    c_wage_data=curate_wage_data(country)
    X = c_inflation_data["TIME"].values
    Y = c_inflation_data["Value"].values
    
    itime = c_inflation_data["TIME"].values
    wtime = c_wage_data["TIME"].values
    
    startpos=0
    istart = int(itime[0])
    wstart = int(wtime[0])
    if(wstart>istart):
        while(istart<wstart):
            startpos+=1
            istart+=1
        X=X[startpos:]
        Y=Y[startpos:]
    X=[pd.to_datetime(d) for d in X]
    plt.plot(X,Y)
    plt.xlabel("Year")
    plt.ylabel("Consumer Price Index")
    plt.title('Inflation for '+country)

    ###################
    #  wage vs time   #
    ###################
    plt.subplot(2,2,2)
    c_wage_data=curate_wage_data(country)
    c_inflation_data=curate_inflation_data(country)
    X = c_wage_data["TIME"].values
    Y = c_wage_data["Value"].values
    itime = c_inflation_data["TIME"].values
    wtime = c_wage_data["TIME"].values
    startpos=0
    istart = int(itime[0])
    wstart = int(wtime[0])
    if(istart>wstart):
        while(wstart<istart):
            startpos+=1
            wstart+=1
        X=X[startpos:]
        Y=Y[startpos:]
    X=[pd.to_datetime(d) for d in X]
    plt.plot(X,Y)
    plt.xlabel("Year")
    plt.ylabel("Annual Growth Rate(%)")
    plt.title('Unit labour costs by Employee for '+country)

    ###################
    #inflation vs wage#
    ###################
    plt.subplot(2,2,3)
    c_inflation_data=curate_inflation_data(country)
    c_wage_data=curate_wage_data(country)
    xtime = c_inflation_data["TIME"].values
    ytime = c_wage_data["TIME"].values
    X = c_inflation_data["Value"].values
    Y = c_wage_data["Value"].values
    startpos=0
    xstart = int(xtime[0])
    ystart = int(ytime[0])
    if(xstart>ystart):
        while(ystart<xstart):
            startpos+=1
            ystart+=1
        Y=Y[startpos:]
        ytime=ytime[startpos:]
    elif(ystart>xstart):
        while(xstart<ystart):
            startpos+=1
            xstart+=1
        X=X[startpos:]
        xtime = xtime[startpos:]
    #print("Correlation: " + str(np.corrcoef(X,Y)[0,1]))
    plt.scatter(X,Y)
    plt.title('Unit Labour Costs vs Inflation for '+ country)
    plt.xlabel("Inflation(CPI)")
    plt.ylabel("Unit Labour Costs(Annual Growth Rate)")
    plt.tight_layout()
    coef = np.polyfit(X,Y,1)
    poly1d_fn = np.poly1d(coef)  
    plt.plot(X,poly1d_fn(X),'--k')
    html_str = mpld3.fig_to_html(fig)
    Html_file= open(country+".html","w")
    Html_file.write(html_str)
    Html_file.close()


