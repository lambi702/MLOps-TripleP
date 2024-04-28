from google.cloud import storage

def upload_blob(service_account_path, bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to the specified bucket."""
    storage_client = storage.Client.from_service_account_json(service_account_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)


def download_blob(service_account_path, bucket_name, gcs_blob_path, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client.from_service_account_json(service_account_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_blob_path)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {gcs_blob_path} downloaded to {destination_file_name}.")