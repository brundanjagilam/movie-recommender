from flask import Flask, request, render_template
import pickle


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)


def recommend(movie):
    movie = movie.strip().lower()
    print(f"Searching for: '{movie}'")  # Debugging

    movie_index = movies[movies['title'].str.strip().str.lower() == movie].index

    if len(movie_index) == 0:
        print("Movie not found!")  # Debugging
        return ["Movie not found"]

    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]


@app.route('/')
def home():
    return render_template('index.html', movie_titles=movies['title'].values)



@app.route('/recommend', methods=['POST'])
def recommend_route():
    movie = request.form['movie']
    recommendations = recommend(movie)

    return render_template('index.html', recommendations=recommendations, movie_titles=movies['title'].tolist())


if __name__ == "__main__":
    app.run(debug=True)
