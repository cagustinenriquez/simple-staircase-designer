from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

points = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/points', methods=['GET', 'POST'])
def point_api():
    if request.method == 'POST':
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify(error='Request must include JSON body with length and height'), 400
        try:
            length = float(payload.get('length', 0))
            height = float(payload.get('height', 0))
        except (TypeError, ValueError):
            return jsonify(error='Length and height must be numbers'), 400
        if length <= 0 or height <= 0:
            return jsonify(error='Length and height must be positive values'), 400
        points.append({'length': length, 'height': height})
        return jsonify(points=points)
    return jsonify(points=points)


@app.route('/api/points/reset', methods=['POST'])
def reset_points():
    points.clear()
    return jsonify(points=points)


@app.route('/api/points/<int:index>', methods=['DELETE'])
def delete_point(index):
    try:
        points.pop(index)
    except IndexError:
        return jsonify(error='Point not found'), 404
    return jsonify(points=points)


if __name__ == '__main__':
    app.run(debug=True)
