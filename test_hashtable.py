import pytest
from hashtable import HashTable, Student


def test_set_and_get():
	table = HashTable(num_buckets=5)
	table.set("S1", Student("S1", "A", "CS", 8.0))
	assert table.get("S1").name == "A"


def test_update_value():
	table = HashTable(num_buckets=5)
	table.set("S1", Student("S1", "A", "CS", 8.0))
	table.set("S1", Student("S1", "B", "IT", 9.0))
	val = table.get("S1")
	assert val.name == "B"
	assert val.department == "IT"
	assert val.gpa == 9.0


def test_remove():
	table = HashTable(num_buckets=5)
	table.set("S1", Student("S1", "A", "CS", 8.0))
	assert table.remove("S1") is True
	assert table.get("S1") is None
	assert table.remove("S1") is False


def test_resize_load_factor():
	table = HashTable(num_buckets=3)
	for i in range(10):
		table.set(f"S{i}", Student(f"S{i}", f"N{i}", "CS", 7.5))
	assert table.size() == 10
	assert table.bucket_count() > 3

