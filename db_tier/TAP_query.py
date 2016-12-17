from astropy.coordinates.sky_coordinate import SkyCoord
from gavo import votable
from gavo.votable.tapquery import RemoteError, WrongStatus, NetworkError

from base_query import LightCurvesDb
from conf import settings
from entities.exceptions import QueryInputError, NoInternetConnection
from utils.helpers import verbose


class TapClient(LightCurvesDb):
    '''
    Common class for all TAP db clients

    Attributes
    ----------
    COO_UNIT_CONV : int, float
        Conversion rate of coordinates from degrees

    QUOTING : list, tuple
        Expressions with any of these symbols are quoted
    '''

    COO_UNIT_CONV = 1
    QUOTING = [" ", "/", "_", "-", ".", "+"]

    def postQuery(self, tap_params):
        '''
        Post query according to given parameters

        Parameters
        -----------
        tap_params : dict 
            Tap query parameters. It has to contains four keys.

            Dict keys:
                URL(str)
                    Url of tap server

                table(str)
                    Name of table for query

                select(str/list)
                    Select string or list of column names

                conditions(list/tuple)
                    For each condition in the list of conditions there
                    is a tuple - ("name of column", "condition") or
                    ("name of column", "lower value", "upper value" for
                    search in the range

        Returns
        --------
        list of lists
            Result from the query as nested lists
        '''

        # Load tap protocol parameters
        self.URL = tap_params["URL"]
        self.table = tap_params["table"]
        if "/" in self.table and not (self.table.startswith('"') or
                                      self.table.startswith("'")):
            self.table = '"' + self.table + '"'
        self.conditions = tap_params["conditions"]
        self.select = tap_params["select"]

        query = self._get_select_text() + self._get_from_text() + \
            self._get_where_text()
        verbose(query, 4, settings.VERBOSITY)
        verbose("TAP query is about to start", 3, settings.VERBOSITY)

        # Run query
        try:
            job = votable.ADQLTAPJob(self.URL, query, timeout=1)
            job.run()
        except RemoteError:
            raise QueryInputError(
                "Wrong TAP query name column/table\n%s" % query)
        except WrongStatus:
            raise QueryInputError("Wrong TAP query url")
        except NetworkError:
            raise NoInternetConnection()

        retrieve_data = votable.load(job.openResult())[0]

        verbose("TAP query is done", 3, settings.VERBOSITY)
        job.delete()
        return retrieve_data

    def _get_select_text(self):
        '''Get SELECT part for query'''

        if (isinstance(self.select, (list, tuple, set))):
            select_text = "SELECT "
            for sel in set(self.select):
                if sel:
                    select_text += '"%s", ' % sel
            select_text = select_text[:-2] + " "
        elif (isinstance(self.select, str)):
            select_text = "SELECT %s " % self.select
        else:
            raise QueryInputError(
                "Select option was not resolved for TAP query\n%s" % self.select)
        return select_text

    def _get_from_text(self):
        '''Get GET part for query'''

        if (type(self.table) == str):
            return "FROM " + self.table + " "
        raise QueryInputError("Given table name is not string")

    def _get_where_text(self):
        '''Get WHERE part for query'''

        where_text = "WHERE "
        for _condition in self.conditions:
            condition = self._transfromCoo(_condition)
            condition = [self._quoteIfNeeded(cond) for cond in condition]

            if type(condition[1]) is tuple:
                condition = (condition[0], condition[1][0], condition[1][1])
            if (len(condition) == 3):
                where_text += "({0} BETWEEN {1} AND {2}) AND ".format(*
                                                                      condition)
            elif (len(condition) == 2):
                where_text += "({0} = {1}) AND ".format(*condition)
            else:
                raise QueryInputError(
                    "Unresolved TAP query condition: %s" % condition)
        where_text = where_text[:-4]
        return where_text

    def _transfromCoo(self, condition):
        if isinstance(condition[1], SkyCoord):
            new_cond = [condition[0]]
            for i in range(1, len(condition)):
                new_cond.append(condition[i].degree * self.COO_UNIT_CONV)
            return new_cond
        return condition

    def _areaSearch(self, ra, dec, delta):
        return (ra - delta / 3600.,
                ra + delta / 3600.), (dec - delta / 3600.,
                                      dec + delta / 3600.)

    def _quoteIfNeeded(self, value):
        value = str(value).strip()

        need_quoting = True in [let in value for let in self.QUOTING]

        if (need_quoting and not value.startswith("'") and
                not value.startswith('"')):
            return "'%s'" % value
        return value
