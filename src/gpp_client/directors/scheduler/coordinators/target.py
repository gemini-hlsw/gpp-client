from dataclasses import dataclass

from gpp_client.coordinator import BaseCoordinator
from gpp_client.subscribers import TargetSubscriber


@dataclass
class TargetCoordinator(BaseCoordinator):
    """
    Includes subscriber to handle subscriptions related to observations.
    """

    def __post_init__(self):
        self.subscribe_to: TargetSubscriber = TargetSubscriber(client=self.client)
