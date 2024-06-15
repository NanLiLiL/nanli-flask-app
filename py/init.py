from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 存储电影条目的列表
movies = [
    {
        '_id': {'$oid': '666d2f84ccecf4ec14ada78c'},
        'rating': ['9.3', '50'],
        'rank': 1,
        'cover_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2564556863.jpg',
        'is_playable': 'True',
        'id': '1307914',
        'types': ['剧情', '犯罪', '惊悚'],
        'regions': ['中国香港'],
        'title': '无间道',
        'url': 'https://movie.douban.com/subject/1307914/',
        'release_date': '2003-09-05',
        'actor_count': 33,
        'vote_count': 1439034,
        'score': '9.3',
        'actors': ['刘德华', '梁朝伟', '黄秋生', '曾志伟', '陈慧琳', '郑秀文', '陈冠希', '余文乐', '萧亚轩', '林家栋', '吴廷烨', '林迪安', '尹志强', '许金峰', '何华超', '利沙华', '区轩玮', '李天翔', '黄燕强', '姚文基', '余世腾', '苏伟南', '黎志伟', '梁皓楷', '张旭燊', '袁伟豪', '叶清', '洪智杰', '张艺', '杨容莲', '李华柱', '曾健勇', '梁超怡'],
        'is_watched': 'False'
    },
    # ... 其他电影条目 ...
]

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    new_movie = request.form.to_dict()
    movies.append(new_movie)
    save_data(movies)
    return jsonify(new_movie)

@app.route('/delete/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = next((movie for movie in movies if movie['_id']['$oid'] == str(movie_id)), None)
    if movie:
        movies.remove(movie)
        save_data(movies)
        return jsonify({'message': 'Movie deleted'})
    else:
        return jsonify({'message': 'Movie not found'}), 404

@app.route('/update/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = next((movie for movie in movies if movie['_id']['$oid'] == str(movie_id)), None)
    if movie:
        movie.update(request.form.to_dict())
        save_data(movies)
        return jsonify(movie)
    else:
        return jsonify({'message': 'Movie not found'}), 404

@app.route('/search', methods=['GET'])
def search_movie():
    query = request.args.get('query', '').lower()
    filtered_movies = [movie for movie in movies if query in movie['title'].lower()]
    return jsonify(filtered_movies)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
