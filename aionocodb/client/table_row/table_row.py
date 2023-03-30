from aiohttp.client import ClientSession
from aiohttp.client import ClientTimeout

from ..models import Project

from ..helpers import Helpers


class TableRow:
    """
       A class for working with table rows
    """
    def __init__(self, host, token, headers, session):
        self.host = host
        self.token = token
        self.headers = headers
        self.session = session
        self.session: ClientSession


    @Helpers.handler
    async def row_list(self,
                   project: Project,
                   table: str,
                   fields: list = None,
                   sort: list = None,
                   where: str = None,
                   limit: int = None,
                   shuffle: int = None,
                   offset: int = None,
                   timeout: int = None,
                   _: dict = "_gp"
                   ) -> dict:
        """
            This function makes it possible to extract existing rows from the table.

            fields: (list)
                Returns the fields that were specified in the list
        
            sort: (list)
                Sort by specified fields from the list

            where: (str)
                Comparison operator (sampling conditions)

            shuffle: (int)
                Shuffle the result for pagination

            limit: (int)
                Number of rows to retrieve (SQL limit)

            offset: (int)
                Offset for pagination (SQL offset value)

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-list

            -> More details about comparison operators and using where:
                https://docs.nocodb.com/developer-resources/rest-apis#comparison-operators
        """
        async with self.session.get(
            timeout=ClientTimeout(total=timeout if timeout is not None else timeout),
            params=_,
            url=Helpers._base_uri(self, project, table)
        ) as response:
            return await response.json()

    
    @Helpers.handler
    async def row_create(self,
                         project: Project,
                         table: str,
                         body: dict,
                         _: dict = "_gp"
                         ) -> dict:
        """
            Adds a new row to the table and returns it.

            body: (dict)

            Example of use:
                >>> await client.row_create(
                        project=project,
                        table=table,
                        body = {
                                'City name': 'Kharkiv',
                                'Description': 'Kharkiv had 1,426,540 permanent residents on January 1, 2019.'
                                }
                    )
            
            Returns:
                >>> {
                        'Id': 1,
                        'City name': 'Kharkiv',
                        'Description': 'Kharkiv had...'
                    }


            Pay attention!
                -> If you try to add a field that does not exist in the table, it will not be added.

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-create
        """
        async with self.session.post(
            json=body,
            url=Helpers._base_uri(self, project, table)
        ) as response:
            return await response.json()
    
    
    @Helpers.handler
    async def row_find_one(self,
                           project: Project,
                           table: str,
                           where: str,
                           fields: list = None,
                           sort: list = None,
                           _: dict = "_gp"
                           ) -> dict:
        """
            Allows you to retrieve a single row from a table if it matches the comparison conditions in where.

            where: (str)

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-find-one
        
            -> More details about comparison operators and using where:
                https://docs.nocodb.com/developer-resources/rest-apis#comparison-operators
        """
        _["limit"] = 1
        async with self.session.get(
            params=_,
            url=Helpers._base_uri(self, project, table, ["find-one"])
        ) as response:
            return await response.json()
        
    
    @Helpers.handler
    async def row_group_by(self,
                           project: Project,
                           table: str,
                           column_name: str,
                           sort: list = None,
                           where: str = None,
                           limit: int = None,
                           offset: int = None,
                           _: dict = "_gp"
                           ):
        """
            Allows you to get one field from all rows of the table by sorting the records.

            column_name: (str)
                The specified field will return with the data of this field
        
            sort: (list)
                Sorts by the specified fields from the list

            where: (str)
                Comparison operator (sampling conditions)
        
            limit: (int)
                Number of rows to retrieve (SQL limit)

            offset: (int)
                Offset for pagination (SQL offset value)

            Example of use:

                >>> await client.row_group_by(
                        project=project,
                        table=table,
                        column_name='City',
                        limit=25,
                        sort=["-City"],
                        offset=25*2
                    )

                -> The answer will be the second page with the previously specified field for each of the 25 lines

            Pay attention!
                -> To use offset correctly, you need to add a number,
                which is specified in the limit parameter, and also multiply it by the number of the desired page to obtain:
                    limit = 25
                    offset = limit * 2
        
            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-group-by

            -> More details about comparison operators and using where:
                https://docs.nocodb.com/developer-resources/rest-apis#comparison-operators
        """
        async with self.session.get(
            params=_,
            url=Helpers._base_uri(self, project, table, ["groupby"])
        ) as response:
            return await response.json()
        

    @Helpers.handler
    async def row_read(self,
                       project: Project,
                       table: str,
                       row_id: int,
                       fields: list = None,
                       _: dict = "_gp"
                       ) -> dict:
        """
            Allows you to get a row from a table using the row id.

            row_id: (int)
                The first row from the table will be retrieved
        
            fields: (list)
                Returns the fields that were specified in the list

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-read
        """
        async with self.session.get(
            params=_,
            url=Helpers._base_uri(self, project, table, [str(row_id)])
        ) as response:
            return await response.json()


    @Helpers.handler
    async def row_update(self,
                         project: Project,
                         table: str,
                         row_id: int,
                         body: dict,
                         _: dict = "_gp"
                         ):
        """
            Allows you to update the data of the desired row in the table.

            row_id: (int)
                The unique identifier of the row to update
        
            body: (dict)
                Data that will be updated in the specified line

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-update
        """
        async with self.session.patch(
            json=body,
            url=Helpers._base_uri(self, project, table, [str(row_id)])
        ) as response:
            return await response.json()


    @Helpers.handler
    async def row_delete(self,
                         project: Project,
                         table: str,
                         row_id: int,
                         _: dict = "_gp"
                         ):
        """
            Allows you to delete a row from a table.

            row_id: (int)
                The unique identifier of the row to delete

            Example of use:

                >>> await client.row_delete(
                        project=project,
                        table=table,
                        row_id=1
                    )
            
            Returns:

                >>> {'Id': 1, 'deleted': True}
                            or
                >>> {'Id': 1, 'deleted': False, 'exist': False}
        """
        return (await self.delete_all_rows_by_ids(self, project=project, table=table, body=[row_id]))[0]
    
        # -> Method reference from API:
        #         https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-delete

        # async with self.session.delete(
        #     url=Helpers._base_uri(self, project, table, [str(row_id)])
        # ) as response:
            # return await Response.table_row.row_delete(self, project=project, table=table, _gp=_, response=response)


    @Helpers.handler
    async def row_exist(self,
                         project: Project,
                         table: str,
                         row_id: int,
                         _: dict = "_gp"
                         ):
        """
            Allows you to check whether a row exists in a table.

            row_id: (int)
                The unique identifier of the row, to be checked

            Example of use:

                >>> await client.row_exist(
                        project=project,
                        table=table,
                        row_id=1
                    )
            
            Returns:

                >>> {'Id': 1, 'exist': True}
                            or
                >>> {'Id': 1, 'exist': False}

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-exist
        """
        async with self.session.get(
            url=Helpers._base_uri(self, project, table, [str(row_id), 'exist'])
        ) as response:
            return await response.json()
        

    @Helpers.handler
    async def bulk_insert_rows(self,
                               project: Project,
                               table: str,
                               body: list,
                               timeout: int = 5,
                               _: dict = "_gp"
                               ):
        """
            Allows you to add multiple rows to a table.

            Example of use:

                >>> await client.bulk_insert_rows(
                        project=project,
                        table=table,
                        body=[
                                {
                                    'Id': 1,
                                    'City name': "Kyiv"
                                },
                                {
                                    'Id': 2,
                                    'City name': "Kharkiv"
                                }
                            ]
                    )
            
            Returns:
            
                >>> {"inserted": 2}
        
            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-bulk-create
        """
        async with self.session.post(
            timeout = ClientTimeout(total=timeout),
            url=Helpers._base_uri(self, project, table, is_bulk=True),
            json=body
        ) as response:
            return await response.json()
        

    @Helpers.handler
    async def update_all_rows_by_ids(self,
                                     project: Project,
                                     table: str,
                                     body: dict,
                                     timeout: int = 5,
                                     _: dict = "_gp"
                                     ):
        """
            Allows you to update multiple rows in a table.
            
            Returns a sequence of digits that correspond to the indexes of the elements in the list of dictionaries to update.

            1 - The element at this index has been updated.

            0 - The element with the specified id in the dictionary does not exist in the table and was therefore not updated.

            Example of use:

                >>> await client.update_all_rows_by_ids(
                        project=project,
                        table=table,
                        body=[
                                 {
                                     'Id': 1,
                                     'City name': "Kyiv"
                                 },
                                 {
                                     'Id': 2,
                                     'City name': "Kharkiv"
                                 }
                             ]
                    )
            
            Returns:

                >>> [1, 1]
                    or
                >>> [0, 1]
        
            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-bulk-update
        """
        async with self.session.patch(
            timeout = ClientTimeout(total=timeout),
            url=Helpers._base_uri(self, project, table, is_bulk=True),
            json=body
        ) as response:
            return await response.json()
    

    @Helpers.handler
    async def delete_all_rows_by_ids(self,
                                     project: Project,
                                     table: str,
                                     body: list,
                                     timeout: int = 5,
                                     _: dict = "_gp"
                                     ):
        """
            Allows you to delete all rows from a table by id.

            Example of use:

                >>> await client.delete_all_rows_by_ids(
                        project=project,
                        table=table,
                        body=[1, 2, 3, ...]
                    )
            
            Returns:
                >>> [
                        {'id': 1, 'deleted': False, 'exist': False},
                        {'id': 2, 'deleted': True, 'exist': False},
                        {'id': 3, 'deleted': False, 'exist': False},
                        ...
                    ]
        
            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-bulk-delete
        """
        body = [{"Id": id} for id in body]
        async with self.session.delete(
            timeout = ClientTimeout(total=timeout),
            url=Helpers._base_uri(self, project, table, is_bulk=True),
            json=body
        ) as response:
            return await response.json()
        

    @Helpers.handler
    async def update_all_rows_with_conditions(self,
                                     project: Project,
                                     table: str,
                                     body: dict,
                                     where: str,
                                     _: dict = "_gp"
                                     ):
        """
            Allows you to update all rows in the table that meet the conditions.

            Example of use:

                >>> await client.update_all_rows_with_conditions(
                        project=project,
                        table=table,
                        body={"Population": 1,420,000},
                        where='(City name,eq,Kharkiv)'
                    )

            Returns:

                >>> {'updated': 1}
        
            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-bulk-update-all
        """
        del _["body"]
        async with self.session.patch(
            url=Helpers._base_uri(self, project, table, ["all"], is_bulk=True),
            params=_,
            json=body
        ) as response:
            return await response.json()

    
    @Helpers.handler
    async def delete_all_rows_with_conditions(self,
                                     project: Project,
                                     table: str,
                                     where: str,
                                     _: dict = "_gp"
                                     ) -> int:
        """
            Allows you to delete all rows from the table that match the conditions.
            
            Example of use:

                >>> await client.delete_all_rows_with_conditions(
                        project=project,
                        table=table,
                        where='(City name,eq,Kharkiv)'
                    )

            Returns:

                >>> {'deleted': 1}

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-bulk-delete-all
        """
        async with self.session.delete(
            url=Helpers._base_uri(self, project, table, ["all"], is_bulk=True),
            params=_
        ) as response:
            return await response.json()
        
    
    @Helpers.handler
    async def rows_export(self,
                          project: Project,
                          table: str,
                          timeout: int = 5,
                          _: dict = "_gp"
                          ):
        """
            Allows you to get rows from a table in .csv file format.

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-csv-export
        """
        async with self.session.get(
            timeout=ClientTimeout(total=timeout),
            url=Helpers._base_uri(self, project, table, ["export", "csv"])
        ) as response:
            return await response.content.read()

    
    @Helpers.handler
    async def nested_relations_row_list(self,
                          project: Project,
                          table: str,
                          row_id: int,
                          relation_type: str,
                          column_name: str,
                          limit: int = None,
                          offset: int = None,
                          where: str = None,
                          _: dict = "_gp"
                          ) -> dict:
        """
            Allows you to get a list of nested rows that are connected to another table.

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-nested-list
        """
        async with self.session.get(
            params=_,
            url=Helpers._base_uri(self, project, table, [str(row_id), relation_type, column_name])
        ) as response:
            return await response.json()
        
    
    @Helpers.handler
    async def nested_relations_row_add(self,
                                       project: Project,
                                       table: str,
                                       row_id: int,
                                       relation_type: str,
                                       column_name: str,
                                       ref_row_id: int,
                                       limit: int = None,
                                       offset: int = None,
                                       _: dict = "_gp"
                                       ):
        """
            Allows you to add a relation to a field in a row in a table.

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-nested-add
        """
        async with self.session.post(
            params=_,
            url=Helpers._base_uri(self, project, table, [str(row_id), relation_type, column_name, str(ref_row_id)])
        ) as response:
            return await response.json()

    
    @Helpers.handler
    async def nested_relations_row_remove(self,
                                       project: Project,
                                       table: str,
                                       row_id: int,
                                       relation_type: str,
                                       column_name: str,
                                       ref_row_id: int,
                                       _: dict = "_gp"
                                       ):
        """
            Allows you to delete a relationship in a field in a row from a table.

            -> Method reference from API:
                https://all-apis.nocodb.com/#tag/DB-table-row/operation/db-table-row-nested-remove
        """
        async with self.session.delete(
            url=Helpers._base_uri(self, project, table, [str(row_id), relation_type, column_name, str(ref_row_id)])
        ) as response:
            return await response.json()


    @Helpers.handler
    async def referenced_rows_excluding(self,
                                       project: Project,
                                       table: str,
                                       row_id: int,
                                       relation_type: str,
                                       column_name: str,
                                       limit: int = None,
                                       offset: int = None,
                                       where: str = None,
                                       _: dict = "_gp"
                                       ):
        async with self.session.get(
            params=_,
            url=Helpers._base_uri(self, project, table, [str(row_id), relation_type, column_name, "exclude"])
        ) as response:
            return await response.json()