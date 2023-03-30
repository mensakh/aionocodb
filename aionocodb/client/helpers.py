from aiohttp.client import ClientResponse

from dataclasses import dataclass
# from json import dumps

from .models import Project


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

            func_name = str(func).split(" ")[1].split(".")[1]
            exceptions_by_func = await Helpers.find_exceptions_by_func(func_name, kwargs)
            if exceptions_by_func is False:
                execution_result = await func(self, **kwargs, _=params)
                beautiful_result = await Helpers.make_beautiful(kwargs, func_name, execution_result)
                return beautiful_result
        return checker
    

    async def find_exceptions_by_func(kwargs, func_name, execution_result=None):
        match func_name:
            case "bulk_insert_rows":
                if len(kwargs.get("body")) == 0:
                    raise ValueError(f"{func_name} | No data to add in body argument")
                    
                for item in kwargs.get("body"):
                    if not isinstance(item, dict):
                        raise ValueError(f"{func_name} | Each element in body must be a dictionary")
        
        if execution_result is not None and isinstance(execution_result, dict):
            if "insert into" in execution_result["msg"] and "bulk_insert_rows" == func_name:
                raise ValueError(f"{func_name} | {execution_result}")
        return False


    async def make_beautiful(kwargs, func_name, execution_result):
        match func_name:
            case "row_exist":
                if isinstance(execution_result, bool) and "row_id" in kwargs:
                    return {"Id": kwargs["row_id"], "exist": bool(execution_result)}
            
            case "delete_all_rows_by_ids":
                if isinstance(execution_result, list):
                    result = []
                    for index, status in enumerate(execution_result):
                        result.append({"Id": kwargs["body"][index], "deleted": bool(status)})
                        if bool(status) is False: result[index].update({"exist": False})
                    return result
            
            case "bulk_insert_rows":
                result = await Helpers.find_exceptions_by_func(kwargs, func_name, execution_result)
                if result is False: return {"inserted": len(kwargs["body"])}

            case "update_all_rows_with_conditions":
                return {"updated": execution_result}

            case "delete_all_rows_with_conditions":
                return {"deleted": execution_result}


        #     case ""
        # if "msg" in list(execution_result):
        #     for exception in ["not found", "cannot read property 'id' of undefined"]:
        #         if exception in execution_result["msg"].lower():
        #             return {"Id": kwargs["row_id"], "exist": False}
        #     else:
        #         raise Exception(execution_result)
        return execution_result