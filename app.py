import yfinance as yf
import plotly.graph_objs as pt
import streamlit as st
from datetime import datetime


NAME = 'BTC-USD'
INIT_USD = 100000

if 'usd' not in st.session_state:
    st.session_state.usd = INIT_USD

if 'xrp' not in st.session_state:
    st.session_state.xrp = 0


st.set_page_config(layout='wide')


def get_data():
    return yf.download(tickers=NAME, period='3h', interval='1m')


def deal_history(buy_amount, price, code):
    fw = open("./log.txt", 'a')

    if code == 0: # 구매
        fw.write(str(datetime.now().strftime("%H시 %M분 %S초")) + "\n")
        fw.write(f"BTC {buy_amount}개를 {price:.2f}원에 구매함"+ "\n")

    elif code == 1: # 판매
        fw.write(str(datetime.now().strftime("%H시 %M분 %S초")) + "\n")
        fw.write(f"BTC {buy_amount}개를 {price:.2f}원에 판매함"+ "\n")
    
    fw.close()


    with col3:
        st.header("거래 기록")
        st.header(" ") #Space

        fr = open("./log.txt", "r")

        lines = fr.readlines()
        count = True

        if len(lines) >= 12:
            lines = lines[-10:]
        
        for line in lines:
            if count == True: # subheader
                st.subheader(line)
                count = False

            else:
                st.write(line)
                st.header(" ") #Space
                count = True
    
        fr.close()



data = get_data()

col1, col2 = st.columns([3, 1])
col3, _ = st.columns([1, 3])


# 그래프 레이아웃
with col1:
    st.title("비트코인 가상 거래소")
    st.header(" ") # Space

    current_price = float(data.iloc[-1]['Close'])
    
    st.header('%s %.5f' % (NAME, current_price))

    if st.button('Refresh'):
        data = get_data()

    fig = pt.Figure([pt.Scatter(x=data.index, y=data['Close'])])

    fig.update_layout(height=800)

    st.plotly_chart(fig, use_container_width=True)
    



# 거래 레이아웃
with col2:
    st.header("거래 하기")

    buy_amount = st.number_input("구매 할 갯수 입력", min_value=0, value=0)

    #Buy
    if st.button('구매'):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])

        buy_price = buy_amount * current_price

        if st.session_state.usd >= buy_amount:
            st.session_state.xrp += buy_amount
            st.session_state.usd -= buy_price
            deal_history(buy_amount, buy_price, 0)
        else:
            st.warning("보유 금액이 부족합니다.")
    
    sell_amount = st.number_input("판매 할 갯수 입력", min_value=0, value=0)

    # Sell
    if st.button("판매"):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])

        if st.session_state.xrp >= sell_amount:
            sell_price = sell_amount * current_price
        
            st.session_state.xrp -= sell_amount
            st.session_state.usd += sell_price
            deal_history(buy_amount, sell_price, 1)
        else:
            st.warning("리플이 부족합니다.")


    st.subheader("나의 USD : %.2f" % st.session_state.usd)
    st.subheader("나의 XRP : %d" % st.session_state.xrp)

    # 손익
    total_in_usd = st.session_state.usd + st.session_state.xrp * current_price
    profit = (total_in_usd - INIT_USD) / INIT_USD * 100
    st.subheader("손익 : %.2f%%" % profit)

