import pytest

from mycompany.models.user_filter import UserFilter
from mycompany.exceptions import ValidationError


def test_invalid_sort_order():

    filters = UserFilter(
        sort_order="hello"
    )

    with pytest.raises(ValidationError):

        filters.to_params()

def test_valid_sort_order():

    filters = UserFilter(
        sort_order="asc"
    )

    params = filters.to_params()

    assert params["sort_order"] == "asc"        

def test_sort_order_case_insensitive():

    filters = UserFilter(
        sort_order="DESC"
    )

    params = filters.to_params()

    assert params["sort_order"] == "desc"   