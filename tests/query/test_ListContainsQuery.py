# coding: utf-8

# https://docs.pytest.org/en/latest/
from pytest import raises

import yabadaba
from yabadaba import load_query

from test_Query import BaseTestQuery
import pandas as pd

class TestStrContainsQuery(BaseTestQuery):

    @property
    def style(self) -> str:
        return 'list_contains'

    def test_mongo(self):
        """Tests mongo query"""

        # Test setting path when loading
        query = load_query(self.style, path='root.element')
        assert query.path == 'root.element'

        # Test None value
        querydict = {}
        query.mongo(querydict, None)
        assert len(querydict) == 0

        # Check single value
        querydict = {}
        query.mongo(querydict, 'value')
        assert len(querydict['$and']) == 1
        assert querydict['$and'][0]['root.element'] == 'value'

        # Check multiple values
        querydict = {}
        query.mongo(querydict, ['value1', 'value2'])
        assert len(querydict['$and']) == 2
        assert querydict['$and'][0]['root.element'] == 'value1'
        assert querydict['$and'][1]['root.element'] == 'value2'

        # Check single value with prefix
        querydict = {}
        query.mongo(querydict, 'value', prefix='content.')
        assert len(querydict['$and']) == 1
        assert querydict['$and'][0]['content.root.element'] == 'value'

    @property
    def df(self) -> pd.DataFrame:
        """pd.Dataframe: demo data for filter testing"""

        return pd.DataFrame([
            {
                'name': 'first',
                'thisguy': ['value1'],
                'parent': [
                    {
                        'thisguy': ['pop', 'goes', 'the', 'weasel']
                    },
                    {
                        'thisguy': ['zoot', 'suit', 'riot']
                    }
                ],
            },
            {
                'name': 'second',
                'thisguy': ['value1', 'value2'],
                'parent': [
                    {
                        'thisguy': ['live', 'and', 'let', 'die']
                    },
                    {
                        'thisguy': ['flying', 'microtonal', 'banana']
                    }
                ],
            },
            {
                'name': 'third',
                'thisguy': ['value3', 'value4'],
                'parent': [
                    {
                        'thisguy': ['funk', '#49']
                    },
                    {
                        'thisguy': ['wheels', 'on', 'the', 'bus']
                    }
                ],
            },
        ])

    def test_pandas(self):
        """Tests pandas filter without a parent element"""

        df = self.df

        # Test setting path when loading
        query = load_query(self.style, name='thisguy')
        assert query.name == 'thisguy'

        # Test None value
        df2 = df[query.pandas(df, None)]
        assert len(df2) == 3

        # Test single missing value
        df2 = df[query.pandas(df, 'NOT THERE')]
        assert len(df2) == 0

        # Test single value
        df2 = df[query.pandas(df, 'value1')]
        assert len(df2) == 2
        assert df2.name.tolist()[0] == 'first'
        assert df2.name.tolist()[1] == 'second'

        # Test multiple values
        df2 = df[query.pandas(df, ['value1', 'value2'])]
        assert len(df2) == 1
        assert df2.name.tolist()[0] == 'second'

    def test_pandas_parent(self):
        """Tests pandas filter with a parent element"""

        df = self.df

        # Test setting parent when loading
        query = load_query(self.style, name='thisguy', parent='parent')
        assert query.name == 'thisguy'
        assert query.parent == 'parent'

        # Test directly setting parent
        query.parent = None
        assert query.parent is None
        query.parent = 'parent'
        assert query.parent == 'parent'

        # Test None value
        df2 = df[query.pandas(df, None)]
        assert len(df2) == 3

        # Test single missing value
        df2 = df[query.pandas(df, 'NOT THERE')]
        assert len(df2) == 0

        # Test single value
        df2 = df[query.pandas(df, 'the')]
        assert len(df2) == 2
        assert df2.name.tolist()[0] == 'first'
        assert df2.name.tolist()[1] == 'third'

        # Test multiple values
        df2 = df[query.pandas(df, ['the', 'bus'])]
        assert len(df2) == 1
        assert df2.name.tolist()[0] == 'third'

    def test_inline(self):
        """This tests the old non-class version of the queries"""

        assert isinstance(yabadaba.query.in_list.description(), str)
        assert isinstance(yabadaba.query.list_contains.description(), str)

        # Test mongo
        querydict = {}
        yabadaba.query.in_list.mongo(querydict, 'root.element', ['value1', 'value2'])
        assert len(querydict['$and']) == 2
        assert querydict['$and'][0]['root.element'] == 'value1'
        assert querydict['$and'][1]['root.element'] == 'value2'

        querydict = {}
        yabadaba.query.list_contains.mongo(querydict, 'root.element', ['value1', 'value2'])
        assert len(querydict['$and']) == 2
        assert querydict['$and'][0]['root.element'] == 'value1'
        assert querydict['$and'][1]['root.element'] == 'value2'

        # Test pandas
        df = self.df
        df2 = df[yabadaba.query.in_list.pandas(df, 'thisguy', ['the', 'bus'],
                                                    parent='parent')]
        assert len(df2) == 1
        assert df2.name.tolist()[0] == 'third'
        
        df2 = df[yabadaba.query.list_contains.pandas(df, 'thisguy', ['the', 'bus'],
                                                    parent='parent')]
        assert len(df2) == 1
        assert df2.name.tolist()[0] == 'third'