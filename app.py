import os
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Redis Connection
# Using environment variables for flexibility in K8s
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
db = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        keys = db.keys()
        tasks = []
        for key in keys:
            val = db.get(key)
            tasks.append({"id": key, "task": val})
        return jsonify(tasks), 200
    except redis.exceptions.ConnectionError:
        return jsonify({"error": "Redis unavailable"}), 503

@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.json
        task_content = data.get('task')
        if not task_content:
            return jsonify({"error": "Task content required"}), 400
        
        # Simple ID generation for demo
        task_id = db.dbsize() + 1
        db.set(task_id, task_content)
        return jsonify({"message": "Task added", "id": task_id}), 201
    except redis.exceptions.ConnectionError:
        return jsonify({"error": "Redis unavailable"}), 503

@app.route('/')
def hello():
    return "Hello from K8s Task-Master! <br> endpoints: GET /tasks, POST /tasks"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
