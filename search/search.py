import datetime
from dataclasses import dataclass, field

from django.core.paginator import Paginator, Page
from django.db.models import Prefetch, Subquery, Q

from observations.models import DataCube, Observation

SPECTRAL_LINE_METADATA_KEY = 'filter1'


@dataclass
class SearchCriteria:
    polarimetry: str = None
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    instrument: str = None
    spectral_line_ids: list = field(default_factory=list)
    features: list = field(default_factory=list)


@dataclass
class SearchResult:
    observation_pk: int
    oid: str
    filename: str
    instrument: str
    date: datetime
    size: int
    thumbnail: str
    spectral_line_profile: str
    spectral_lines: list
    additional_values: list
    cubes_in_observation: list


def datetime_from_date(date, end_of_day=False):
    if end_of_day:
        return datetime.datetime(year=date.year, month=date.month, day=date.day, hour=23, minute=59, second=59)
    else:
        return datetime.datetime(year=date.year, month=date.month, day=date.day)


class Column:
    def __init__(self, name, only_spec):
        self.name = name
        self.only_spec = only_spec

    def get_name(self):
        return self.name

    def get_value(self, observation):
        raise NotImplementedError()

    def get_only_spec(self):
        return self.only_spec


class MetadataColumn(Column):
    def __init__(self, name, value_key):
        super().__init__(name, 'metadata__%s' % value_key)
        self.value_key = value_key

    def get_value(self, observation):
        return list(set([getattr(cube.metadata, self.value_key) for cube in observation.cubes.all()]))


class TagColumn(Column):
    def __init__(self, name):
        super().__init__(name, 'tags')

    def get_value(self, observation):
        return list(set([tag.name for cube in observation.cubes.all() for tag in cube.tags.all()]))


class AdditionalColumns:
    def __init__(self):
        self.additional_columns = []

    def __iter__(self):
        return self.additional_columns.__iter__()

    def add(self, column: Column):
        self.additional_columns.append(column)

    def get_all_names(self):
        return [col.get_name() for col in self.additional_columns if col.get_name() is not None]

    def get_all_only_specs(self):
        return [col.get_only_spec() for col in self.additional_columns if col.get_only_spec() is not None]


@dataclass
class SearchResultPage:
    page: Page
    additional_columns: AdditionalColumns


def _create_search_results_from_observation(observation, additional_columns):
    cube_count = observation.cubes.count()
    default_cube = observation.cubes.all()[0]

    if hasattr(default_cube, 'previews'):
        thumbnail = default_cube.previews.thumbnail if default_cube.previews else None
    else:
        thumbnail = None

    if hasattr(default_cube, 'spectral_line_data'):
        spectral_line_profile = default_cube.spectral_line_data.data_preview if default_cube.spectral_line_data else None
    else:
        spectral_line_profile = None

    spectral_lines = list(set([getattr(cube.metadata, SPECTRAL_LINE_METADATA_KEY) for cube in observation.cubes.all()]))

    additional_values = [col.get_value(observation) for col in additional_columns]

    total_size = sum(cube.size for cube in observation.cubes.all())

    return SearchResult(observation.id, default_cube.oid, default_cube.filename, default_cube.instrument.name,
                        default_cube.metadata.date_beg, total_size, thumbnail, spectral_line_profile,
                        spectral_lines, additional_values, cube_count)


class SearchResultsWrapper:
    """
    Wraps a Observation search results QuerySet and converts the items
    contained within it to SearchResult instances so that they can be
    easily presented in the interface.
    """

    def __init__(self, query_set, additional_columns, ordered=True):
        self.query_set = query_set
        self.additional_columns = additional_columns
        self.ordered = ordered

    def __getitem__(self, k):
        value = self.query_set.__getitem__(k)

        if isinstance(k, slice):
            value = [_create_search_results_from_observation(v, self.additional_columns) for v in value]
        else:
            value = _create_search_results_from_observation(value, self.additional_columns)

        return value

    def __len__(self):
        return self.query_set.__len__()


def search_observations(search_criteria: SearchCriteria, page_number=1, complex_query=Q()):
    additional_columns = AdditionalColumns()
    complete_query = {}

    if search_criteria.polarimetry == 'polarimetric':
        complete_query['cubes__metadata__naxis4__exact'] = 4
    elif search_criteria.polarimetry == 'nonpolarimetric':
        complete_query['cubes__metadata__naxis4__exact'] = 1

    # Date search criteria are always specified because they are needed to ensure that correct
    # query generation and prefetching. There is likely a specific cause for this that allows
    # us to address the problem with more precision, but that will require more time to debug
    # and figure out.
    complete_query['cubes__metadata__date_beg__gte'] = datetime_from_date(
        search_criteria.start_date) if search_criteria.start_date else datetime.datetime.min
    complete_query['cubes__metadata__date_end__lte'] = datetime_from_date(
        search_criteria.end_date, end_of_day=True) if search_criteria.end_date else datetime.datetime.max

    if search_criteria.spectral_line_ids:
        complete_query['cubes__metadata__%s__in' % SPECTRAL_LINE_METADATA_KEY] = search_criteria.spectral_line_ids

    if search_criteria.features:
        complete_query['cubes__tags__name__in'] = search_criteria.features
        additional_columns.add(TagColumn('Features'))

    if search_criteria.instrument and search_criteria.instrument != 'all':
        complete_query['cubes__instrument__name__iexact'] = search_criteria.instrument

    only_fields = ['oid', 'observation_id', 'filename', 'instrument__name', 'metadata__date_beg', 'size', 'previews',
                   'spectral_line_data', 'metadata__%s' % SPECTRAL_LINE_METADATA_KEY,
                   *additional_columns.get_all_only_specs()]

    observation_ids = Observation.objects.filter(complex_query).filter(**complete_query).only('pk').values_list(
        'pk', flat=True).distinct()

    datacube_dataset = DataCube.objects.only(*only_fields).select_related('metadata', 'instrument', 'previews',
                                                                          'spectral_line_data', 'observation')

    # It's tempting to add an .order_by('cubes__metadata__date_beg') here to ensure predictable sorting of the
    # search results in the list, but adding such a call to the QuerySet messes up the number of results returned
    # since the field we're sorting on can have many entries that matches the same Observation ID. Instead we
    # ensure that fields we want to sort on are present in the Observation model. If this becomes too much of
    # a limitation we will have to revisit the design.

    observations = Observation.objects.filter(pk__in=Subquery(observation_ids)).prefetch_related(
        Prefetch('cubes', queryset=datacube_dataset)).order_by('-date_beg')

    paginator = Paginator(observations, 25)
    page_obj = paginator.get_page(page_number)

    # Wrap the QuerySet to ensure that the caller will get a list of SearchResult items back.
    page_obj.object_list = SearchResultsWrapper(page_obj.object_list, additional_columns)

    return SearchResultPage(page=page_obj, additional_columns=additional_columns)
