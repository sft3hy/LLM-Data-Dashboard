import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
from config import KAGGLE_API
    


def search_datasets(query, sort_by='hottest', size=6):
    """
    Searches Kaggle datasets based on a query.

    Parameters:
        api (KaggleApi): Authenticated Kaggle API object.
        query (str): Search term to query datasets.
        sort_by (str): Sort by criteria ('relevance', 'votes', 'updated', 'active').
        size (int): Limit the number of results (default is None, returns all).
    
    Returns:
        list: A list of datasets matching the query.
    """
    try:
        datasets = KAGGLE_API.dataset_list(search=query, sort_by=sort_by)
        if size:
            datasets = datasets[:size]
        return datasets
    except Exception as e:
        raise RuntimeError(f"Error searching datasets: {e}")

def download_dataset(dataset_slug, download_path='datasets', unzip=True):
    """
    Downloads a dataset from Kaggle.

    Parameters:
        api (KaggleApi): Authenticated Kaggle API object.
        dataset_slug (str): Slug of the dataset (e.g., 'zillow/zecon').
        download_path (str): Path to download the dataset (default is './datasets').
        unzip (bool): Whether to unzip the downloaded dataset (default is True).
    """
    try:
        os.makedirs(download_path, exist_ok=True)
        KAGGLE_API.dataset_download_files(dataset_slug, path=download_path, unzip=unzip)
        print(f"Dataset '{dataset_slug}' downloaded to {download_path}.")
    except Exception as e:
        raise RuntimeError(f"Error downloading dataset: {e}")

# # Example usage
# if __name__ == "__main__":
#     try:
#         # Set up the API

#         # Search for datasets
#         query = "russian equipment losses"
#         datasets = search_datasets(query, size=5)
#         print(f"Top 5 datasets for '{query}':")
#         for dataset in datasets:
#             print(dataset)
#             print(f" - {dataset.ref} | {dataset.title} | {dataset.size} | {dataset.description[:200]}")

#         # Example: Download the first dataset in the search result
#         if datasets:
#             first_dataset_slug = datasets[0].ref
#             # download_dataset(KAGGLE_API, first_dataset_slug)
#         else:
#             print("No datasets found for the query.")
#     except Exception as e:
#         print(str(e))
