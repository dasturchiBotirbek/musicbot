from aiogram import Router

from . import admin, common, download, top


def build_root_router() -> Router:
    router = Router(name="root")
    router.include_router(admin.router)
    router.include_router(common.router)
    router.include_router(top.router)
    router.include_router(download.router)
    return router


__all__ = ["build_root_router"]
