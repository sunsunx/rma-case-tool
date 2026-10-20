import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
	page_title="RMA/RTV Case Management Tool",
	layout="wide",
)

st.markdown(
	"""
	<style>
	h1{
		font-size: 50px !important;
	}

	h2{
		font-size: 40px !important;
	}

	h3{
		font-size: 30px !important;
	}

	</style>
	""",
	unsafe_allow_html=True
)


st.title("RMA/RTV Case Management Tool")
conn=sqlite3.connect("rma_rtv.db")

df=pd.read_sql_query(
	"SELECT * FROM cases", conn
)

st.subheader("Case Summary")

col1,col2,col3,col4=st.columns(4)

col1.metric("Total Cases", len(df))
col2.metric("RMA Cases",(df["CaseType"]=="RMA").sum())
col3.metric("RTV Cases",(df["CaseType"]=="RTV").sum())
col4.metric("Total Return Value",f"{df['ReturnValue'].sum():,.2f}")


#bar_chart: case status
status_counts=(
	df["Status"]
	.value_counts()
	.reset_index()
)

status_counts.columns=["Status","CaseCount"]

fig_status=px.bar(
	status_counts,
	x="CaseCount",
	y="Status",
	orientation="h",
	text="CaseCount",
	title="Cases by Status"
)

fig_status.update_traces(
    marker_color="#123B66",
    texttemplate="%{text:,.0f}",
    textposition="inside"
)

fig_status.update_layout(
	xaxis_title="Number of Cases",
	yaxis_title="",
	height=350
)

#bar_chart: RMA/RTV cost
return_value_by_type = (
    df.groupby("CaseType")["ReturnValue"]
      .sum()
      .reset_index()
)

fig_value = px.bar(
    return_value_by_type,
    x="ReturnValue",
    y="CaseType",
	orientation="h",
    text="ReturnValue",
    title="Return Value by Case Type"
)

fig_value.update_traces(
    marker_color="#123B66",
    texttemplate="%{text:,.2f}",
    textposition="inside"
)

fig_value.update_layout(
    xaxis_title="Return Value",
    yaxis_title="Case Type",
    height=350
)


#Display charts side by side
chart_col1,chart_col2=st.columns(2)
with chart_col1: 
	st.plotly_chart(
		fig_status,
		use_container_width=True
		)

with chart_col2:
	st.plotly_chart(
		fig_value,
		use_container_width=True
		)


#filter

st.subheader("Filter Cases")

case_type=st.selectbox("Case Type",["All","RMA","RTV"])

status=st.selectbox("Status",["All","Open","In Progress","Closed"])

filtered_df=df.copy()

#casetype
if case_type != "All":
	filtered_df=filtered_df[filtered_df["CaseType"]==case_type]

#case status
if status !="All":
	filtered_df=filtered_df[filtered_df["Status"]==status]

#caseID
search_case=st.text_input(
	"Search Case ID",
	placeholder="e.g. Case00016"
)

if search_case:filtered_df=filtered_df[
	filtered_df["CaseID"].str.contains(
		search_case,
		case=False,
		na=False
)
]


st.subheader("Case List")

display_df=filtered_df[
	["CaseID",
	 "InvoiceNo",
	 "CaseType",
	 "Status",
	 "Priority",
	 "ProcessingDays",
	 "ReturnValue"
]
].reset_index(drop=True)

st.dataframe(display_df)

if search_case:
	detail_df=df[
	df["CaseID"].str.lower()
	==search_case.strip().lower()
	]
	
	if detail_df.empty:
		st.warning("Case ID not found.")
	else:
		st.subheader("Case Details")
		
		st.dataframe(
			detail_df[
				[                   
				 "InvoiceNo",
                    		 "StockCode",
                    		 "CaseType",
                    		 "Status",
                    		 "ProcessingDays",
                    		 "ReturnQty",
                    		 "ReturnValue"
				]
			].reset_index(drop=True)

		)
