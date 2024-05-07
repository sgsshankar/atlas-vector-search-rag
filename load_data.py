from pymongo import MongoClient
from langchain_openai import AzureOpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
import key_param

# Set the MongoDB URI, DB, Collection Names
client = MongoClient(key_param.MONGO_URI)
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
searchIndexName ="default"
collection = client[dbName][collectionName]

# Initialize the DirectoryLoader
loader = DirectoryLoader( './sample_files', glob="./*.txt", show_progress=True)
data = loader.load()

# Define the OpenAI Embedding Model we want to use for the source data
# The embedding model is different from the language generation model
embeddings = AzureOpenAIEmbeddings(deployment=key_param.AZURE_EMBEDDINGS_DEPLOYMENT, 
                                    azure_endpoint = key_param.AZURE_OPENAI_ENDPOINT,
                                    openai_api_version = key_param.AZURE_OPENAI_API_VERSION,
                                    openai_api_key=key_param.AZURE_OPENAI_API_KEY,
                                    show_progress_bar=True)

# Initialize the VectorStore, and
# vectorise the text from the documents using the specified embedding model, and insert them into the specified MongoDB collection
vectorStore = MongoDBAtlasVectorSearch.from_documents( data, embeddings, collection=collection, index_name=searchIndexName)