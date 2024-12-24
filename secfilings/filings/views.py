from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
from transformers import AutoTokenizer
import json
from django.conf import settings
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from operator import or_
from llama_cpp import Llama
import os
from datetime import datetime
   
# Load the LLaMA model in .gguf format
llm = Llama(
        model_path=settings.LLAMA_MODEL,  # Path to the .gguf model
        temperature=0.75,
        max_tokens=2048,
       
        n_ctx=2048,  # Adjust context window
    n_batch=512,  # Adjust batch size
        verbose=True
    )
output_file = f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
   
class CSVInsightsAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_csv(file)
            csv_data = df.to_csv(index=False)
            insights_gpt = ''#generate_insights_from_csv(csv_data)
            insights_llama = generate_insights_from_csv_llama(csv_data)
            return JsonResponse({"insights": [insights_gpt, insights_llama]}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    def get(self, request):
        last_size = int(request.query_params.get("last_size", 0))  # Last read size
        from pathlib import Path
        try:
            # Using Path to combine settings.BASE_DIR with the file name
            file_dir = Path(settings.BASE_DIR) / output_file
            print(file_dir)
            # Check if the file exists
            if not file_dir.exists():
                return Response({"new_data": "", "current_size": last_size})
            
            # Get the current size of the file
            current_size = file_dir.stat().st_size

            # If the current size is larger than the last size, read the new data
            if current_size > last_size:
                with open(file_dir, "r") as f:
                    f.seek(last_size)
                    new_data = f.read()
                    return Response({"new_data": new_data, "current_size": current_size})

            # Return no new data if the size hasn't changed
            return Response({"new_data": "", "current_size": current_size})
        except Exception as e:
            return Response({"error": f"Error fetching data: {str(e)}"}, status=500)

def generate_insights_from_csv_llama(csv_data, max_tokens=2048, batch_size=500):
   csv_data_str = csv_data if isinstance(csv_data, str) else csv_data.to_csv(index=False)
   
   lines = csv_data_str.split('\n')
   header = lines[0]
   avg_tokens_per_row = len(header.split(',')) * 5
   safe_batch_size = min(batch_size, (max_tokens - 200) // avg_tokens_per_row)
   
   batches = [lines[i:i + safe_batch_size] for i in range(1, len(lines), safe_batch_size)]
   all_insights = []
   
   with open(output_file, 'w') as f:
       f.write("Data Analysis Results\n===================\n\n")
       
       for i, batch in enumerate(batches):
           batch_data = '\n'.join([header] + batch)
           prompt = f"Analyze this data batch:\n{batch_data}\nProvide key insights."
           
           try:
               response = llm.create_completion(
                   prompt=prompt,
                   max_tokens=1024,
                   temperature=0.7,
                   top_p=0.95,
                   top_k=40,
                   stream=False
               )
               insight = response['choices'][0]['text']
               all_insights.append(insight)
               f.write(f"Batch {i+1} Insights:\n{insight}\n\n")
           except RuntimeError as e:
               f.write(f"Error processing batch {i+1}: {e}\n")
               continue

       final_summary = '\n'.join(all_insights)
       f.write("\nFinal Summary:\n")
       f.write(final_summary)
   
   with open(output_file, 'r') as f:
       return f.read()
    
def generate_insights_from_csv(csv_data):
    llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
    print(llm,os.getenv("OPENAI_API_KEY"))

    prompt = PromptTemplate(
        input_variables=["data"],
        template="""
        [You are a data analyst. Here is a dataset:]
        [{data}]

        [Provide a detailed summary, including key patterns, trends, and insights on this SEC Filings data.]
        """
    )

    chain = prompt | llm

    insights = chain.invoke({"data": csv_data})
    return insights.content
class GenerateCSVAPIView(APIView):
    def get(self, request):
        # Directory containing the JSON files
        json_dir = settings.EXTRACTED_FILES_DIR  # Update to your actual JSON directory
        print(json_dir)  # Debugging purposes

        # Initialize a list to store the extracted data
        data = []

        # Loop through all JSON files in the directory
        for file in os.listdir(json_dir):
            if file.endswith('.json'):  # Ensure only JSON files are processed
                file_path = os.path.join(json_dir, file)

                # Open and read the JSON file
                with open(file_path, 'r') as f:
                    json_data = json.load(f)

                    # Extract required fields explicitly
                    general_info = {
                        "cik": json_data.get("cik"),
                        "company": json_data.get("company"),
                        "filing_type": json_data.get("filing_type"),
                        "filing_date": json_data.get("filing_date"),
                        "period_of_report": json_data.get("period_of_report"),
                        "sic": json_data.get("sic"),
                        "state_of_inc": json_data.get("state_of_inc"),
                        "state_location": json_data.get("state_location"),
                        "fiscal_year_end": json_data.get("fiscal_year_end"),
                        "filing_html_index": json_data.get("filing_html_index"),
                        "htm_filing_link": json_data.get("htm_filing_link"),
                        "complete_text_filing_link": json_data.get("complete_text_filing_link"),
                        "filename": file,  # Add filename for traceability
                    }

                    # Extract only item fields (item_1 to item_10 or variations like item_1A)
                    item_info = {key: json_data.get(key) for key in json_data.keys() if key.startswith('item_')}

                    # Merge general_info and item_info
                    extracted_info = {**general_info, **item_info}

                    # Append to data list
                    data.append(extracted_info)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data)

        # Fill NaN for missing keys
        df = df.fillna('')

        # Generate Insights
        insights = {}
        try:
            # 1. Most Active Filing Dates
            active_dates = df['filing_date'].value_counts().head(5).to_dict()
            insights['most_active_dates'] = active_dates

            # 2. Monthly Trends
            df['filing_month'] = pd.to_datetime(df['filing_date']).dt.month
            monthly_trends = df['filing_month'].value_counts().sort_index().to_dict()
            insights['monthly_trends'] = monthly_trends

            # 3. State of Incorporation
            top_states = df['state_of_inc'].value_counts().head(5).to_dict()
            insights['top_states'] = top_states

            # 4. SIC Codes
            top_sic = df['sic'].value_counts().head(5).to_dict()
            insights['top_sic'] = top_sic

            # 5. Fiscal Year-End
            top_fiscal_year_ends = df['fiscal_year_end'].value_counts().head(5).to_dict()
            insights['top_fiscal_year_ends'] = top_fiscal_year_ends
        except Exception as e:
            insights['error'] = str(e)

        # Save the DataFrame to a CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, "sec_filings.csv")
        df = df.head(10)
        df.to_csv(csv_file_path, index=False)

        # Prepare response
        response_data = {
            "insights": insights,
            "csv_file_url": request.build_absolute_uri(f"/media/sec_filings.csv")
        }

        # Serve the CSV directly if needed
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sec_filings.csv"'
        df.to_csv(response, index=False)
        df.to_csv('sec_filings.csv', index=False)
        
        return JsonResponse(response_data)
