import ast
import os
from flask import Flask, render_template, request, redirect, jsonify, flash, send_from_directory
import pandas as pd
import requests
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'amatuer analysts'

rating_df = pd.read_csv('rating_counts_final.csv')
sentiment_df = pd.read_csv('Sentiment.csv')
summary_df = pd.read_csv('Final_Keywords_Summarization.csv')
price_sentiment_df = pd.read_csv('price_sentiment.csv')
quality_sentiment_df = pd.read_csv('quality_sentiment.csv')
service_sentiment_df = pd.read_csv('service_sentiment.csv')
effect_sentiment_df = pd.read_csv('effect_sentiment.csv')
states_df = pd.read_csv('states.csv')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index3.html')


@app.route('/analysis', methods=['GET', 'POST'])
def showAnalysis():
    product_data = {}
    plot_html = None
    plot_html_states = None
    plot_html_rating = None
    plot_html_sentiment = None
    plot_html_price_sentiment = None
    plot_html_quality_sentiment = None
    plot_html_service_sentiment = None
    plot_html_effect_sentiment = None
    if request.method == 'POST':
        product_name = request.form['product_name']
        if product_name:
            summary = summary_df[summary_df['PRODUCT_NAME'] == product_name]
            ratings = rating_df[rating_df['PRODUCT_NAME'] == product_name]
            sentiments = sentiment_df[sentiment_df['PRODUCT_NAME'] == product_name]
            price_sentiments = price_sentiment_df[price_sentiment_df['PRODUCT_NAME'] == product_name]
            quality_sentiments = quality_sentiment_df[quality_sentiment_df['PRODUCT_NAME'] == product_name]
            effect_sentiments = effect_sentiment_df[effect_sentiment_df['PRODUCT_NAME'] == product_name]
            service_sentiments = service_sentiment_df[service_sentiment_df['PRODUCT_NAME'] == product_name]
            state_frequencies = states_df[states_df['PRODUCT_NAME'] == product_name]
            try:
                state_dict = ast.literal_eval(state_frequencies['State'].values[0])
                print(state_dict)
                if isinstance(state_dict, dict):
                    # Sort the dictionary based on values and select the top 5 items
                    state_dict = dict(sorted(state_dict.items(), key=lambda item: item[1], reverse=True)[:5])
                    print(state_dict)
                else:
                    print("Error: 'state_dict' is not a dictionary.")
                state_df = pd.DataFrame(list(state_dict.items()), columns=['State', 'Reviews'])

                # Use px.bar with the DataFrame
                fig = px.bar(state_df, x='State', y='Reviews', color='State')

                # Customize the layout if needed
                fig.update_layout(xaxis_title='State', yaxis_title='Reviews', height=500, width=800)

                # Convert the plot to HTML
                plot_html_states = pio.to_html(fig, full_html=False)
                # Show the plot
            except (SyntaxError, ValueError, IndexError) as e:
                print(f"Error: {e}")

            if summary.empty or ratings.empty or sentiments.empty:
                flash('Product Not Found')
                return render_template('analysis.html', data=product_data)

            service = summary['Service Summary'].values[0]
            price = summary['Price Summary'].values[0]
            effect = summary['Effect Summary'].values[0]
            quality = summary['Quality Summary'].values[0]
            rating = [ratings['5 star'].values[0], ratings['4 star'].values[0],
                      ratings['3 star'].values[0],
                      ratings['2 star'].values[0], ratings['1 star'].values[0]]
            sentiment_data = [sentiments['sentiment_positive_num'].values[0],
                              sentiments['sentiment_neutral_num'].values[0],
                              sentiments['sentiment_negative_num'].values[0]]

            if not price_sentiments.empty:
                price_sentiment_data = [price_sentiments['sentiment_price_positive_num'].values[0],
                                        price_sentiments['sentiment_price_neutral_num'].values[0],
                                        price_sentiments['sentiment_price_negative_num'].values[0]]
                # Price Sentiment subplot
                plot_data = {'Value': price_sentiment_data, 'Category': ['Positive', 'Neutral', 'Negative']}

                color_map = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
                fig = px.bar(plot_data, x='Value', y='Category', orientation='h', color='Category',
                             color_discrete_map=color_map)

                # Customize the layout if needed
                fig.update_layout(xaxis_title='Number', yaxis_title='Sentiment', height=300, width=500)

                # Convert the plot to HTML
                plot_html_price_sentiment = pio.to_html(fig, full_html=False)

            if not quality_sentiments.empty:

                quality_sentiment_data = [quality_sentiments['sentiment_quality_positive_num'].values[0],
                                      quality_sentiments['sentiment_quality_neutral_num'].values[0],
                                      quality_sentiments['sentiment_quality_negative_num'].values[0]]

                plot_data = {'Value': quality_sentiment_data, 'Category': ['Positive', 'Neutral', 'Negative']}

                color_map = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
                fig = px.bar(plot_data, x='Value', y='Category', orientation='h', color='Category',
                             color_discrete_map=color_map)

                # Customize the layout if needed
                fig.update_layout(xaxis_title='Number', yaxis_title='Quality', height=300, width=500)

                # Convert the plot to HTML
                plot_html_quality_sentiment = pio.to_html(fig, full_html=False)

            if not service_sentiments.empty:

                service_sentiment_data = [service_sentiments['sentiment_service_positive_num'].values[0],
                                          service_sentiments['sentiment_service_neutral_num'].values[0],
                                          service_sentiments['sentiment_service_negative_num'].values[0]]

                plot_data = {'Value': service_sentiment_data, 'Category': ['Positive', 'Neutral', 'Negative']}

                color_map = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
                fig = px.bar(plot_data, x='Value', y='Category', orientation='h', color='Category',
                             color_discrete_map=color_map)

                # Customize the layout if needed
                fig.update_layout(xaxis_title='Number', yaxis_title='Service', height=300, width=500)

                # Convert the plot to HTML
                plot_html_service_sentiment = pio.to_html(fig, full_html=False)

            if not effect_sentiments.empty:
                effect_sentiment_data = [effect_sentiments['sentiment_effect_positive_num'].values[0],
                                          effect_sentiments['sentiment_effect_neutral_num'].values[0],
                                          effect_sentiments['sentiment_effect_negative_num'].values[0]]

                plot_data = {'Value': effect_sentiment_data, 'Category': ['Positive', 'Neutral', 'Negative']}

                color_map = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
                fig = px.bar(plot_data, x='Value', y='Category', orientation='h', color='Category',
                             color_discrete_map=color_map)

                # Customize the layout if needed
                fig.update_layout(xaxis_title='Number', yaxis_title='Effect', height=300, width=500)

                # Convert the plot to HTML
                plot_html_effect_sentiment = pio.to_html(fig, full_html=False)

            product_data = {
                "product_name": product_name,
                "rating": rating,
                "service": service,
                "price": price,
                "effect": effect,
                "quality": quality,
            }

            plot_data = {'Value': rating, 'Category': ['5 star', '4 star', '3 star', '2 star', '1 star']}
            fig = px.bar(plot_data, x='Value', y='Category', orientation='h')

            # Customize the layout if needed
            fig.update_layout(xaxis_title='Number', yaxis_title='Rating', height=500, width=800)

            # Convert the plot to HTML
            plot_html_rating = pio.to_html(fig, full_html=False)

            # Sentiment Plot
            plot_data = {'Value': sentiment_data, 'Category': ['Positive', 'Neutral', 'Negative']}

            color_map = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
            fig = px.bar(plot_data, x='Value', y='Category', orientation='h', color='Category',
                         color_discrete_map=color_map)

            # Customize the layout if needed
            fig.update_layout(xaxis_title='Percentage', yaxis_title='Sentiment', height=500, width=800)

            # Convert the plot to HTML
            plot_html_sentiment = pio.to_html(fig, full_html=False)


        print(product_data)
        return render_template('analysis.html', data=product_data, plot_rating=plot_html_rating,
                               plot_sentiment=plot_html_sentiment, plot_price_sentiment=plot_html_price_sentiment,
                               plot_quality_sentiment=plot_html_quality_sentiment, plot_service_sentiment=plot_html_service_sentiment,
                               plot_effect_sentiment=plot_html_effect_sentiment, plot_states=plot_html_states)

    return render_template('analysis.html', data=product_data)


@app.route('/lda')
def show_lda():
    return render_template('lda_visualization.html')

@app.route('/download/<filename>')
def download_file(filename):
    # Replace 'downloads' with the actual directory where your file is stored
    filepath = os.path.join('D:/Advay/MLProjects/ReviewAnalysis/ProductAnalysisWebsite', filename)

    # Check if file exists before sending
    if not os.path.exists(filepath):
        return 'File not found!', 404

    # Send the file with appropriate headers
    return send_from_directory('D:/Advay/MLProjects/ReviewAnalysis/ProductAnalysisWebsite', filename, as_attachment=True)

app.run(debug=True)

# Add the sentiment interactive plot per product
# Format the summary
# Fix the footer

#Aqua Glow Gel Face Moisturizer With Himalayan Thermal Water and Hyaluronic Acid for 72 Hours Hydration - 100ml
#Green Tea Face Wash With Green Tea & Collagen For Open Pores - 100 ml
# Onion Shampoo with Onion and Plant Keratin for Hair Fall Control - 200ml
# Vitamin C Foaming Face Wash Combo Pack with Refill - 150ml + 150ml