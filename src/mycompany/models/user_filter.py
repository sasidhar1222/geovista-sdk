from dataclasses import dataclass

from .enums import SortOrder
from .enums import UserSortField
from ..exceptions import ValidationError

@dataclass
class UserFilter:

    search: str | None = None

    name: str | None = None

    email: str | None = None

    sort_by: UserSortField | str | None = None

    sort_order: SortOrder | str = SortOrder.ASC

    def to_params(self) -> dict:

        params = {}

        # ==============================
        # SEARCH
        # ==============================

        if self.search is not None:
            params["search"] = self.search

        # ==============================
        # NAME
        # ==============================

        if self.name is not None:
            params["name"] = self.name

        # ==============================
        # EMAIL
        # ==============================

        if self.email is not None:
            params["email"] = self.email

        # ==============================
        # SORT BY
        # ==============================

        if self.sort_by is not None:

            if isinstance(self.sort_by, UserSortField):

                params["sort_by"] = self.sort_by.value

            elif isinstance(self.sort_by, str):

                try:

                    params["sort_by"] = UserSortField(
                        self.sort_by
                    ).value

                except ValueError:

                    allowed = ", ".join(
                        item.value
                        for item in UserSortField
                    )

                    raise ValidationError(
                        f"Invalid sort_by '{self.sort_by}'. "
                        f"Allowed values: {allowed}"
                    )

        # ==============================
        # SORT ORDER
        # ==============================

        if self.sort_order is not None:

            if isinstance(self.sort_order, SortOrder):

                params["sort_order"] = self.sort_order.value

            elif isinstance(self.sort_order, str):

                try:

                    params["sort_order"] = SortOrder(
                        self.sort_order.lower()
                    ).value

                except ValueError:

                    allowed = ", ".join(
                        item.value
                        for item in SortOrder
                    )

                    raise ValidationError(
                        f"Invalid sort_order '{self.sort_order}'. "
                        f"Allowed values: {allowed}"
                    )

        return params