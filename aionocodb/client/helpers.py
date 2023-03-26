from dataclasses import dataclass

from .models import Project

import re


@dataclass
class NocoDBApiUris:
    API_V1_AUTH = "api/v1/auth"
    API_V1_DB_DATA = "api/v1/db/data"
    API_V1_DB_PUBLIC = "api/v1/db/public"
    API_V1_DB_META = "api/v1/db/meta"
    API_V1_DB_STORAGE = "api/v1/db/storage"


class Helpers:
    def __init__(self): pass


    def _base_uri(self, project: Project, table: str, args: list = [], is_bulk: bool = False, api_v: str = 'default'):
        return "/".join(
            (
                self.host,
                NocoDBApiUris.API_V1_DB_DATA if api_v == 'default' else api_v,
                "bulk" if is_bulk is True else "-del-",
                project.project_name,
                project.project_org,
                table if is_bulk is False else table,
                *[arg for arg in args]
            )
        ).replace("-del-/", "")
    
    
    def _storage_uri(self, args: list = []):
        return "/".join(
            (
                self.host,
                NocoDBApiUris.API_V1_DB_STORAGE,
                *[arg for arg in args]
            )
        )
    
    
    def handler(func):
        async def checker(self, *args, **kwargs):
            params = kwargs.copy()
            params = {k: v for k, v in params.items() if k not in ["project", "table"]}
            result = await func(self, *args, **kwargs, _=params)
            return result
        return checker