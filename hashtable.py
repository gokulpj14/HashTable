from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class Student:
	student_id: str
	name: str
	age: int
	grade: str
	major: str


class HashTable:
	def __init__(self, num_buckets: int = 17):
		if num_buckets <= 0:
			raise ValueError("num_buckets must be positive")
		self._num_buckets = num_buckets
		self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(num_buckets)]
		self._size = 0

	def _hash(self, key: str) -> int:
		# Simple polynomial rolling hash for strings
		p = 53
		m = self._num_buckets
		hash_value = 0
		p_pow = 1
		for ch in key:
			hash_value = (hash_value + (ord(ch) - 31) * p_pow) % m
			p_pow = (p_pow * p) % m
		return hash_value % m

	def _bucket_for(self, key: str) -> List[Tuple[str, Any]]:
		index = self._hash(key)
		return self._buckets[index]

	def set(self, key: str, value: Any) -> None:
		bucket = self._bucket_for(key)
		for i, (k, _) in enumerate(bucket):
			if k == key:
				bucket[i] = (key, value)
				return
		bucket.append((key, value))
		self._size += 1
		# Resize if load factor > 0.75
		if self.load_factor() > 0.75:
			self._resize(self._num_buckets * 2 + 1)

	def get(self, key: str) -> Optional[Any]:
		bucket = self._bucket_for(key)
		for k, v in bucket:
			if k == key:
				return v
		return None

	def contains(self, key: str) -> bool:
		return self.get(key) is not None

	def remove(self, key: str) -> bool:
		bucket = self._bucket_for(key)
		for i, (k, _) in enumerate(bucket):
			if k == key:
				del bucket[i]
				self._size -= 1
				return True
		return False

	def items(self) -> List[Any]:
		values: List[Any] = []
		for bucket in self._buckets:
			for _, v in bucket:
				values.append(v)
		return values

	def size(self) -> int:
		return self._size

	def bucket_count(self) -> int:
		return self._num_buckets

	def load_factor(self) -> float:
		return self._size / self._num_buckets

	def _resize(self, new_bucket_count: int) -> None:
		old_items = []
		for bucket in self._buckets:
			old_items.extend(bucket)
		self._num_buckets = new_bucket_count
		self._buckets = [[] for _ in range(self._num_buckets)]
		self._size = 0
		for k, v in old_items:
			self.set(k, v)

