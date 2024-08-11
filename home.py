import streamlit as st
import pandas as pd
import altair as alt
import g4f



def chat_bot(prompt):
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.default,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    return response


@st.cache_resource
def generate_summary(df,category):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here Superchain & Optimism Stack {category} data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences"
    st.write(chat_bot(prompt))


def home():
    st.markdown("##")

    a,b,c = st.columns([2,2,2])

    with a:
        st.metric("Total Transactions (Layer3 OP Quests)", '17,666,559')
    with b:
        st.metric("Total Users (Layer3 OP Quests)", '683,754')
    with c:
        st.metric("Total Transaction Fees (Layer3 OP Quests)", '$2,098,564' )

    df = pd.read_csv("SDK_data/Superchain Transactions.csv")

    df['evt_day'] = pd.to_datetime(df['evt_day'])

    # Chart title and description
    st.markdown("# Superchain & OP Stack Analytics")
    st.markdown("##")

    st.markdown("## Transactions")
    st.markdown("##")

    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('evt_day:T', title='Time'),
            y=alt.Y('op_transactions:Q', stack=None, title='op_transactions'),
            color=alt.Color('Chain:N', legend=alt.Legend(title='Chain')),
            tooltip=['time:T', 'Chain:N', 'txns:Q']
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )


    st.dataframe(pd.read_csv("SDK_data/Gas_per_Txn_Superchain.csv"), width=1200)

    st.markdown("##")

    generate_summary(df,'transactions')
    

    st.markdown("## Addresses : New addresses, Active addresses")
    st.markdown("##")
    a,b = st.columns([2,2])

    with a:
        st.altair_chart(
        alt.Chart(df).mark_circle().encode(
            x=alt.X('evt_day:T', title='Time'),
            y=alt.Y('Active_Addresses:Q', stack=None, title='Active_Addresses'),
            color=alt.Color('Chain:N', legend=alt.Legend(title='Chain')),
            tooltip=['time:T', 'Chain:N', 'txns:Q']
        ).properties(
            width=800,
            height=400,
            title='Active_Addresses'
        ),
        use_container_width=True
    )
        
    with b:
        df = pd.read_csv("SDK_data/New_addresses.csv")

        df['month_cohort'] = pd.to_datetime(df['month_cohort'])

        st.altair_chart(
        alt.Chart(df).mark_circle().encode(
            x=alt.X('month_cohort:T', title='Time'),
            y=alt.Y('total_users:Q', stack=None, title='total_users'),
            color=alt.Color('chain:N', legend=alt.Legend(title='Chain')),
            tooltip=['time:T', 'Chain:N', 'txns:Q']
        ).properties(
            width=800,
            height=400,
            title='New_Addresses'
        ),
        use_container_width=True
    )
        
    st.markdown("##")

    df = pd.read_csv("SDK_data/ETH_volume.csv")

    df['day'] = pd.to_datetime(df['day'])

    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('eth_volume:Q', stack=None, title='eth_volume'),
            color=alt.Color('chain:N', legend=alt.Legend(title='Chain')),
            tooltip=['time:T', 'Chain:N', 'txns:Q']
        ).properties(
            width=800,
            height=400,
            title='Daily ETH Tansfer Volume Base VS Optimism'
        ),
        use_container_width=True
    )
    st.markdown("##")

    st.markdown("## Economics : Marketcap, L2 Revenue, Volume, Profit 💲s")
    st.markdown("##")


    st.markdown("##")

    df = pd.read_csv("SDK_data/marketcap.csv")
    # df['date'] = pd.to_datetime(df['date'])

    st.altair_chart(
        alt.Chart(df).mark_area(color='red',opacity=0.4).encode(
            x=alt.X('date:T', title='Time'),
            y=alt.Y('market_caps:Q', stack=None, title='market_caps')
        ).properties(
            width=800,
            height=400,
            title='Superchain & OP Stack Marketcap'
        ),
        use_container_width=True
    )

    st.markdown("##")
    st.altair_chart(
        alt.Chart(df).mark_area(color='yellow', opacity=0.4).encode(
            x=alt.X('date:T', title='Time'),
            y=alt.Y('total_volumes:Q', stack=None, title='total_volumes')
        ).properties(
            width=800,
            height=400,
            title='Superchain & OP Stack total_volumes'
        ),
        use_container_width=True
    )

    st.markdown("##")

    a,b = st.columns([2,2])
    df_base = pd.read_csv("SDK_data/base_revenue.csv")
    df_blast = pd.read_csv("SDK_data/Blast_revenue.csv")
    df_optimisim = pd.read_csv("SDK_data/optimism_reveue.csv")
    df_mantle = pd.read_csv("SDK_data/mantle_revenue.csv")

    with a:
        
        df_base['evt_day'] = pd.to_datetime(df_base['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_base).mark_area(color='rosybrown').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_l2_rev_usd:Q', stack=None, title='cumulative_l2_rev_usd'),
            ).properties(
                width=800,
                height=400,
                title='Base L2 AVG Revenue'
            ),
            use_container_width=True
        )

        df_blast['evt_day'] = pd.to_datetime(df_blast['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_blast).mark_area(color='dimgray').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_l2_rev_usd:Q', stack=None, title='cumulative_l2_rev_usd'),
            ).properties(
                width=800,
                height=400,
                title='Blast L2 AVG Revenue'
            ),
            use_container_width=True
        )

        df_optimisim['evt_day'] = pd.to_datetime(df_optimisim['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_optimisim).mark_area(color='green').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_l2_rev_usd:Q', stack=None, title='cumulative_l2_rev_usd'),
            ).properties(
                width=800,
                height=400,
                title='Optimisim L2 AVG Revenue'
            ),
            use_container_width=True
        )

        
    with b:

        df_base['evt_day'] = pd.to_datetime(df_base['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_base).mark_bar(color='rosybrown').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_margin_usd:Q', stack=None, title='cumulative_margin_usd'),
            ).properties(
                width=800,
                height=400,
                title='Base Profit'
            ),
            use_container_width=True)
        
        df_blast['evt_day'] = pd.to_datetime(df_blast['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_blast).mark_bar(color='dimgray').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_margin_usd:Q', stack=None, title='cumulative_margin_usd'),
            ).properties(
                width=800,
                height=400,
                title='Blast Profit'
            ),
            use_container_width=True)
        
        df_optimisim['evt_day'] = pd.to_datetime(df_optimisim['evt_day'])

        # Creating the multi-area graph (stacked area chart)
        st.altair_chart(
            alt.Chart(df_optimisim).mark_bar(color='green').encode(
                x=alt.X('evt_day:T', title='Time'),
                y=alt.Y('cumulative_margin_usd:Q', stack=None, title='cumulative_margin_usd'),
            ).properties(
                width=800,
                height=400,
                title='Optimisim Profit'
            ),
            use_container_width=True)
        

    st.markdown("##")

    st.markdown("## L3 Leaderboard")
    st.markdown("##")

    st.data_editor(pd.read_csv('SDK_data/L3_leaderboard.csv'), width=1200)

    st.markdown("##")
    st.markdown("## NFTs Mints")
    st.markdown("##")

    df = pd.read_csv("SDK_data/nft_mints.csv")

    df['block_date'] = pd.to_datetime(df['block_date'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('block_date:T', title='Time'),
            y=alt.Y('mint_count:Q', stack=None, title='mint_count'),
            color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
            tooltip=['time:T', 'Chain:N', 'txns:Q']
        ).properties(
            width=800,
            height=400,
            title='Mint Counts'
        ),
        use_container_width=True
    )
    generate_summary(df, 'nft mints')

    st.markdown("##")
    st.markdown("## Contracts")
    st.markdown("##")
    st.data_editor(pd.read_csv('SDK_data/contracts.csv'), width=1200)


        
       







        