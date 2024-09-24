import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                data.append(row)
            else:
                print(f"Ignoring invalid row: {row}")
    return data


def preprocess_query(query):
    processed_query = query.lower()
    return processed_query


def search_response(user_query):
    file_path = 'qR_file.csv'
    data = load_data(file_path)
    processed_user_query = preprocess_query(user_query)
    queries = [preprocess_query(row[0]) for row in data]
    responses = [row[1] for row in data]
    vectorizer = TfidfVectorizer()
    query_vectors = vectorizer.fit_transform(queries)
    user_query_vector = vectorizer.transform([processed_user_query])
    similarities = cosine_similarity(user_query_vector, query_vectors)[0]
    max_similarity_index = similarities.argmax()
    threshold = 0.7
    if user_query == "who made you" or user_query == "who created you" or user_query == "who is your creator":
        return "I'm sorry but that information is irrelevant"
    if similarities[max_similarity_index] > threshold:
        return responses[max_similarity_index]
    else:
        return "Sorry, I don't have a response for that."


def main():
    print("Press Ctrl+C to exit the program")
    try:
        while True:
            user_query = input("You: ")
            response = search_response(user_query)
            print("Bot:", response)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except EOFError:
        print("\nNo input detected. Program terminated.")


if __name__ == "__main__":
    main()
