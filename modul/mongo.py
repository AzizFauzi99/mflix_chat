from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.operations import SearchIndexModel
import time
from modul.llm import LLMClient

llm_client = LLMClient()

class MongoDBClient:
    def __init__(self):
        load_dotenv()
        username = os.environ['MONGO_USER']
        password = os.environ['MONGO_PASSWORD']
        uri = f"mongodb+srv://{username}:{password}@cluster0.tegtk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri, server_api=ServerApi('1'))

    def create_index(self, db_name, collection_name, index_name):
        """
        Create a vector search index in MongoDB
        
        :param db_name: Name of the database
        :param collection_name: Name of the collection
        :param index_name: Name of the index to create
        """
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "plot_embedding",
                        "numDimensions": 1536,
                        "similarity": "cosine"
                    }
                ]
            },
            name=index_name,
            type="vectorSearch",
        )
        result = self.client[db_name][collection_name].create_search_index(model=search_index_model)
        print(f"New search index named {result} is building.")
        print("Polling to check if the index is ready. This may take up to a minute.")

        predicate = lambda index: index.get("queryable") is True
        while True:
            indices = list(self.client[db_name][collection_name].list_search_indexes())
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        print(f"{result} is ready for querying.")

    def vector_search(self, query, db_name, collection_name, num_candidates=150, limit=5):
        """
        Perform vector search in MongoDB
        
        :param query: Search query string
        :param db_name: Name of the database
        :param collection_name: Name of the collection
        :param num_candidates: Number of candidates to search
        :param limit: Number of results to return
        :return: List of search results
        """
        query_vector = llm_client.get_embedding(query)

        pipeline = [
            {
                '$vectorSearch': {
                    'index': 'vector_index',
                    'path': 'plot_embedding',
                    'queryVector': query_vector,
                    'numCandidates': num_candidates,
                    'limit': limit
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'plot': 1,
                    'title': 1,
                    'score': {
                        '$meta': 'vectorSearchScore'
                    }
                }
            }
        ]

        result = list(self.client[db_name][collection_name].aggregate(pipeline))
        return result

    def insert_data(self, data):
        """
        Insert data to MongoDB
        
        :param data: Data to insert
        """
        db_name = "sample_mflix"
        collection_name1 = "embedded_movies"
        collection_name2 = "movies"
        self.client[db_name][collection_name2].insert_many(data)

        for item in data:
            item["plot_embedding"] = llm_client.get_embedding(item["plot"])
        self.client[db_name][collection_name1].insert_many(data)

        print(f"Data inserted to {db_name}.{collection_name1}")

    def update_data(self, filter_criteria, update_fields):
        """
        Update data in MongoDB collection.
        
        :param filter_criteria: Dictionary containing filter criteria to find documents to update
        :param update_fields: Dictionary containing fields and values to update
        """
        try:
            db_name = "sample_mflix"
            collection_name1 = "embedded_movies"
            collection_name2 = "movies"

            collection1 = self.client[db_name][collection_name1]
            collection2 = self.client[db_name][collection_name2]

            update_operation = {"$set": update_fields}

            result = collection1.update_many(filter_criteria, update_operation)
            collection2.update_many(filter_criteria, update_operation)

            print(f"Matched {result.matched_count} documents, updated {result.modified_count} documents.")
        except Exception as e:
            print(f"An error occurred while updating data: {e}")

    def delete_data(self, filter_criteria):
        """
        Delete data in MongoDB collection.
        
        :param filter_criteria: Dictionary containing filter criteria to find documents to delete
        """
        try:
            db_name = "sample_mflix"
            collection_name1 = "embedded_movies"
            collection_name2 = "movies"

            collection1 = self.client[db_name][collection_name1]
            collection2 = self.client[db_name][collection_name2]

            result = collection1.delete_many(filter_criteria)
            result2 = collection2.delete_many(filter_criteria)

            print(f"Deleted {result.deleted_count} documents in {collection_name1}.")
            print(f"Deleted {result2.deleted_count} documents in {collection_name2}.")
        except Exception as e:
            print(f"An error occurred while deleting data: {e}")