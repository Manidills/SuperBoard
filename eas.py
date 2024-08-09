import streamlit as st
import pandas as pd
import altair as alt

from eas_graph import eas_graph



def eas():
    st.markdown("##")
    st.markdown("# Ethereum Attestation Service (EAS)")
    st.markdown("##")

    
    action = st.radio("Select protocol",['EAS','EAS_GRAPH'], horizontal=True)


    if action == 'EAS':
        st.markdown("##")
        st.markdown("## EAS Across Chains")
        st.markdown("##")

        a,b = st.columns([4,2])

        with a:
            st.metric("Total Schemas", 1517)
            st.metric("registerers", 416)
        with b:
            st.metric("revocable",1163)
            st.metric("non-revocable", 354)
        st.markdown("##")


        
        
        df = pd.read_csv("SDK_data/EAS/daily_att.csv")
        df_1 = pd.read_csv("SDK_data/EAS/weekly_att.csv")
        df['block_time'] = pd.to_datetime(df['block_time'])
        df_1['block_time'] = pd.to_datetime(df_1['block_time'])

        a,b = st.columns([2,2])

        with a:
            # Creating the multi-area graph (stacked area chart)
            st.altair_chart(
                alt.Chart(df).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('total:Q', stack=None, title='total'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('attested_schemas:Q', stack=None, title='attested_schemas'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('unique_attesters:Q', stack=None, title='unique_attesters'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('unique_recipients:Q', stack=None, title='unique_recipients'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.data_editor(pd.read_csv('SDK_data/EAS/eas_chain.csv'))
        with b:
            st.altair_chart(
                alt.Chart(df_1).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('total:Q', stack=None, title='total'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df_1).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('attested_schemas:Q', stack=None, title='attested_schemas'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df_1).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('unique_attesters:Q', stack=None, title='unique_attesters'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.altair_chart(
                alt.Chart(df_1).mark_line().encode(
                    x=alt.X('block_time:T', title='Time'),
                    y=alt.Y('unique_recipients:Q', stack=None, title='unique_recipients'),
                    color=alt.Color('blockchain:N', legend=alt.Legend(title='Chain')),
                    tooltip=['time:T', 'Chain:N', 'txns:Q']
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
            st.data_editor(pd.read_csv('SDK_data/EAS/schema_stats.csv'))

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/top_100_eas.csv'))
        st.markdown("##")



        st.markdown("##")
        st.markdown("## EAS Optimisim")
        st.markdown("##")

        a,b = st.columns([4,2])

        with a:
            st.metric("Total Schemas", 530)
            st.metric("Number of Attestations onchain", 410507)
        with b:
            st.metric("Unique Creators",160)
            st.metric("Total Attesters onchain", 11091)

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/Optimisim_number_of_att.csv'), width=1200)

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/optimisim_schemas.csv'), width=1200)

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/optimisim_distribution_of_att.csv'), width=1200)

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/top_10_op.csv'), width=1200)


        st.markdown("##")
        st.markdown(f"##  passport.gitcoin.co [Optimisim] ")
        st.markdown("##")

        a,b = st.columns([4,2])

        with a:
            st.metric("Number of Gitcoin Passport Stamps V1 onchain", 63161)    
        with b:
            st.metric("Number of Gitcoin Passport Stamps Recipients", 48394)

        df = pd.read_csv("SDK_data/EAS/passport_cumulative_att.csv")
        df['Day'] = pd.to_datetime(df['Day'])
        st.altair_chart(
                alt.Chart(df).mark_area(color='azure', opacity=0.4).encode(
                    x=alt.X('Day:T', title='Time'),
                    y=alt.Y('# Attestations:Q', stack=None, title='AVG Attestations')
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
        
        df = pd.read_csv("SDK_data/EAS/passport_daily_att.csv")
        df['Day'] = pd.to_datetime(df['Day'])
        st.altair_chart(
                alt.Chart(df).mark_area(color='yellow', opacity=0.4).encode(
                    x=alt.X('Day:T', title='Time'),
                    y=alt.Y('# Attestations:Q', stack=None, title='Daily Attestations')
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )
        
        
        df = pd.read_csv("SDK_data/EAS/passport_montly_unique_att.csv")
        df['Month'] = pd.to_datetime(df['Month'])
        st.altair_chart(
                alt.Chart(df).mark_area(color='blueviolet', opacity=0.4).encode(
                    x=alt.X('Month:T', title='Time'),
                    y=alt.Y('# Recipients:Q', stack=None, title='# Recipients')
                ).properties(
                    width=800,
                    height=400
                ),
                use_container_width=True
            )


        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/passport_recepite_scores.csv'), width=1200)

        st.markdown("##")
        st.data_editor(pd.read_csv('SDK_data/EAS/passport_recepite_stamps.csv'), width=1200)


    elif action == "EAS_GRAPH":
        eas_graph()
