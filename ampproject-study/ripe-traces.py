from datetime import datetime
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

ATLAS_API_KEY = "faf17fcb-bbc2-450f-8a68-a600d293f8c9"

ping = Ping(af=4, target="cdn.ampproject.org", description="testing new wrapper")

traceroute = Traceroute(
    af=4,
    target="cdn.ampproject.org",
    description="amp cdn",
    protocol="ICMP",
)

source1 = AtlasSource(
    type="country",
    value="KE",
    requested=5,
    tags={"exclude": ["system-anchor"]}
)

source2 = AtlasSource(
    type="country",
    value="TZ",
    requested=5,
    tags={"exclude": ["system-anchor"]}
)

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[traceroute],
    sources=[source1, source2],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()
