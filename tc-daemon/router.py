import uvicorn
from pyroute2 import IPRoute
from fastapi import FastAPI

ipr = IPRoute()
ipr.bind()


app = FastAPI()


@app.get("/iface/{iface_name}")
async def iface_id(iface_name):
    with IPRoute() as ipr:
        iface = ipr.link_lookup(ifname=iface_name)
    return {"iface": iface[0]}
