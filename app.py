from flask import Flask, render_template, request, redirect, url_for, flash
from hashtable import HashTable, Student
import logging
import os
from dotenv import load_dotenv


def create_app() -> Flask:
	# Load environment variables from .env if present
	load_dotenv()
	app = Flask(__name__)
	app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

	# Structured logging
	log_level = os.getenv("LOG_LEVEL", "INFO").upper()
	logging.basicConfig(
		level=getattr(logging, log_level, logging.INFO),
		format="%(asctime)s %(levelname)s %(name)s %(message)s"
	)
	logger = logging.getLogger("hash-table-app")

	# In-memory hash table for student records
	student_table = HashTable(num_buckets=17)

	@app.route("/")
	def index():
		return render_template("index.html")

	@app.route("/students", methods=["GET"])
	def list_students():
		students = student_table.items()
		# Search
		q = request.args.get("q", "").strip().lower()
		if q:
			def matches(s: Student) -> bool:
				return (
					q in s.student_id.lower() or
					q in s.name.lower() or
					q in s.grade.lower() or
					q in s.major.lower() or
					q == str(s.age)
				)
			students = [s for s in students if matches(s)]
		# Sort
		sort_by = request.args.get("sort_by", "student_id")
		order = request.args.get("order", "asc")
		key_map = {
			"student_id": lambda s: s.student_id,
			"name": lambda s: s.name.lower(),
			"age": lambda s: s.age,
			"grade": lambda s: s.grade,
			"major": lambda s: s.major.lower(),
		}
		key_fn = key_map.get(sort_by, key_map["student_id"])
		students = sorted(students, key=key_fn, reverse=(order == "desc"))
		return render_template("list.html", students=students, q=q, sort_by=sort_by, order=order)

	@app.route("/students/add", methods=["GET", "POST"])
	def add_student():
		if request.method == "POST":
			student_id = request.form.get("student_id", "").strip()
			name = request.form.get("name", "").strip()
			age_str = request.form.get("age", "").strip()
			grade = request.form.get("grade", "").strip()
			major = request.form.get("major", "").strip()
			if not student_id or not name or not age_str or not grade or not major:
				flash("All fields are required.", "error")
				return redirect(url_for("add_student"))
			try:
				age = int(age_str)
				if age <= 0 or age > 120:
					raise ValueError("Age out of range")
			except ValueError:
				flash("Age must be a valid positive integer.", "error")
				return redirect(url_for("add_student"))
			student = Student(student_id=student_id, name=name, age=age, grade=grade, major=major)
			# Upsert: add or replace existing
			existed = student_table.contains(student_id)
			student_table.set(student_id, student)
			if existed:
				flash(f"Updated existing student with ID {student_id}.", "success")
				logger.info("Updated student_id=%s", student_id)
			else:
				flash(f"Added student with ID {student_id}.", "success")
				logger.info("Added student_id=%s", student_id)
			return redirect(url_for("list_students"))
		return render_template("add.html")

	@app.route("/students/edit/<student_id>", methods=["GET", "POST"])
	def edit_student(student_id: str):
		existing = student_table.get(student_id)
		if existing is None:
			flash(f"No student found with ID {student_id}.", "info")
			return redirect(url_for("list_students"))
		if request.method == "POST":
			name = request.form.get("name", "").strip()
			age_str = request.form.get("age", "").strip()
			grade = request.form.get("grade", "").strip()
			major = request.form.get("major", "").strip()
			if not name or not age_str or not grade or not major:
				flash("All fields are required.", "error")
				return redirect(url_for("edit_student", student_id=student_id))
			try:
				age = int(age_str)
				if age <= 0 or age > 120:
					raise ValueError("Age out of range")
			except ValueError:
				flash("Age must be a valid positive integer.", "error")
				return redirect(url_for("edit_student", student_id=student_id))
			student_table.set(student_id, Student(student_id=student_id, name=name, age=age, grade=grade, major=major))
			flash(f"Updated student {student_id}.", "success")
			logger.info("Edited student_id=%s", student_id)
			return redirect(url_for("list_students"))
		return render_template("edit.html", s=existing)

	@app.route("/students/search", methods=["GET", "POST"])
	def search_student():
		result = None
		query_id = None
		if request.method == "POST":
			query_id = request.form.get("student_id", "").strip()
			if not query_id:
				flash("Student ID is required to search.", "error")
				return redirect(url_for("search_student"))
			result = student_table.get(query_id)
			if result is None:
				flash(f"No student found with ID {query_id}.", "info")
			else:
				logger.info("Searched student_id=%s found=%s", query_id, True)
		return render_template("search.html", result=result, query_id=query_id)

	@app.route("/students/delete", methods=["POST"])
	def delete_student():
		student_id = request.form.get("student_id", "").strip()
		if not student_id:
			flash("Student ID is required to delete.", "error")
			return redirect(url_for("list_students"))
		removed = student_table.remove(student_id)
		if removed:
			flash(f"Deleted student with ID {student_id}.", "success")
			logger.info("Deleted student_id=%s", student_id)
		else:
			flash(f"No student found with ID {student_id}.", "info")
		return redirect(url_for("list_students"))

	# Error handlers
	@app.errorhandler(404)
	def not_found(e):
		return render_template("404.html"), 404

	@app.errorhandler(500)
	def server_error(e):
		return render_template("500.html"), 500

	return app


if __name__ == "__main__":
	app = create_app()
	debug_env = os.getenv("FLASK_DEBUG", "1") == "1"
	host = os.getenv("HOST", "127.0.0.1")
	port = int(os.getenv("PORT", "5000"))
	app.run(host=host, port=port, debug=debug_env)

