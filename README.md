# fifo_calculator
What this program takes into account:

    FIFO (first in first out)

    Fractual Assets
    
    open long/short positions

    coin fees


What it doesnt account for:

    using multiple exchanges (you need to make sure the transactions are ordered in the correct time line)


What you need:

    seperate .csv file for every financial tool used (futures, spot, margin, trading bots ect)

    "Side" column ("buy" or "sell", casing doesnt matter)

    "Avg. Filled Price" or "Filled Price" column containing the average filled price per order 

    "Filled Amount" column that contains the filled amount per order

    "Fee" column that contains the Fees in USDT per order

    "Symbol" column that has the symbol of the trading pair


Limitations:

    Only works for USDT or similar trading pairs (the output value is the profite/loss of the counter trainding pair)

    open buy/sell amounts can fluctuate insignificantly due to pythons remainder roundings

    profit output can fluctutate from actual in miniscule amounts due to pythons remainder roundings

    THESE LIMITATIONS ARE ONLY WHEN THERE ARE FRACTUAL AMOUNTS AND NOT WHOLE COINS 
    (as long as you dont trade obscurely high amounts in only fractual transactions you should be fine)




