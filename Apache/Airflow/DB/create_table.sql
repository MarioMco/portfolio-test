CREATE TABLE dim_currency(
    currency INT,
    curreny_label TEXT,
    currency_name TEXT,
    curency_description TEXT,
    etl_load_id INT,
    load_date TIMESTAMP,
    update_date TIMESTAMP
)

CREATE TABLE dim_channel(
channelkey INT,
channellabel TEXT,
channelname TEXT,
channeldescription TEXT,
etlloadid INT,
loaddate TIMESTAMP,
updatedate TIMESTAMP 
)