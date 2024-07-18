"""
To run this code as a local test, use the following console command:
```
pytest -v --docs-tests -k "how_to_connect_to_data_on_gcs_using_pandas" tests/integration/test_script_runner.py
```
"""

import great_expectations as gx

context = gx.get_context()

# Python
# <snippet name="docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/filesystem/how_to_connect_to_data_on_gcs_using_pandas.py define_add_pandas_gcs_args">
datasource_name = "my_gcs_datasource"
bucket_or_name = "my_bucket"
gcs_options = {}
# </snippet>

bucket_or_name = "test_docs_data"

# Python
# <snippet name="docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/filesystem/how_to_connect_to_data_on_gcs_using_pandas.py create_datasource">
datasource = context.data_sources.add_pandas_gcs(
    name=datasource_name, bucket_or_name=bucket_or_name, gcs_options=gcs_options
)
# </snippet>

assert datasource_name in context.data_sources.all()

# Python
# <snippet name="docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/filesystem/how_to_connect_to_data_on_gcs_using_pandas.py add_asset">
asset_name = "my_taxi_data_asset"
gcs_prefix = "data/taxi_yellow_tripdata_samples/"
batching_regex = r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2})\.csv"
data_asset = datasource.add_csv_asset(name=asset_name, gcs_prefix=gcs_prefix)
# </snippet>

assert data_asset

assert datasource.get_asset_names() == {"my_taxi_data_asset"}

my_batch_definition = data_asset.add_batch_definition_monthly(
    name="Monthly Taxi Data", regex=batching_regex
)
my_batch_request = my_batch_definition.build_batch_request(
    {"year": "2019", "month": "03"}
)
batches = data_asset.get_batch_list_from_batch_request(my_batch_request)
assert len(batches) == 1
assert set(batches[0].columns()) == {
    "vendor_id",
    "pickup_datetime",
    "dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "rate_code_id",
    "store_and_fwd_flag",
    "pickup_location_id",
    "dropoff_location_id",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
}
