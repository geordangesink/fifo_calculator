from pandas import *

csv_spot = read_csv("INSERT PATH")
csv_isolated_margin = read_csv("INSERT PATH")
csv_cross_margin = 0#ADD FILE HERE
csv_futures = read_csv("INSERT PATH")
csv_bot = read_csv("INSERT PATH")
csv_liquidation_isolated = read_csv("INSERT PATH")
csv_liquidation_cross = 0#ADD FILE HERE


print("____________________________________________________________________________")



"""
MAKE A CLASS FOR EACH COIN
ADD LIQUIDATIONS
"""

def profit(financial_tool, name, coin_pair):
#calculate buy costs and sell costs
    #some csv has "Avg. Filled Price", others "Filled Price" as columns
    try:
        avg_filled_price = financial_tool["Avg. Filled Price"].tolist()
    except (KeyError):
        avg_filled_price = financial_tool["Filled Price"].tolist()

    try:
        dates = financial_tool["Filled Time(UTC)"].tolist()
    except(KeyError):
        dates = financial_tool["Time Filled(UTC)"].tolist()

    filled_amount = financial_tool["Filled Amount"].tolist()

    side = financial_tool["Side"].tolist()

    symbol = financial_tool["Symbol"].tolist()

    fees = financial_tool["Fee"].tolist()

    #for futures
    if name == "Futures":
        filled_value = financial_tool["Filled Value"].tolist()
        for i in range(len(avg_filled_price)):
            filled_amount[i] = abs(filled_value[i]) / avg_filled_price[i]
    
    sell_coins_amount = []
    sell_coins_price = []
    buy_coins_amount = []
    buy_coins_price = []

    open_buy_amount = []
    open_buy_price = []
    open_sell_amount = []
    open_sell_price = []
    open_buy_amount_total = 0
    open_sell_amount_total = 0
    counter = 0
    fee = 0

    avg_buy_price = 0
    avg_sell_price = 0
    avg_sell_amount = 0
    avg_buy_amount = 0
    
    #ADD DATES FOR LIQUIDATION
    ######################MAKE IT WORK FOR CROSS MARGIN TOO###########################MAYBE WRITE IN BINARY SEARCH##########################
    if filled_amount == csv_isolated_margin["Filled Amount"].tolist():
        #see where liquidation took place in respect to trades
        liquidation_dates = csv_liquidation_isolated["End Time"].tolist()
        liquidation_amount = csv_liquidation_isolated["Amount"].tolist()
        liquidation_volume = csv_liquidation_isolated["Total Asset Value"].tolist()
        liquidation_pair = csv_liquidation_isolated["Pair"].tolist()

        for x in range(len(liquidation_dates)):
            if liquidation_pair[x] == coin_pair:
                liquidation_date_int = int(liquidation_dates[x][0] + liquidation_dates[x][1] + liquidation_dates[x][2] + liquidation_dates[x][3] 
                                           + liquidation_dates[x][5] + liquidation_dates[x][6] + liquidation_dates[x][8] + liquidation_dates[x][9] 
                                           + liquidation_dates[x][11] + liquidation_dates[x][12] + liquidation_dates[x][14] + liquidation_dates[x][15])
                index = 0
                for i in range(len(dates)):
                    if int(dates[i][0] + dates[i][1] + dates[i][2] + dates[i][3] 
                           + dates[i][5] + dates[i][6] + dates[i][8] + dates[i][9] 
                           + dates[i][11] + dates[i][12] + dates[i][14] + dates[i][15]) < liquidation_date_int:
                        index += 1
                    else:
                        break
                filled_amount.insert(index, float(liquidation_amount[x]))
                avg_filled_price.insert(index, float(liquidation_volume[x]) / float(liquidation_amount[x]))
                side.insert(index, "SELL")
                symbol.insert(index, coin_pair) ##########MAKE IT WORK AUTOMATICALLY###############
                fees.insert(index, 0)

            else:
                None    


    #split into Sell and Buy######################################
    for i in range(len(side)):
        side[i] = str(side[i])
        side[i] = side[i].lower()

        if coin_pair == symbol[i]:
            fee += fees[i]

                #one pair (coin amount/coin price) for each row (eg. sell_coins_amount[1] and sell_coins_price[1] are one pair)
            if side[i] == "sell":
                for s in range(int(filled_amount[i])):
                    sell_coins_amount.append(1)
                    sell_coins_price.append(avg_filled_price[i])

                    avg_sell_price += avg_filled_price[i]
                    avg_sell_amount += 1
                if (filled_amount[i] % 1) != 0:
                    sell_coins_amount.append((filled_amount[i] % 1))
                    sell_coins_price.append(avg_filled_price[i])

                    avg_sell_price += avg_filled_price[i] * (filled_amount[i] % 1)
                    avg_sell_amount += filled_amount[i] % 1
                else:
                    None
            else:
                for b in range(int(filled_amount[i])):
                    buy_coins_amount.append(1)
                    buy_coins_price.append(avg_filled_price[i])

                    avg_buy_price += avg_filled_price[i]
                    avg_buy_amount += 1
                if (filled_amount[i] % 1) != 0:
                    buy_coins_amount.append((filled_amount[i] % 1))
                    buy_coins_price.append(avg_filled_price[i])

                    avg_buy_price += avg_filled_price[i] * (filled_amount[i] % 1)
                    avg_buy_amount += filled_amount[i] % 1
                else:
                    None

        else:
            None

    ###################THIS TEST SHOWS IF OPEN BUY/SELL AMOUNT IS MISSING ##########################
    # sell = 0
    # buy = 0
    # sell_1 = 0
    # buy_1 = 0

    # for i in range(len(sell_coins_amount)):
    #     sell_1 += sell_coins_amount[i]
    
    # for i in range(len(buy_coins_amount)):
    #     buy_1 += buy_coins_amount[i]

    # for i in range(len(sell_test)):
    #     sell += sell_test[i]

    # for i in range(len(buy_test)):
    #     buy += buy_test[i]
                
    # print(buy)
    # print(sell)
    # print(buy_1)
    # print(sell_1)
    ###############################################################################################
    try:
        avg_buy_price = avg_buy_price / avg_buy_amount
        avg_sell_price = avg_sell_price / avg_sell_amount
    except(ZeroDivisionError):
        None



    if len(sell_coins_amount) <= len(buy_coins_amount):
        length = len(sell_coins_amount)

    elif len(sell_coins_amount) > len(buy_coins_amount):
        length = len(buy_coins_amount)
        
    pnl = [] #####FRACTIONS
    for i in range(length + 1): #Whole assets
        
        try:
            left_over_buy = buy_coins_amount[i]
        except(IndexError):
            None
        try:
            left_over_sell = sell_coins_amount[i]
        except(IndexError):
            None

        try:
            if sell_coins_amount[i] > buy_coins_amount[i]:

                left_over_sell = sell_coins_amount[i] - buy_coins_amount[i]

                pnl.append((buy_coins_amount[i] * sell_coins_price[i]) 
                        - (buy_coins_amount[i] * buy_coins_price[i]))
                
                buy_coins_amount[i] = 0

            #open short possitions
            
                if buy_coins_amount[i+1] >= left_over_sell:

                    buy_coins_amount[i+1] -= left_over_sell

                    pnl.append((left_over_sell * sell_coins_price[i])
                                - (left_over_sell * buy_coins_price[i+1])) 
                    
                    left_over_sell = 0
                       

                else:
                    while buy_coins_amount[i+1+counter] < left_over_sell:
                        left_over_sell -= buy_coins_amount[i+1+counter]

                        pnl.append((buy_coins_amount[1+i+counter] * sell_coins_price[i])
                                - (buy_coins_amount[1+i+counter] * buy_coins_price[i+1+counter]))
                        
                        buy_coins_amount[i+1+counter] = 0
                        counter += 1

                        if buy_coins_amount[i+1+counter] >= left_over_sell:
                            buy_coins_amount[i+1+counter] -= left_over_sell

                            pnl.append((left_over_sell * sell_coins_price[i])
                                - (left_over_sell * buy_coins_price[i+1]))
                        
                            left_over_sell = 0 #only will be 0 when the latest buy_coins_amount = lef_over_sell
                            counter = 0
                            break
                    
        except(IndexError):
            try:
                sell_coins_amount[i]
                sell_coins_amount[i] = left_over_sell #makes sense, look coment above

                for x in range(len(sell_coins_amount) - i):
                    open_sell_amount.append(sell_coins_amount[i+x])
                    open_sell_price.append(sell_coins_price[i+x])
            except(IndexError):
                None
        try:
            if sell_coins_amount[i] < buy_coins_amount[i]:

                left_over_buy = buy_coins_amount[i] - sell_coins_amount[i]

                pnl.append((sell_coins_amount[i] * sell_coins_price[i]) 
                        - (sell_coins_amount[i] * buy_coins_price[i]))
                
                sell_coins_amount[i] = 0

            #open long possitions
            
                if sell_coins_amount[i+1] >= left_over_buy:

                    sell_coins_amount[i+1] -= left_over_buy

                    pnl.append((left_over_buy * sell_coins_price[i])
                                - (left_over_buy * buy_coins_price[i+1]))
                    
                    left_over_buy = 0
                       

                else:
                    while sell_coins_amount[i+1+counter] < left_over_buy:
                        left_over_buy -= sell_coins_amount[i+1+counter]

                        pnl.append((sell_coins_amount[1+i+counter] * sell_coins_price[i])
                                - (sell_coins_amount[1+i+counter] * buy_coins_price[i+1+counter]))
                        
                        sell_coins_amount[i+1+counter] = 0
                        counter += 1

                        if sell_coins_amount[i+1+counter] >= left_over_buy:
                            sell_coins_amount[i+1+counter] -= left_over_buy

                            pnl.append((left_over_buy * sell_coins_price[i])
                                - (left_over_buy * buy_coins_price[i+1]))
                        
                            left_over_buy = 0 #only will be 0 when the latest buy_coins_amount = lef_over_sell
                            counter = 0
                            break       

        except(IndexError):
            try:
                buy_coins_amount[i]
                buy_coins_amount[i] = left_over_buy #makes sense, look coment above

                for x in range(len(buy_coins_amount) - i):
                    open_buy_amount.append(buy_coins_amount[i+x])
                    open_buy_price.append(buy_coins_price[i+x])

            except(IndexError):
                None

        try:
            if sell_coins_amount[i] == buy_coins_amount[i]:
                pnl.append((sell_coins_price[i] * sell_coins_amount[i]) - (buy_coins_price[i] * buy_coins_amount[i]))
                sell_coins_amount[i] = 0
                buy_coins_amount[i] = 0

        except(IndexError):
            None

        
        #EXPERIMENTAL################################################# (open buy and sell amount)
        # try:
        #     sell_coins_amount[i]
        # except(IndexError):
        #     try:
        #         open_buy_amount.append(buy_coins_amount[i])
        #         open_buy_price.append(buy_coins_price[i])
        #     except(IndexError):
        #         None
        
        # try:
        #     buy_coins_amount[i]
        # except(IndexError):
        #     try:
        #         open_sell_amount.append(sell_coins_amount[i])
        #         open_sell_price.append(sell_coins_price[i])
        #     except(IndexError):
        #         None
        #EXPERIMENTAL################################################
                

    #add all profits
    total_pnl = 0
    for i in range(len(pnl)):
        total_pnl += pnl[i]

    #Fees

    # total_pnl -= fee                ######################################    ALREADY DEDUCTED????????????   ########################################

    #open positions

    for i in range(len(open_buy_amount)):
        open_buy_amount_total += open_buy_amount[i]

    for i in range(len(open_sell_amount)):
        open_sell_amount_total += open_sell_amount[i]

    #print financetool-individual data
    print( name, "PNL: ", total_pnl)
    print( "     of which are fees: -", fee)
    print( "     open buy amount: ", open_buy_amount_total) ##################### DOESNT WORK WHEN CHANGING BETWEEN TOOLS    #################
    print( "     open sell amount: ", open_sell_amount_total)#################################################################################
    print( "     avg buy price: ", avg_buy_price)
    print( "     avg sell price: ", avg_sell_price)

    return total_pnl


anual_profit = profit(csv_isolated_margin, "Isolated Margin", "INSERT TRADING PAIR") + profit(csv_futures, "Futures", "INSERT TRADING PAIR") + profit(csv_bot, "Trading Bot","INSERT TRADING PAIR") + profit(csv_spot, "Spot", "INSERT TRADING PAIR")

print("TOTAL_PROFIT: ", anual_profit)
print("____________________________________________________________________________")


##################   SPOT PNL IS TOO HIGH AS WELL AS OPEN SELL AMOUNT FOR MYR O SPOT   ##################################################