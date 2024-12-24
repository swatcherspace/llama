Downlaod the Dataset from this website :- https://www.kaggle.com/datasets/pranjalverma08/sec-edgar-annual-financial-filings-2021

Then place it in the secfilings/ folder of the django appliction
To get the tredning insights:-
Below api will create a a sec_filings.csv
curl -X GET http://127.0.0.1:8000/filings/generate-csv/

After you will get the csv processed and the general trending insights about the data
Donwload the llama-2 .gguf file from the Huggingface then place it in secfilings/ folder of the django appliction
Using the latest llama-2 Model, which has been trained on 7 Billion Params.

If you already have the data then use that attaching like below i hve taken the already_processed file as a reference.

Below API will generate the results using llama-2 Model and save it in a temporary .txt file 

curl -X POST -F 'file=path to your csv file i.e sec_filings.csv' http://127.0.0.1:8000/filings/generate-insights/


Below API is which will be later on be retrieved by any API in the frontend in chunks(Async) or long polling, whatever the infrastruture is comfortable with.

