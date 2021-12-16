import pytest
from valid8 import ValidationError

from core.domain_objects.cost import Cost


def test_create_cost_maximum_euros():
	c = Cost.create((10**7)-1, 5)
	assert c.euro == (10**7)-1


def test_create_cost_maximum_euros_fail():
	with pytest.raises(ValidationError):
		Cost.create((10**7) + 1, 5)


def test_create_cost_minimum_euros():
	c = Cost.create(0, 5)
	assert c.euro == 0


def test_create_cost_minimum_euros_fail():
	with pytest.raises(ValidationError):
		Cost.create(-1, 5)


def test_create_cost_maximum_cents():
	c = Cost.create(5, 99)
	assert c.cents == 99


def test_create_cost_maximum_cents_fail():
	with pytest.raises(ValidationError):
		Cost.create(5, 100)


def test_create_cost_minimum_cents():
	c = Cost.create(5, 0)
	assert c.cents == 0


def test_create_cost_minimum_cents_fail():
	with pytest.raises(ValidationError):
		Cost.create(5, -1)


def test_create_cost_value_in_cents():
	c = Cost.create(100, 50)
	assert c.value_in_cents == 10050


def test_cost_str():
	assert str(Cost.create(5279, 99)) == '5279.99'


def test_cost_parse():
	c_str = '8544.99'
	assert str(Cost.parse(c_str)) == c_str

