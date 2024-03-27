"""gr.State() component."""

from __future__ import annotations

import datetime
import math
from copy import deepcopy
from typing import Any, Callable

from gradio_client.documentation import document

from gradio.components.base import Component


@document()
class State(Component):
    EVENTS = []
    """
    Special hidden component that stores session state across runs of the demo by the
    same user. The value of the State variable is cleared when the user refreshes the page.

    Demos: interface_state, blocks_simple_squares
    Guides: real-time-speech-recognition
    """

    allow_string_shortcut = False

    def __init__(
        self,
        value: Any = None,
        render: bool = True,
        *,
        time_to_live: int | None = None,
        delete_callback: Callable[[None], None] | None = None,
    ):
        """
        Parameters:
            value: the initial value (of arbitrary type) of the state. The provided argument is deepcopied. If a callable is provided, the function will be called whenever the app loads to set the initial value of the state.
            render: has no effect, but is included for consistency with other components.
        """
        self.time_to_live = time_to_live or math.inf
        self.delete_callback = delete_callback or (lambda: None)
        self._created_at: datetime.datetime = datetime.datetime.now()
        try:
            self.value = deepcopy(value)
        except TypeError as err:
            raise TypeError(
                f"The initial value of `gr.State` must be able to be deepcopied. The initial value of type {type(value)} cannot be deepcopied."
            ) from err
        super().__init__(value=self.value, render=render)

    @property
    def stateful(self):
        return True

    @property
    def expired(self):
        return (datetime.datetime.now() - self._created_at).seconds > self.time_to_live

    def preprocess(self, payload: Any) -> Any:
        """
        Parameters:
            payload: Value
        Returns:
            Passes a value of arbitrary type through.
        """
        return payload

    def postprocess(self, value: Any) -> Any:
        """
        Parameters:
            value: Expects a value of arbitrary type, as long as it can be deepcopied.
        Returns:
            Passes a value of arbitrary type through.
        """
        return value

    def api_info(self) -> dict[str, Any]:
        return {"type": {}, "description": "any valid json"}

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        return None

    @property
    def skip_api(self):
        return True
