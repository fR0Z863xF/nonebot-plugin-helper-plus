from pydantic import BaseModel, Extra
from pathlib import Path
import os,re
from typing import List


class Config(BaseModel, extra=Extra.ignore):
    
    config_path: Path=Path() / "data" / "helper"
    rule_group: List[str]=[]
    '''
    def __init__(self,**data):
        super().__init__(self,data)
        if not self.config_path.exists():
            os.makedirs(self.config_path)
        else:
            for root, ds, fs in os.walk(self.config_path):
                for f in fs:
                    if f.endswith('.json') and re.match(r'.*\d.*', f):
                        try:
                            str(f.split(".").get(0))
                            fullname = os.path.join(root, f)
                            self.rule_group.append(fullname)
                        except:
                            continue
    '''

    """Plugin Config Here"""
