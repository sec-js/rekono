from findings.enums import DataType
from findings.models import OSINT
from tools.tools.base_tool import BaseTool


class EmailharvesterTool(BaseTool):
    '''EmailHarvester tool class.'''

    def parse_output_file(self) -> None:
        '''Parse tool output file to create finding entities.'''
        with open(self.path_output, 'r') as output_file:
            emails = output_file.readlines()                                    # Read emails
        for email in emails:
            self.create_finding(OSINT, data=email, data_type=DataType.EMAIL)